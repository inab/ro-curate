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

"""API for validating Research Objects bundled as BagIt archives.

Usual usage of this API involves calling `validate` with the path to a
Research Object bundle as a parameter, then iterating over the errors
returned.

"""

from .errors import (
        ValidationError,
        ConstraintViolationError,
        MissingResourceError,
        MissingManifestError,
    )
from .graph import validate_graph
from .bundle import validate

VERSION = "0.2.0"
