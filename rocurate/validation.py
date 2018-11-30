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
import json
from bdbag import bdbag_api as bdbag
import rdflib
from rdflib import RDF
from rdflib.namespace import DCTERMS
from pyshacl import validate as shacl_validate
from rocurate.shapes import PATH as shapes_path

_MANIFEST_RELATIVE_PATHS = [
    'data/.ro/manifest.json',
    '.ro/manifest.json',
    'data/',
    '',
]


class ValidationError(Exception):
    pass


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
    If a suitable file is not found a `ValidationError` is thrown.
    :param ro_path: path to the root directory of the research object
    :return: `file` object for the most suitable manifest file
    """
    # Create a list of suitable absolute paths to tests for a manifest
    manifest_paths = list(map(
        lambda p: _ro_bundle_file_path(ro_path, p), _MANIFEST_RELATIVE_PATHS))

    # Try each path in `manifest_paths` in order until a manifest is found
    for file_path in manifest_paths:
        try:
            return file_path
        except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
            continue

    # If no manifest is found, raise exception
    raise ValidationError(
        f'Manifest not found in path(s): {manifest_paths}')


def validate(ro_path):
    """
    Validates the research object at the path `ro_path`, throwing an
    exception if an error is encountered.
    :param ro_path: relative or absolute path to the root directory of the
    research object
    """
    # Extract bag to temp directory and process the RO as a directory
    ro_path = bdbag.extract_bag(ro_path, temp=True)

    # Validate BagIt RO bag
    ro_path = os.path.abspath(ro_path)
    bdbag.validate_bag(ro_path)
    bdbag.validate_bag_structure(ro_path)

    # Get graph of manifest data
    manifest = find_manifest(ro_path)
    manifest_graph = rdflib.Graph()
    with open(manifest, 'r') as f:
        manifest_data = f.read()
    manifest_graph.parse(data=manifest_data, format='json-ld')

    # Get graph of shacl shapes
    shacl_graph = rdflib.Graph()
    with open(shapes_path, 'r') as f:
        shacl_data = f.read()
    shacl_graph.parse(data=shacl_data, format='turtle')

    # Validate manifest against shacl graph
    r = shacl_validate(manifest_graph, shacl_graph=shacl_graph,
                       inference='rdfs', target_graph_format='json-ld',
                       shacl_graph_format='turtle')
    conforms, results_graph, results_text = r
    if not conforms:
        print("Manifest is invalid: " + results_text)

    # Get optional graph in dct:conformsTo property of manifest graph
    ro = rdflib.Namespace('http://purl.org/wf4ever/ro#')
    for s, p, o in manifest_graph.triples((None, DCTERMS.conformsTo, None)):
        if (s, RDF.type, ro.ResearchObject) in manifest_graph:
            shacl_graph_2 = rdflib.Graph()
            shacl_graph_2.load(o)
            r = shacl_validate(manifest_graph, shacl_graph=shacl_graph_2,
                           inference='rdfs', target_graph_format='json-ld')
            conforms, results_graph, results_text = r
            if not conforms:
                print("Manifest is invalid: " + results_text)