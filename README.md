# ro-curate

ro-curate is a tool for validating and refining research objects.

## Requirements
- pyenv and pyenv-virtualenv
- Python 3.6.9+
- Python Modules:
  - bdbag>=1.5.6,<2.0
  - pyshacl
  - rdflib
  - pytest
  
Installation
------------

Directly from GitHub:

```
cd ${HOME}/user

git clone -b vre https://github.com/inab/ro-curate.git

cd ro-curate
```

Create the Python environment

```
pyenv-virtualenv 3.6.9 ro-curate
pyenv activate ro-curate
pip install -e .
pip install -r requirements.txt
```