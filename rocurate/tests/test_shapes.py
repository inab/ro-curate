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
from rocurate.shapes import PATH
from rocurate.validation import (
        validate_graph,
        ValidationError,
    )
from . import graph_validates


class TestResearchObjectShape(unittest.TestCase):
    def test_cardinalities(self):
        assert not graph_validates('simple-creator-0')
        assert graph_validates('simple-creator-1')
        assert graph_validates('simple-creator-5')

        assert not graph_validates('simple-created-0')
        assert graph_validates('simple-created-1')
        assert not graph_validates('simple-created-5')

        assert not graph_validates('simple-createdBy-0')
        assert graph_validates('simple-createdBy-1')
        assert graph_validates('simple-createdBy-5')

        assert not graph_validates('simple-createdOn-0')
        assert graph_validates('simple-createdOn-1')
        assert not graph_validates('simple-createdOn-5')
