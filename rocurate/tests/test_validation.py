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
from rocurate.validation import *
from . import data_file


class TestValidation(unittest.TestCase):
    def test_find_manifest_for_empty_bundle(self):
        with find_manifest(data_file('empty')) as manifest:
            data = manifest.read()
            assert data == ''

    def test_find_manifest_for_empty_json(self):
        path = data_file('empty/.ro/manifest.json')
        with find_manifest(path) as manifest:
            data = manifest.read()
            assert data == ''

    def test_validate_fails_for_empty_bundle(self):
        with self.assertRaises(Exception):
            validate(data_file('empty'))


