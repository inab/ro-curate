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
from rocurate.shapes import PATH as SHAPES_PATH
from rocurate.graph import validate_graph
from rocurate.errors import (
        ValidationError,
        MissingResourceError,
        MissingManifestError,
    )

_MANIFEST_RELATIVE_PATHS = [
    'metadata/manifest.json',
    'data/.ro/manifest.json',
    '.ro/manifest.json',
    '',
]


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
    If a suitable file is not found a `MissingManifestError` is thrown.
    :param ro_path: path to the root directory of the research object
    :return: `file` object for the most suitable manifest file
    """
    # Create a list of suitable absolute paths to tests for a manifest
    manifest_paths = map(lambda p: _ro_bundle_file_path(ro_path, p),
                         _MANIFEST_RELATIVE_PATHS)

    # Try each path in `manifest_paths` in order until a manifest is found
    for file_path in manifest_paths:
        if os.path.isfile(file_path):
            return file_path

    # If no manifest is found, raise exception
    raise MissingManifestError()


def validate(ro_path):
    """
    Validates the research object at the path `ro_path`, throwing an
    exception if an error is encountered.
    Throws urllib.error.HTTPError, ValidationError, MissingManifestError,
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
    manifest_graph = rdflib.Graph()
    try:
        manifest_path = find_manifest(ro_path)
    except MissingManifestError as err:
        yield err
        return
    with open(manifest_path, 'r') as f:
        manifest_graph.parse(data=f.read(), format='json-ld')

    # Validate manifest against shacl graph
    for err in validate_graph(manifest_graph):
        yield err

    # TODO: Get optional graph in dct:conformsTo property of manifest graph
    pass
