# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manver']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'semantic-version>=2.9.0,<3.0.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['manver = manver.cli:main']}

setup_kwargs = {
    'name': 'manver',
    'version': '1.0.0',
    'description': 'Bump your semantic version of any software using regex',
    'long_description': '# manver\n[![PyPI version](https://badge.fury.io/py/bump-semver-anywhere.svg)](https://badge.fury.io/py/bump-semver-anywhere)\n\nThis is a library intented to replace all semversion bumpers and finally be agnostic of the language / use case for your semantic versioning. This is achieved by providing the regex pattern to the place and filename of the string that contains the semantic version.\n\n## usage\n\n- install `pip install manver`\n- create a `.manver.toml` in the root of your project (see _config example_) or run `manver init`\n- run `manver bump -p patch`\n\n```console\nHello there. Today I want to show you a library I have been working on. I was inspired by necessity of changing all the versions in every file: `pyproject.toml`, `__init__.py`, `docker-compose.yaml`, `package.json`, etc. I searched for packages that do this but either they are specific to the language (Python or Javascript) or I did not like the customization for it. At the end I decided to create `manver`. This is inspired in [bump2version](https://github.com/c4urself/bump2version/) but with a much simpler approach. It uses TOML for configuration.\n\n> This is a library intended to replace all semantic version bumpers and finally be agnostic of the language. This is achieved by providing the regex pattern to the place and filename of the string that contains the version.\n\nconfiguration example:\n```toml\n# .manver.toml\n\n[general]\ncurrent_version = "0.1.2"\n\n[vcs]\ncommit = true\ncommit_msg = "release({part}): bump {current_version} -> {new_version}"\n\n[files]\n\n[files.python-module]\nfilename = "manver/__init__.py"\npattern = \'__version__ ?= ?"(.*?)"\'\n\n[files.python-pyproject]\nfilename = "pyproject.toml"\npattern = \'version ?= ?"(.*?)"\'\n```\n\nIt can be run as CLI `manver bump -p patch` or triggered via a Github action by commenting `/release patch`\n\n```console\n❯ python -m manver bump -p patch\n[-] Loading config from .manver.toml and bumping patch\n[=] config loaded\n[ ] files to update\n • manver/__init__.py: 0.1.1\n • pyproject.toml: 0.1.1\n • .manver.toml: 0.1.1\n[ ] VCS enabled with git\n[-] bumping patch version\n • manver/__init__.py -> 0.1.2\n • pyproject.toml -> 0.1.2\n • .manver.toml -> 0.1.2\n[*] saving files to disk\n[*] staging\n[*] commiting: release(patch): bump 0.1.1 -> 0.1.2\nblack....................................................................Passed\nisort....................................................................Passed\nflake8...................................................................Passed\n[main 5092515] release(patch): bump 0.1.1 -> 0.1.2\n 3 files changed, 3 insertions(+), 3 deletions(-)\n[+] bye bye\n```\n\n\nPS: If you have any suggestions for changing the name to a much simpler one I will be grateful.\nPS2: I accept PR and any feedback.\n\n\n### cli\n\n```console\n❯ manver --help\nUsage: python -m manver [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  bump  Bump your semantic version of any software using regex\n  init  Initialize the config\n```\n\n```console\n❯ manver bump --help\nUsage: python -m manver bump [OPTIONS]\n\n  Bump your semantic version of any software using regex\n\nOptions:\n  -c, --config FILE               the config file  [default:\n                                  .manver.toml]\n  -p, --part [major|minor|patch|prerelease]\n                                  the version part to bump  [required]\n  -n, --dry-run                   do not modify files\n  --help                          Show this message and exit.\n```\n\n```console\n❯ manver init --help\nUsage: python -m manver init [OPTIONS]\n\n  Initialize the config\n\nOptions:\n  -o, --output PATH  the output config file path  [default:\n                     .manver.toml]\n  --help             Show this message and exit.\n```\n\n## config example\n\nThe following example will bump the version for docker and a python or javascript package.\n\n```toml\n# .manver.toml\n\n[general]\ncurrent_version = "0.1.0"\n\n[vcs]\ncommit = true\ncommit_msg = "release({part}): bump {current_version} -> {new_version}"\n\n[files]\n\n[files.docker]\nfilename = "docker-compose.yaml"\npattern = \'image:.*?:(.*?)"\'\n\n[files.python-module]\nfilename = "__init__.py"\npattern = \'__version__ ?= ?"(.*?)"\'\n\n[files.python-pyproject]\nfilename = "pyproject.toml"\npattern = \'version ?= ?"(.*?)"\'\n\n[files.javascript]\nfilename = "package.json"\npattern = \'"version": ?"(.*?)"\'\n```\n\n## github action\n\nSee `.github/workflows/manver.yaml` to integrate the action to your repo.\n\nThe current behaviour is to comment `/release <part>` (e.g. `/release patch`) in a pull request. \nPer default it pushes the bump commit to the branch the PR points to. \nTherefore it should be commented after accepting the PR',
    'author': 'Ivan Gonzalez',
    'author_email': 'scratchmex@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scratchmex/all-relative',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
