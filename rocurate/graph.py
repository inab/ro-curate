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

"""API for validating Research Object coded as rdflib graphs.

This module should not be imported directly, instead import `rocurate`.

"""

import rdflib
import pyshacl
from rocurate.errors import ConstraintViolationError
from rocurate import shapes


_shacl_graph = None


def get_shacl_graph():
    """Lazily load the SHACL graph for the universal shape"""
    global _shacl_graph
    if _shacl_graph is None:
        _shacl_graph = rdflib.Graph()
        with open(shapes.PATH, 'r') as f:
            _shacl_graph.parse(data=f.read(), format="turtle")
        return _shacl_graph
    else:
        return _shacl_graph


def validate_graph(graph):
    """Validate an rdflib Graph object that encodes a research object.

    Checks the Research Object in the graph against a universal shape. Yields
    a value instance of a subclass of ValidationError for every issue found.

    Parameters
    ----------

    graph : rdflib.Graph
        An RDF graph that codes a Research Object.

    Yields
    ------

    ValidationError
        Each issue is yielded as a value of a subclass of ValidationError.
    """

    conforms, results, _ = \
        pyshacl.validate(graph, shacl_graph=get_shacl_graph())

    if not conforms:
        sh = rdflib.Namespace('http://www.w3.org/ns/shacl#')
        for result in results.subjects(rdflib.RDF.type, sh.ValidationResult):
            focus = results.value(result, sh.focusNode)
            path = results.value(result, sh.resultPath)
            value = results.value(result, sh.value)
            message = str(results.value(result, sh.resultMessage))
            yield ConstraintViolationError(focus, path, value, message)
