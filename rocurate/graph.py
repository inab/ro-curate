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

from urllib.request import urlopen
import re
import rdflib
import pyshacl
from rocurate.errors import ConstraintViolationError
from rocurate.util import path_to_uri
from rocurate import shapes

# Namespaces
ns = {
    'sh': rdflib.Namespace('http://www.w3.org/ns/shacl#'),
    'roc': rdflib.Namespace(
        'https://w3id.org/ro/curate#'),
}


def guess_format(path):
    formats = {
        'json': 'json-ld',
        'ttl': 'turtle',
        'rdf': 'xml',
    }
    for ext, fmt in formats.items():
        if path.endswith(ext):
            return fmt
    return None


FILE_ROOT_RE = re.compile(r'file://')


def _to_real_uri(uriref, archive_path):
    if isinstance(uriref, rdflib.term.URIRef):
        archive_uri = path_to_uri(archive_path)
        uri = FILE_ROOT_RE.sub(archive_uri, str(uriref))
        return rdflib.term.URIRef(uri)
    else:
        return uriref


def set_file_uri_base(graph, base):
    for s, p, o in graph:
        graph.remove((s, p, o))
        s = _to_real_uri(s, base)
        p = _to_real_uri(p, base)
        o = _to_real_uri(o, base)
        graph.add((s, p, o))


def get_graph(uri, base=None):
    """Returns an RDF graph from a URI."""
    graph = rdflib.Graph()
    fmt = guess_format(uri)
    with urlopen(uri) as f:
        data = f.read().decode("utf-8")
    graph.parse(data=data, format=fmt)
    if base:
        set_file_uri_base(graph, base)
    return graph


def get_shacl_graph():
    return get_graph(path_to_uri(shapes.PATH))


# Yields pairs of RDF paths and paths to SHACL the RDF should conform to.
def _get_graph_shacl_pairs(graph):
    for s, _, o in graph.triples((None, ns['roc'].conformsToSHACL, None)):
        yield str(s), str(o)


def validate_rdf_graph(graph, shacl):
    conforms, results, _ = pyshacl.validate(graph, shacl_graph=shacl)

    if not conforms:
        sh = ns['sh']
        for result in results.subjects(rdflib.RDF.type, sh.ValidationResult):
            focus = results.value(result, sh.focusNode)
            path = results.value(result, sh.resultPath)
            value = results.value(result, sh.value)
            message = str(results.value(result, sh.resultMessage))
            yield ConstraintViolationError(focus, path, value, message)


def validate_graph(graph, base=None):
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
    shacl_graph = get_shacl_graph()

    for err in validate_rdf_graph(graph, shacl_graph):
        yield err

    for graph_path, shacl_path in _get_graph_shacl_pairs(graph):
        graph = get_graph(graph_path, base=base)
        shacl_graph = get_graph(shacl_path)
        for err in validate_rdf_graph(graph, shacl_graph):
            yield err
