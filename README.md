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
git clone -b vre https://github.com/inab/ro-curate.git
```

Create the Python environment

```
python3 -m venv ro-curate/venv
source venv/bin/activate
pip install -r requirements.txt
```