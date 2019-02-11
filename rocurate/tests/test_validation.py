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


def iterator_empty(i):
    """Returns True if the given iterator is empty, else False.

    Note that this function consumes one element of the given iterator,
    provided it is non-empty.
    """
    try:
        next(i)
        return True
    except StopIteration:
        return False


def instance_in(klass, items):
    """Returns True if there is an instance of a specific class in items.

    Items are considered instances of a class if
    isinstance(class, item) == True.

    Returns False if the iterable of items is empty.
    """
    return any(isinstance(x, klass) for x in items)


class TestValidation(unittest.TestCase):
    def test_validation_for_simple_correct_bundle_succeeds(self):
        assert iterator_empty(validate(data_file('build/simple.zip')))

    def test_validation_for_empty_bundle_fails(self):
        errors = validate(data_file('build/empty.zip'))
        assert instance_in(ManifestNotFoundError, errors)

    def test_validation_for_missing_ro_prov_bundle_fails(self):
        errors = validate(data_file('build/ro-missing-prov.zip'))
        assert instance_in(ValidationError, errors)

    def test_validation_for_missing_remote_resource_fails(self):
        errors = validate(data_file('build/missing-remote-profile.zip'))
        assert instance_in(ResourceNotFoundError, errors)
