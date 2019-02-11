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

import os
from urllib.error import HTTPError
from bdbag import bdbag_api as bdbag
import rdflib
from rdflib import RDF
from rdflib.namespace import DCTERMS
from pyshacl import validate as shacl_validate
from rocurate.shapes import PATH as SHAPES_PATH

_MANIFEST_RELATIVE_PATHS = [
    'data/.ro/manifest.json',
    '.ro/manifest.json',
    'data/',
    '',
]


# TODO: make ValidationError a base class for all validation errors
class ValidationError(Exception):
    def __init__(self, results_graph, results_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results_graph = results_graph
        self.results_text = results_text

    def __str__(self):
        return self.results_text


class ResourceNotFoundError(Exception):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    def __str__(self):
        return f'resource not found at {self.path}'


# TODO: remove this?
class ManifestNotFoundError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'manifest file not found'


def _ro_bundle_file_path(ro_path, file_path):
    return os.path.abspath(os.path.join(ro_path, file_path))


def _ro_bundle_file(ro_path, file_path):
    """
    Helper function to get a file in an research object bundle.
    Throws the same exceptions as `open()` if there is a problem opening the
    file.
    :param ro_path: path to the root directory of the research object
    :param file_path: relative path to the file within the research object
    :return: `file` object for the file.
    """
    file_abspath = _ro_bundle_file_path(ro_path, file_path)
    return open(file_abspath)


def find_manifest(ro_path):
    """
    Finds the most likely manifest file in a research object.
    If a suitable file is not found a `ManifestNotFoundError` is thrown.
    :param ro_path: path to the root directory of the research object
    :return: `file` object for the most suitable manifest file
    """
    # Create a list of suitable absolute paths to tests for a manifest
    manifest_paths = list(map(
        lambda p: _ro_bundle_file_path(ro_path, p), _MANIFEST_RELATIVE_PATHS))

    # Try each path in `manifest_paths` in order until a manifest is found
    for file_path in manifest_paths:
        if os.path.isfile(file_path):
            return file_path

    # If no manifest is found, raise exception
    raise ManifestNotFoundError()


def _rdf_graph_from_file(path, fmt='json-ld'):
    """
    Throws ResourceNotFoundError.
    :param path:
    :param fmt:
    :return:
    """
    g = rdflib.Graph()
    try:
        with open(path, 'r') as f:
            data = f.read()
    except (FileNotFoundError, IsADirectoryError):
        raise ResourceNotFoundError(path)

    g.parse(data=data, format=fmt)
    return g


def _rdf_graph_from_remote(path):
    """
    Throws urllib.error.HTTPError.
    :param path:
    :return:
    """
    g = rdflib.Graph()
    try:
        g.load(path)
    except HTTPError as err:
        if err.code == 404:
            raise ResourceNotFoundError(path)
    return g


def _validate_rdf(rdf_graph, shacl_graph):
    conforms, graph, text = shacl_validate(rdf_graph, shacl_graph=shacl_graph)
    if not conforms:
        raise ValidationError(graph, text)


# TODO: make this function return an iterable of validation errors
def validate(ro_path):
    """
    Validates the research object at the path `ro_path`, throwing an
    exception if an error is encountered.
    Throws urllib.error.HTTPError, ValidationError, ManifestNotFoundError,
    json.decoder.JSONDecodeError.
    :param ro_path: relative or absolute path to the root directory of the
    research object
    """
    # Extract bag to temp directory and process the RO as a directory
    ro_path = bdbag.extract_bag(ro_path, temp=True)
    ro_path = os.path.abspath(ro_path)

    # Validate BagIt RO bag
    bdbag.validate_bag(ro_path)
    bdbag.validate_bag_structure(ro_path)

    # Get graphs for manifest and main profile
    manifest_graph = _rdf_graph_from_file(find_manifest(ro_path))
    shacl_graph = _rdf_graph_from_file(SHAPES_PATH, fmt='turtle')

    # Validate manifest against shacl graph
    _validate_rdf(manifest_graph, shacl_graph)

    # Get optional graph in dct:conformsTo property of manifest graph
    ro = rdflib.Namespace('http://purl.org/wf4ever/ro#')
    for s, p, o in manifest_graph.triples((None, DCTERMS.conformsTo, None)):
        if (s, RDF.type, ro.ResearchObject) in manifest_graph:
            shacl_graph_2 = _rdf_graph_from_remote(o)
            _validate_rdf(manifest_graph, shacl_graph_2)
