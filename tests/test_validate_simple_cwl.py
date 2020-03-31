#   Copyright 2020 Laura Rodriguez Navas - Barcelona Supercomputing Center
#
#   Based on Adam Cowdy implementation
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

from __future__ import absolute_import

import unittest
import six
import os

from schema_salad.schema import load_schema, load_and_validate
from schema_salad.validate import ValidationException
from pkg_resources import Requirement, resource_filename, ResolutionError  # type: ignore
from typing import Optional, Text

# change
WF = "/Users/laurarodrigueznavas/BSC/ro-curate/tests/data/src/cwlprofile/data/workflow/workflow.cwl"


def get_data(filename):  # type: (Text) -> Optional[Text]
    filepath = None
    try:
        filepath = resource_filename(
            Requirement.parse("schema-salad"), filename)
    except ResolutionError:
        pass
    if not filepath or not os.path.isfile(filepath):
        filepath = os.path.join(os.path.dirname(__file__), os.pardir, filename)
    return filepath


class TestValidate(unittest.TestCase):
    def test_validate_for_simple_correct_cwl_succeeds(self):
        document_loader, avsc_names, schema_metadata, \
            metaschema_loader = load_schema(get_data(u"tests/cwl/CommonWorkflowLanguage.yml"))

        try:
            load_and_validate(document_loader, avsc_names, six.text_type(get_data(WF)), True)
        except ValidationException as e:
            print("\n", e)
            raise
