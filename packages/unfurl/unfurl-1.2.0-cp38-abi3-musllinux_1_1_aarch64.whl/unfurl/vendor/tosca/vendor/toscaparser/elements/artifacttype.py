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

from toscaparser.elements.statefulentitytype import StatefulEntityType
from toscaparser.common.exception import ExceptionCollector
from toscaparser.common.exception import UnknownFieldError


class ArtifactTypeDef(StatefulEntityType):
    """TOSCA built-in artifacts type."""

    SECTIONS = (
        DERIVED_FROM,
        INTERFACES,
        ATTRIBUTES,
        PROPERTIES,
        DESCRIPTION,
        METADATA,
        VERSION,
        _SOURCE,
        MIME_TYPE,
        FILE_EXT,
    ) = (
        "derived_from",
        "interfaces",
        "attributes",
        "properties",
        "description",
        "metadata",
        "version",
        "_source",
        "mime_type",
        "file_ext",
    )

    properties = None
    mime_type = None
    file_ext = None


    def __init__(self, atype, custom_def=None):
        super(ArtifactTypeDef, self).__init__(atype, self.ARTIFACT_PREFIX, custom_def)
        if self.defs is not None:
            self.properties = self.defs.get(self.PROPERTIES)
            self.mime_type = self.defs.get("mime_type")
            self.file_ext = self.defs.get("file_ext", [])
            self._validate_keys()

    def _validate_keys(self):
        for key in self.defs.keys():
            if key not in self.SECTIONS:
                ExceptionCollector.appendException(
                    UnknownFieldError(what='Artifacttype "%s"' % self.type, field=key)
                )

    @property
    def parent_type(self):
        """Return a artifact entity from which this entity is derived."""
        if not hasattr(self, "defs"):
            return None
        partifact_entity = self.derived_from(self.defs)
        if partifact_entity:
            return ArtifactTypeDef(partifact_entity, self.custom_def)

    def get_artifact(self, name):
        """Return the definition of an artifact field by name."""
        if name in self.defs:
            return self.defs[name]
