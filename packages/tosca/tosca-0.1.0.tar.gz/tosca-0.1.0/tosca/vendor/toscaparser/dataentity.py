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

from toscaparser.common.exception import ExceptionCollector
from toscaparser.common.exception import MissingRequiredFieldError
from toscaparser.common.exception import TypeMismatchError
from toscaparser.common.exception import UnknownFieldError
from toscaparser.common.exception import ValidationError
from toscaparser.elements.constraints import Schema
from toscaparser.elements.datatype import DataType
from toscaparser.elements.portspectype import PortSpec
from toscaparser.elements.scalarunit import ScalarUnit_Frequency
from toscaparser.elements.scalarunit import ScalarUnit_Size
from toscaparser.elements.scalarunit import ScalarUnit_Time
from toscaparser.elements.scalarunit import ScalarUnit_Bitrate
from toscaparser.utils.gettextutils import _
from toscaparser.utils import validateutils
import collections.abc


class ValueDataType(object):
    def __init__(self, type):
        self.value_type = type
        self.defs = dict(type=type)

    def get_value(self, key, parent=False):
        return self.defs.get(key)

class DataEntity(object):
    """A complex data value entity."""

    def __init__(self, datatypename, value, custom_def=None, prop_name=None):
        self.custom_def = custom_def
        self.type = datatypename
        if datatypename in Schema.PROPERTY_TYPES:
            self.datatype = ValueDataType(datatypename)
            self.schema = {}
        else:
            self.datatype = DataType(datatypename, custom_def)
            if self.datatype.value_type:
                # "type" and "properties" are mutually exclusive
                self.schema = {}
            else:
                self.schema = self.datatype.get_properties_def()
        self.value = value
        self.property_name = prop_name
        self._properties = None

    @property
    def properties(self):
        if self._properties is None:
            from toscaparser.properties import Property

            values = self.value or {}
            self._properties = {
                name: Property(
                    name, values.get(name, aDef.default), aDef.schema, self.custom_def
                )
                for name, aDef in self.schema.items()
            }
        return self._properties

    def validate(self):
        """Validate the value by the definition of the datatype."""

        # A datatype can not have both 'type' and 'properties' definitions.
        # If the datatype has 'type' definition:
        if self.datatype.value_type:
            self.value = DataEntity.validate_datatype(
                self.datatype.value_type, self.value, None, self.custom_def, None, None, self
            )
            schema = Schema(self.property_name, self.datatype.defs)
            for constraint in schema.constraints:
                constraint.validate(self.value)
        # If the datatype has 'properties' definition:
        else:
            if not isinstance(self.value, collections.abc.Mapping):
                ExceptionCollector.appendException(
                    TypeMismatchError(what=self.value, type=self.datatype.type)
                )
                return self.value

            allowed_props = []
            required_props = []
            default_props = {}
            if self.schema:
                allowed_props = self.schema.keys()
                for name, prop_def in self.schema.items():
                    if prop_def.default is not None:
                        default_props[name] = prop_def.default
                    elif prop_def.required:
                        required_props.append(name)

            # check allowed field
            metadata = self.datatype.get_value('metadata', parent=True)
            if not metadata or not metadata.get('additionalProperties'):
                for value_key in list(self.value.keys()):
                    if value_key not in allowed_props:
                        ExceptionCollector.appendException(
                            UnknownFieldError(
                                what=(_('Data value of type "%s"') % self.datatype.type),
                                field=value_key,
                            )
                        )

            # check default field
            for def_key, def_value in default_props.items():
                if def_key not in self.value:
                    self.value[def_key] = def_value

            # check missing field
            missingprop = []
            for req_key in required_props:
                if req_key not in self.value:
                    missingprop.append(req_key)
            if missingprop:
                ExceptionCollector.appendException(
                    MissingRequiredFieldError(
                        what=(_('Data value of type "%s"') % self.datatype.type),
                        required=missingprop,
                    )
                )

            # check every field
            for name, value in list(self.value.items()):
                schema_name = self._find_schema(name)
                if not schema_name or value is None:
                    continue
                # skip validating null values, they need to be handled higher up in the stack
                # if value is None and name in required_props:
                #     msg = f'Field "{name}" of type "{self.datatype.type}" cannot be null.'
                #     ExceptionCollector.appendException(ValidationError(message=msg))
                #     continue
                prop_schema = Schema(name, schema_name)
                # check if field value meets type defined
                DataEntity.validate_datatype(prop_schema.type, value,
                                             prop_schema.entry_schema,
                                             self.custom_def, None,
                                             prop_schema.key_schema)
                # check if field value meets constraints defined
                if prop_schema.constraints:
                    for constraint in prop_schema.constraints:
                        if isinstance(value, collections.abc.MutableSequence):
                            for val in value:
                                constraint.validate(val)
                        else:
                            constraint.validate(value)

        return self.value

    def _find_schema(self, name):
        if self.schema and name in self.schema.keys():
            return self.schema[name].schema

    @staticmethod
    def validate_datatype(
        type, value, entry_schema=None, custom_def=None, prop_name=None, key_schema=None, self=None
    ):
        """Validate value with given type.

        If type is list or map, validate its entry by entry_schema(if defined)
        If type is a user-defined complex datatype, custom_def is required.
        """
        from toscaparser.functions import is_function

        if value is None or is_function(value):
            return value
        if type == Schema.ANY:
            return value
        if type == Schema.STRING:
            return validateutils.validate_string(value)
        elif type == Schema.INTEGER:
            return validateutils.validate_integer(value)
        elif type == Schema.FLOAT:
            return validateutils.validate_float(value)
        elif type == Schema.NUMBER:
            return validateutils.validate_numeric(value)
        elif type == Schema.BOOLEAN:
            return validateutils.validate_boolean(value)
        elif type == Schema.RANGE:
            return validateutils.validate_range(value)
        elif type == Schema.TIMESTAMP:
            validateutils.validate_timestamp(value)
            return value
        elif type == Schema.LIST:
            validateutils.validate_list(value)
            if entry_schema:
                DataEntity.validate_entry(value, entry_schema, custom_def)
            return value
        elif type == Schema.SCALAR_UNIT_SIZE:
            return ScalarUnit_Size(value).validate_scalar_unit()
        elif type == Schema.SCALAR_UNIT_FREQUENCY:
            return ScalarUnit_Frequency(value).validate_scalar_unit()
        elif type == Schema.SCALAR_UNIT_TIME:
            return ScalarUnit_Time(value).validate_scalar_unit()
        elif type == Schema.SCALAR_UNIT_BITRATE:
            return ScalarUnit_Bitrate(value).validate_scalar_unit()
        elif type == Schema.VERSION:
            return validateutils.TOSCAVersionProperty(value).get_version()
        elif type == Schema.MAP:
            validateutils.validate_map(value)
            if key_schema:
                DataEntity.validate_key(value, key_schema, custom_def)
            if entry_schema:
                DataEntity.validate_entry(value, entry_schema, custom_def)
            return value
        elif type in [Schema.PORTSPEC, Schema.PORTSPEC_FULLNAME]:
            ps = PortSpec.make(value)
            ps.validate()
            return ps
        elif type in [Schema.PORTDEF, Schema.PORTDEF_FULLNAME]:
            return validateutils.validate_portdef(value, prop_name)
        elif not self:
            return DataEntity(type, value, custom_def).validate()
        else:  # avoid infinite recursion
            return value

    @staticmethod
    def validate_entry(value, entry_schema, custom_def=None):
        """Validate entries for map and list."""
        schema = Schema(None, entry_schema)
        valuelist = value
        if isinstance(value, collections.abc.Mapping):
            valuelist = list(value.values())
        for v in valuelist:
            DataEntity.validate_datatype(schema.type, v,
                                         schema.entry_schema,
                                         custom_def, None,
                                         schema.key_schema)
            if schema.constraints:
                for constraint in schema.constraints:
                    constraint.validate(v)
        return value

    @staticmethod
    def validate_key(value, key_schema, custom_def=None):
        '''Validate keys for map'''
        schema = Schema(None, key_schema)
        valuelist = value
        if isinstance(value, collections.abc.Mapping):
            valuelist = list(value.keys())
        for v in valuelist:
            DataEntity.validate_datatype(schema.type, v,
                                         schema.entry_schema,
                                         custom_def, None,
                                         schema.key_schema)
            if schema.constraints:
                for constraint in schema.constraints:
                    constraint.validate(v)
        return value
