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
from rocurate import validate_graph
from . import data


class TestValidateGraph(unittest.TestCase):
    def test_yields_error_with_message_for_ro_with_no_created_date(self):
        g = data.graph('simple-ResearchObject-created-0')
        errors = validate_graph(g)
        violation = next(errors)
        self.assertEqual(violation.message, 'Missing creation date')
