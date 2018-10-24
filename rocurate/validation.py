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

_MANIFEST_RELATIVE_PATHS = [
    '.ro/manifest.json',
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
            return open(file_path, 'r')
        except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
            continue

    # If no manifest is found, raise exception
    raise ValidationError(
        f'Manifest not found in path(s): {manifest_paths}')


def validate(ro_path):
    """
    Validates the research object at the path `ro_path`, throwing an
    exception if an error is encountered or returning a list
    of warnings if successful.
    :param ro_path: path to the root directory of the research object
    """
    with find_manifest(ro_path) as manifest:
        manifest_data = json.load(manifest)
        print(manifest_data)
