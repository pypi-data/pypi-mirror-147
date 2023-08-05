# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['plexmatch']
setup_kwargs = {
    'name': 'plexmatch',
    'version': '0.1.0',
    'description': '',
    'long_description': "# plexmatch\n\n[![Test](https://github.com/Cologler/plexmatch-python/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Cologler/plexmatch-python/actions/workflows/test.yml)\n\nA simple library for handle [plexmatch](https://support.plex.tv/articles/plexmatch/) file.\n\n## Usage\n\n```python\nfrom pathlib import Path\nfrom plexmatch import parse, tostr\n\nplex_match = parse(Path('.plexmatch').read_text())\n# do something with plex_match, then:\nPath('.plexmatch').write_text(tostr(plex_match))\n```\n",
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
