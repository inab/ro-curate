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
import sys

_MANIFEST_RELATIVE_PATHS = [
    '.ro/manifest.json',
    '',
]


class ValidationError(Exception):
    pass


def read_manifest(ro_path):
    # Create a list of suitable absolute paths to tests for a manifest
    manifest_paths = list(map(
        lambda p: os.path.normpath(os.path.join(os.getcwd(), ro_path, p)),
        _MANIFEST_RELATIVE_PATHS,
    ))

    # Try each path in `manifest_paths` in order until a manifest is found
    for file_path in manifest_paths:
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except (FileNotFoundError, IsADirectoryError, NotADirectoryError):
            continue

    # If no manifest is found, raise exception
    raise ValidationError(
        f'Manifest not found in path(s): {manifest_paths}')


def validate(ro_path):
    """
    Validates the research object at the path `ro_path`, printing the results.
    :param ro_path: the path to the root directory of the research object
    """
    try:
        manifest_data = read_manifest(ro_path)
        print(manifest_data)
    except ValidationError as err:
        print(
            f'Error validating research object at \'{ro_path}\': {err}',
            file=sys.stderr,
        )
