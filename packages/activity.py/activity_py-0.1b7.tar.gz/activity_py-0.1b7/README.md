# activity.py

Load running activities, output into a neat JSON format.

[![PyPI](https://img.shields.io/pypi/v/activity.py.svg)](https://pypi.org/project/activity.py/)
[![Changelog](https://img.shields.io/github/v/release/sesh/activity.py?include_prereleases&label=changelog)](https://github.com/sesh/activity.py/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sesh/activity.py/blob/main/LICENSE)


## Installation

Install this library using `pip`:

    pip install activity.py


## Usage

Import `Activity` and use the `load_fit` and `load_gpx` function to load your activities.
You can access attributes on the activity at that point, or alternatively use `as_json` to dump your activity as a JSON object.

```python
from activity_py import Activity

activity = Activity.load_fit('fitfile.fit')
print(activity.duration, activity.distance, activity.pace)
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

    cd activity.py
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest

Using `pipenv`, this looks like:

    pipenv install .[test]
    pipenv run pytest


## Activity JSON

Documentation TBC.
