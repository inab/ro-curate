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

import sys
from argparse import ArgumentParser
from rocheck import VERSION


def main():
    args = ArgumentParser(description='Validate research objects.')
    args.add_argument('--version', action='version', version=VERSION)
    args.parse_args(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
