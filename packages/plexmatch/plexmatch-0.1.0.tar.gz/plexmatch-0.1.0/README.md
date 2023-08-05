# plexmatch

[![Test](https://github.com/Cologler/plexmatch-python/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Cologler/plexmatch-python/actions/workflows/test.yml)

A simple library for handle [plexmatch](https://support.plex.tv/articles/plexmatch/) file.

## Usage

```python
from pathlib import Path
from plexmatch import parse, tostr

plex_match = parse(Path('.plexmatch').read_text())
# do something with plex_match, then:
Path('.plexmatch').write_text(tostr(plex_match))
```
