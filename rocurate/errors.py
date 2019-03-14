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

This module should not be imported directly. Instead import `rocurate`.

"""


class ValidationError(Exception):
    pass


class ConstraintViolationError(ValidationError):
    def __init__(self, focus=None, path=None, value=None, message=''):
        super().__init__()
        self.focus = focus
        self.path = path
        self.value = value
        self.message = message

    def __str__(self):
        return f'Constraint violation in node "{self.focus}": {self.message}'


class MissingResourceError(ValidationError):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    def __str__(self):
        return f'resource not found at {self.path}'


class MissingManifestError(ValidationError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'manifest file not found'
