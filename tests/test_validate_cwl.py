from __future__ import absolute_import

import unittest
import six
import os

from schema_salad.schema import load_schema, load_and_validate
from schema_salad.validate import ValidationException
from pkg_resources import Requirement, resource_filename, ResolutionError  # type: ignore
from typing import Optional, Text


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


class TestErrors(unittest.TestCase):
    def test_errors(self):
        document_loader, avsc_names, schema_metadata, metaschema_loader = load_schema(
            get_data(u"tests/cwl/CommonWorkflowLanguage.yml"))

        for t in ("cwl/test1.cwl",
                  "cwl/test2.cwl",
                  "cwl/test3.cwl",
                  "cwl/test4.cwl",
                  "cwl/test5.cwl",
                  "cwl/test6.cwl",
                  "cwl/test7.cwl",
                  "cwl/test8.cwl",
                  "cwl/test9.cwl",
                  "cwl/test10.cwl",
                  "cwl/test11.cwl"):
            with self.assertRaises(ValidationException):
                try:
                    load_and_validate(document_loader, avsc_names,
                                      six.text_type(get_data("tests/" + t)), True)
                except ValidationException as e:
                    print("\n", e)
                    raise
