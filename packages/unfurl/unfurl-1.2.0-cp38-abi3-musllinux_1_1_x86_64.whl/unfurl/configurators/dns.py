from itertools import groupby
import os
from collections import defaultdict
from dataclasses import dataclass

try:
  from octodns.manager import Manager
  from octodns.zone import Zone

  # octodns installs natsort_keygen
  from natsort import natsort_keygen

  _natsort_key = natsort_keygen()
except ImportError:
    _natsort_key = None  # type: ignore

from ..configurator import Configurator, TaskView
from ..projectpaths import WorkFolder
from ..support import Status
from ..runtime import NodeInstance

from ..util import change_cwd
from ..eval import map_value
from toscaparser.properties import Property


# octodns requires keys in its yaml config to be sorted this way
def sort_dict(d):
    assert _natsort_key  # type: ignore
    keys_sorted = sorted(d.keys(), key=_natsort_key)
    return dict((k, d[k]) for k in keys_sorted)


@dataclass
class DnsProperties:
    """unfurl.nodes.DNSZone properties"""

    name: str
    """DNS name of the zone"""
    exclusive: bool
    """Remove records from the zone not specified in `records`"""
    provider: dict
    """OctoDNS provider configuration"""
    records: dict
    """DNS records to add to the zone"""
    default_ttl: int


def _get_records(attrs):
    # valid task error with a dependency for later evaluation
    records = attrs.get("records") or {}
    # sad hack:
    raw_records = attrs.context.currentResource.template.properties.get("records") or {}
    n_def = Property("", None, dict(type="string"))
    v_def = Property("", None, dict(type="list"))

    def _get_record(key):
        # key can be an expression:
        name = map_value(key, attrs.context)
        if attrs.validate and not name:
            attrs._validate(key, name, key, n_def)

        record = records[key]  # validates DNSRecord datatype
        # additional validation:
        if attrs.validate and "value" in record and record["value"] is None:
            attrs._validate("value", record["value"], raw_records[key]["value"], n_def)
        if attrs.validate and "values" in record and record["values"] is None:
            attrs._validate(
                "values", record["value"], raw_records[key]["values"], v_def
            )

        # value is a ResultsMap, make it a dict so we can serialize it as yaml
        return name, map_value(record, attrs.context)

    return dict(_get_record(key.strip()) for key in records)


def _get_zone(zone):
    if zone.endswith("."):
        return zone
    return zone + "."

def _forcelist(o):
    if not isinstance(o, list):
        return [o]
    return o

def _compare_records(name, expected, existing):
    if name not in existing:
        return 0
    current = existing[name]
    for r in _forcelist(expected):
        for s in _forcelist(current):
            if r["type"] == s["type"]:
                if r != s:
                    return -1  # differs
                break
        else:
            return 0  # not found
    return 1  # found

class DNSConfigurator(Configurator):
    """A configurator for managing a DNS zone using OctoDNS.
    Unless the ``exclusive`` attribute is set on the DNSZone instance, it will ignore records in the zone that are not specified in the ``records`` property.
    OctoDNS requires the full set of records for a zone so OctoDnsConfigurator will
    renders OctoDNS's configuration files using the zone data it last retrieved as saved in the ``zone`` attribute.
    The zone data is refreshed when the configurator is run by a job.
    The ``managed_records`` attribute tracks the records managed by the specification
    so that as the specification changes records which are no longer specified will be removed.
    """

    def can_dry_run(self, task):
        return True

    @classmethod
    def set_config_spec_args(cls, kw: dict, template):
        if _natsort_key is None:
            artifact = template.find_or_create_artifact("octodns", predefined=True)
            if artifact:
                kw["dependencies"].append(artifact)
        return kw

    def _update_zone(self, attributes, op, managed):
        records = attributes.get_copy("zone") or {}
        if attributes["exclusive"]:
            records.clear()
        elif attributes.get("managed_records"):
            # remove records we added before
            for key in attributes["managed_records"]:
                records.pop(key, None)
        if op == "configure":
            # (re)add the current records
            records.update(managed)
        return records

    def render(self, task: TaskView):
        """Create yaml config files which will be consumed by OctoDNS"""
        properties = self._extract_properties_from(task)
        managed = properties.records
        if isinstance(task.target, NodeInstance):
            for cap in task.target.get_capabilities("resolve"):
                for rel in cap.relationships:
                    managed.update(_get_records(rel.attributes))
        if task._errors:  # validation failed
            return managed

        # set up for the syncing that happens in run()
        folder = task.set_work_folder()
        self._create_main_config_file(folder, properties)

        op = task.configSpec.operation
        if op not in ["configure", "delete"]:
            return managed
        records = self._update_zone(task.target.attributes, op, managed)
        # create zone files
        self._write_zone_data(folder, properties.name, records)

        path = folder.cwd
        with change_cwd(path, task.logger):
            # raises an error if validation fails
            Manager(config_file="main-config.yaml").validate_configs()
        return managed

    @staticmethod
    def _write_zone_data(folder, zone, records):
        assert zone.endswith("."), f"{zone} name must end with '.'"
        folder.write_file(sort_dict(records), f"{zone}yaml")

    @staticmethod
    def _extract_properties_from(task) -> DnsProperties:
        attrs = task.vars["SELF"]
        name = _get_zone(attrs.get_copy("name"))
        exclusive = attrs.get_copy("exclusive")
        provider = attrs.get_copy("provider")
        records = _get_records(attrs)
        default_ttl = attrs.get_copy("default_ttl", 300)
        return DnsProperties(name, exclusive, provider, records, default_ttl)

    @staticmethod
    def _create_main_config_file(folder: WorkFolder, properties: DnsProperties):
        content = {
            "providers": {
                "source_config": {
                    "class": "octodns.provider.yaml.YamlProvider",
                    "directory": "./",
                    "enforce_order": True,
                    "default_ttl": properties.default_ttl,
                },
                "target_config": properties.provider,
            },
            "zones": {
                properties.name: {
                    "lenient": True,
                    "sources": ["source_config"],
                    "targets": ["target_config"],
                }
            },
        }
        folder.write_file(content, "main-config.yaml")

    def _dump_current_dns_records(self, task: TaskView, folder: WorkFolder):
        task.logger.debug("OctoDNS configurator - downloading current DNS records")

        path = folder.cwd
        zone_name = _get_zone(task.vars["SELF"]["name"])
        with change_cwd(path, task.logger):
            manager = Manager(config_file="main-config.yaml")
            zone = Zone(zone_name, manager.configured_sub_zones(zone_name))
            exists = manager.providers["target_config"].populate(zone, lenient=True)
            if not exists:
                return {}
            # now the zone.records has the latest records as a set
            # copied from https://github.com/octodns/octodns/blob/f6629f1ce49919d523f7d26eb14e9125348a3059/octodns/provider/yaml.py#L160
            # Order things alphabetically (records sort that way
            records = list(zone.records)
            records.sort()
            data = defaultdict(list)
            for record in records:
                d = record.data
                d["type"] = record._type
                if record.ttl == manager.providers["source_config"].default_ttl:
                    # ttl is the default, we don't need to store it
                    del d["ttl"]
                if record._octodns:
                    d["octodns"] = record._octodns
                data[record.name].append(sort_dict(d))

            # Flatten single element lists
            for k in data.keys():
                if len(data[k]) == 1:
                    data[k] = data[k][0]

            return sort_dict(data)

    def run(self, task: TaskView):
        """Apply DNS configuration"""
        # update zone and managed
        op = task.configSpec.operation
        task.logger.debug(f"OctoDNS configurator - run - {op}")
        if os.getenv("UNFURL_MOCK_DEPLOY"):
            managed = task.rendered
            task.vars["SELF"]["managed_records"] = managed
            task.logger.debug("setting managed_records %s", managed)
            yield task.done(success=True, modified=True, result="Mock OctoDNS synced")
        elif op in ["configure", "delete"]:
            yield self._run_octodns_sync(task)  # create or update zone
        elif op == "check" or op == "connect":
            yield self._run_check(task)
        else:
            raise NotImplementedError(f"Operation '{op}' is not allowed")

    def _run_octodns_sync(self, task: TaskView):
        managed = task.rendered
        # get the latest live records
        # XXX if check ran during this job don't recheck (check state change?)
        folder = task.get_work_folder()
        live = self._dump_current_dns_records(task, folder)
        zone = task.vars["SELF"]["zone"]
        if live != zone:  # zone data changed externally
            task.vars["SELF"]["zone"] = live
        updated = self._update_zone(
            task.target.attributes, task.configSpec.operation, managed
        )
        # note: render will already written the same data if live hasn't changed
        self._write_zone_data(folder, _get_zone(task.vars["SELF"]["name"]), updated)
        task.vars["SELF"]["managed_records"] = managed
        task.logger.debug("setting managed_records %s", managed)

        if updated == live:
            # nothing to do
            return task.done(success=True, modified=False)

        with change_cwd(folder.cwd, task.logger):
            manager = Manager(config_file="main-config.yaml")
            manager.sync(dry_run=task.dry_run)
            task.vars["SELF"]["zone"] = updated
            assert task.target.attributes is task.vars["SELF"]
            task.logger.debug("setting zone %s", updated)
            return task.done(success=True, modified=True, result="OctoDNS synced")

    def _run_check(self, task: TaskView):
        """Retrieves current zone data and compares with expected"""
        managed = task.rendered
        task.vars["SELF"]["managed_records"] = managed
        folder = task.get_work_folder()
        records = self._dump_current_dns_records(task, folder)
        modified = False
        if task.vars["SELF"]["zone"] != records:
            task.vars["SELF"]["zone"] = records
            modified = True
            self._write_zone_data(folder, _get_zone(task.vars["SELF"]["name"]), records)

        msg = None
        if task.vars["SELF"]["exclusive"]:
            if records == managed:
                status = Status.ok
            elif not records:
                status = Status.absent
            else:
                msg = "DNS zone is out of sync"
                status = Status.error
        else:
            if not records and managed:
                status = Status.absent
            else:
                match = False
                status = Status.ok
                msg = "DNS records in sync"
                for name, value in managed.items():
                    cmp = _compare_records(name, value, records)
                    if cmp > 0: # found
                        match = True
                    elif cmp < 0:  # doesn't match
                        msg = f"DNS zone is out of sync: expected to find {managed} in {records}"
                        status = Status.error
                        break                        
                    else:  # missing
                        if match:
                            msg = f"DNS zone is out of sync: expected to find {managed} in {records}"
                            status = Status.error
                            break
                        else:
                            msg = "DNS records missing"
                            status = Status.absent                        

        if msg:
            task.logger.verbose(msg)
        # XXX save managed in outputs
        return task.done(True, modified=modified, status=status, result=msg)
