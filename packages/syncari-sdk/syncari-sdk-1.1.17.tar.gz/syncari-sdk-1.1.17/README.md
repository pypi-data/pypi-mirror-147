# Syncari Python SDK

Syncari Python Synapse Development Kit or `synapse-sdk`

### Setup
For the first time, after checkout of this repository, create a python virtual environment
```
python3 -m venv .
source bin/activate
pip install .
```

### Linter
To run pylint after changes, run the command `./run_linter.sh`. For any new folder, modify the `run_linter.sh` to add the folder to the linter.

### Tests
To run pytests, run the command 
```
pytest unittests
```

### Publishing synapse-sdk to pypi

First time install tools needed to publish
```
pip install wheel
pip install twine
```

And to publish:

```
rm -rf dist 
python setup.py sdist bdist_wheel
twine check dist/* 
twine upload dist/*
syncaridev/!Syncari123#
```