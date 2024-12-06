#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from toscaparser.common.exception import ExceptionCollector, TypeMismatchError
from toscaparser.common.exception import UnknownFieldError
from toscaparser.common.exception import MissingRequiredFieldError
from toscaparser.entity_template import EntityTemplate
from toscaparser.utils import validateutils

# 3.6.7 Artifact definition p84
SECTIONS = (
    METADATA,
    DESCRIPTION,
    FILE,
    REPOSITORY,
    DEPLOY_PATH,
    VERSION,
    CHECKSUM,
    CHECKSUM_ALGORITHM,
    PERMISSIONS,
    INTENT,
    TARGET,
    ORDER,
    CONTENTS,
    TYPE,
    PROPERTIES,  # TYPE and PROPERTIES should be last
) = (
    "metadata",
    "description",
    "file",
    "repository",
    "deploy_path",
    "version",
    "checksum",
    "checksum_algorithm",
    "permissions",
    "intent",
    "target",
    "order",
    "contents",
    "type",
    "properties",
)

log = logging.getLogger("tosca")


class Artifact(EntityTemplate):
    """Artifacts defined in Node types or templates."""

    SECTIONS = SECTIONS

    def __init__(self, name, artifact, custom_def=None, base=None, tosca_template=None):
        if isinstance(artifact, str):
            artifact = dict(file=artifact, type="tosca.artifacts.Root")
        elif isinstance(artifact, dict) and "type" not in artifact:
            artifact = dict(artifact, type="tosca.artifacts.Root")
        super(Artifact, self).__init__(name, artifact, "artifact_type", custom_def, tosca_template)
        for key in SECTIONS[:-2]:  # skip "type" and "properties"
            setattr(self, key, artifact.get(key))
        self._source = base
        if self.metadata:
            validateutils.validate_map(self.metadata)
        # XXX validate file ext matches type definition
        self._validate_required_fields(artifact)

    @property
    def mime_type(self):
        # XXX if not set deduce from file ext
        return self.type_definition.mime_type

    @property
    def file_extensions(self):
        return self.type_definition.file_ext

    def _validate_required_fields(self, template):
        if "file" not in template:
            ExceptionCollector.appendException(
                MissingRequiredFieldError(
                    what='Artifact "%s"' % self.name, required="file"
                )
            )
        if "permissions" in template and not isinstance(template["permissions"], str):
            ExceptionCollector.appendException(
                TypeMismatchError(
                    what='Permission field on artifact "%s"' % self.name, type="string"
                )
            )
