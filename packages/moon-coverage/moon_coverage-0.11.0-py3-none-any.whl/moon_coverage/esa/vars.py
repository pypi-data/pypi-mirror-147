"""ESA variables."""

from pathlib import Path


DATA = Path.home() / '.moon-coverage-esa-crema'

DATA.mkdir(exist_ok=True, parents=True)
