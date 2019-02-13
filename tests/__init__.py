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
import rdflib
from rocurate.validation import validate_graph

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def data_file(file):
    return os.path.join(DATA_DIR, file)


def robundle(name):
    return data_file(f'build/{name}.zip')


def rordf(name):
    return data_file(f'rdf/{name}.ttl')


def graph_validates(name):
    g = rdflib.Graph()
    with open(rordf(name), 'r') as f:
        data = f.read()
    g.parse(data=data, format='turtle')
    try:
        next(validate_graph(g))
        return False
    except StopIteration:
        return True
