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

from toscaparser.common.exception import (
    InvalidTOSCAVersionPropertyException)
from toscaparser.tests.base import TestCase
from toscaparser.utils.gettextutils import _
from toscaparser.utils.validateutils import TOSCAVersionProperty


class TOSCAVersionPropertyTest(TestCase):

    def test_tosca_version_property(self):
        version = '18.0.3.beta-1'
        expected_output = '18.0.3.beta-1'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

        version = 18
        expected_output = '18'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

        version = 18.0
        expected_output = '18.0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

        version = '18.0.3'
        expected_output = '18.0.3'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

        version = 0
        expected_output = '0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = 00
        expected_output = '0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

        version = 0.0
        expected_output = '0.0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

        version = 00.00
        expected_output = '0.0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

        version = '0.0.0'
        expected_output = '0.0.0'
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))

    def test_tosca_version_property_invalid_major_version(self):

        version = 'x'
        exp_msg = _('Value of TOSCA version property "x" is invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_minor_version(self):

        version = '18.x'
        exp_msg = _('Value of TOSCA version property "18.x" is invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

        version = '18.x.y'
        exp_msg = _('Value of TOSCA version property "18.x.y" is invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

        version = '18-2'
        exp_msg = _('Value of TOSCA version property "18-2" is invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_fix_version(self):

        version = '18.0.a'
        exp_msg = _('Value of TOSCA version property "18.0.a" is invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_qualifier(self):
        # change test, this is now valid because we support semantic versioning syntax (https://semver.org/)
        version = '18.0.1-xyz'
        expected_output = '18.0.1-xyz'
        output = TOSCAVersionProperty(version).get_version()
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))
        self.assertEqual(output, expected_output)

        # valid semver 2.0:
        assert TOSCAVersionProperty("18.0.1-xyz.1").pre_release == "xyz.1"
        full = TOSCAVersionProperty("18.0.1-xyz.1+7527a406")
        assert full.pre_release == "xyz.1"
        assert full.build_metadata == "7527a406"
        assert TOSCAVersionProperty("18.0.1+7527a406").build_metadata == "7527a406"

        version = 'v2'
        expected_output = 'v2'
        assert TOSCAVersionProperty(version).is_semver_compatible_with(TOSCAVersionProperty(version))
        output = TOSCAVersionProperty(version).get_version()
        self.assertEqual(output, expected_output)

        version = '0.0.0.abc'
        exp_msg = _('Value of TOSCA version property "0.0.0.abc" is invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_invalid_build_version(self):
        version = '18.0.1.abc-x'
        exp_msg = _('Value of TOSCA version property '
                    '"18.0.1.abc-x" is invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

        version = '0.0.0.abc-x'
        exp_msg = _('Value of TOSCA version property "0.0.0.abc-x" is '
                    'invalid.')
        err = self.assertRaises(InvalidTOSCAVersionPropertyException,
                                TOSCAVersionProperty, version)
        self.assertEqual(exp_msg, err.__str__())

    def test_tosca_version_property_semver_compatibility(self):
        assert TOSCAVersionProperty("v1.1.0").is_semver_compatible_with(
                                    TOSCAVersionProperty("v1.2.0"))
        assert not TOSCAVersionProperty("2.1.0").is_semver_compatible_with(
                                    TOSCAVersionProperty("1.2.0"))
        assert TOSCAVersionProperty("0.1.0").is_semver_compatible_with(
                                    TOSCAVersionProperty("v0.1.0"))

