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


def graph_validates(name):
    """Return True if a graph validates without error, else False."""
    try:
        next(validate_graph(data.graph(name)))
        return False
    except StopIteration:
        return True


class TestResearchObjectShape(unittest.TestCase):
    def test_cardinalities(self):
        assert not graph_validates('simple-ResearchObject-creator-0')
        assert graph_validates('simple-ResearchObject-creator-1')
        assert graph_validates('simple-ResearchObject-creator-5')

        assert not graph_validates('simple-ResearchObject-created-0')
        assert graph_validates('simple-ResearchObject-created-1')
        assert not graph_validates('simple-ResearchObject-created-5')

        assert not graph_validates('simple-ResearchObject-createdBy-0')
        assert graph_validates('simple-ResearchObject-createdBy-1')
        assert graph_validates('simple-ResearchObject-createdBy-5')

        assert not graph_validates('simple-ResearchObject-createdOn-0')
        assert graph_validates('simple-ResearchObject-createdOn-1')
        assert not graph_validates('simple-ResearchObject-createdOn-5')

        assert graph_validates('simple-ResearchObject-isDescribedBy-0')
        assert graph_validates('simple-ResearchObject-isDescribedBy-1')
        assert not graph_validates('simple-ResearchObject-isDescribedBy-5')


class TestAggregationShape(unittest.TestCase):
    def test_cardinalities(self):
        assert not graph_validates('simple-Aggregation-aggregates-0')
        assert graph_validates('simple-Aggregation-aggregates-1')
        assert graph_validates('simple-Aggregation-aggregates-3')


class TestManifestShape(unittest.TestCase):
    def test_cardinalities(self):
        assert not graph_validates('simple-Manifest-creator-0')
        assert graph_validates('simple-Manifest-creator-1')
        assert graph_validates('simple-Manifest-creator-5')

        assert not graph_validates('simple-Manifest-created-0')
        assert graph_validates('simple-Manifest-created-1')
        assert not graph_validates('simple-Manifest-created-5')

        assert not graph_validates('simple-Manifest-createdBy-0')
        assert graph_validates('simple-Manifest-createdBy-1')
        assert graph_validates('simple-Manifest-createdBy-5')

        assert not graph_validates('simple-Manifest-createdOn-0')
        assert graph_validates('simple-Manifest-createdOn-1')
        assert not graph_validates('simple-Manifest-createdOn-5')

        assert graph_validates('simple-Manifest-describes-0')
        assert graph_validates('simple-Manifest-describes-1')
        assert not graph_validates('simple-Manifest-describes-5')


class TestProxyShape(unittest.TestCase):
    def test_cardinalities(self):
        assert not graph_validates('simple-Proxy-proxyFor-0')
        assert graph_validates('simple-Proxy-proxyFor-1')
        assert not graph_validates('simple-Proxy-proxyFor-5')

        assert not graph_validates('simple-Proxy-proxyIn-0')
        assert graph_validates('simple-Proxy-proxyIn-1')
        assert not graph_validates('simple-Proxy-proxyIn-5')


class TestAnnotationShape(unittest.TestCase):
    def test_cardinalities(self):
        assert not graph_validates('simple-Annotation-hasBody-0')
        assert graph_validates('simple-Annotation-hasBody-1')
        assert not graph_validates('simple-Annotation-hasBody-5')

        assert not graph_validates('simple-Annotation-body-0')
        assert graph_validates('simple-Annotation-body-1')
        assert not graph_validates('simple-Annotation-body-5')

        assert not graph_validates('simple-Annotation-annotatesResource-0')
        assert graph_validates('simple-Annotation-annotatesResource-1')
        assert not graph_validates('simple-Annotation-annotatesResource-5')

        assert not graph_validates(
                'simple-Annotation-annotatesAggregatedResource-0')
        assert graph_validates(
                'simple-Annotation-annotatesAggregatedResource-1')
        assert not graph_validates(
                'simple-Annotation-annotatesAggregatedResource-5')

        assert not graph_validates('simple-Annotation-hasTarget-0')
        assert graph_validates('simple-Annotation-hasTarget-1')
        assert not graph_validates('simple-Annotation-hasTarget-5')

        assert not graph_validates('simple-Annotation-creator-0')
        assert graph_validates('simple-Annotation-creator-1')
        assert graph_validates('simple-Annotation-creator-5')

        assert not graph_validates('simple-Annotation-created-0')
        assert graph_validates('simple-Annotation-created-1')
        assert not graph_validates('simple-Annotation-created-5')

        assert not graph_validates('simple-Annotation-createdBy-0')
        assert graph_validates('simple-Annotation-createdBy-1')
        assert graph_validates('simple-Annotation-createdBy-5')

        assert not graph_validates('simple-Annotation-createdOn-0')
        assert graph_validates('simple-Annotation-createdOn-1')
        assert not graph_validates('simple-Annotation-createdOn-5')


# class TestFolderEntryShape(unittest.TestCase):
#     def test_cardinalities(self):
#         assert not graph_validates('simple-FolderEntry-entryName-0')
#         assert graph_validates('simple-FolderEntry-entryName-1')
#         assert not graph_validates('simple-FolderEntry-entryName-5')
