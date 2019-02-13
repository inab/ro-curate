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

"""Contains exceptions returned/thrown by the rocurate API.

Classes:
    - ValidationError
    - MissingManifestError
    - MissingResourceError

"""


class ValidationError(Exception):
    def __init__(self, results_graph, results_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results_graph = results_graph
        self.results_text = results_text

    def __str__(self):
        return self.results_text


class ResourceNotFoundError(ValidationError):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    def __str__(self):
        return f'resource not found at {self.path}'


class ManifestNotFoundError(ValidationError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'manifest file not found'
