#   Copyright 2018 Adam Cowdy
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import unittest
from rocurate.validation import (
        validate,
        ManifestNotFoundError,
        ResourceNotFoundError,
        ValidationError,
    )
from . import data_file


class TestValidation(unittest.TestCase):
    def test_validation_for_simple_correct_bundle_succeeds(self):
        validate(data_file('build/simple.zip'))

    def test_validation_for_empty_bundle_fails(self):
        with self.assertRaises(ManifestNotFoundError):
            validate(data_file('build/empty.zip'))

    def test_validation_for_missing_ro_prov_bundle_fails(self):
        with self.assertRaises(ValidationError):
            validate(data_file('build/ro-missing-prov.zip'))

    def test_validation_for_missing_remote_resource_fails(self):
        with self.assertRaises(ResourceNotFoundError):
            validate(data_file('build/missing-remote-profile.zip'))
