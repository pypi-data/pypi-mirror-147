"""Events csv file module."""

from pathlib import Path

from .event import AbstractEvent, EventsDict, EventsList
from ..html import Html, table
from ..misc import logger


warn, _ = logger('EventsFileParser')


class EventsFile(EventsDict):
    """Event File object.

    Parameters
    ----------
    fname: str or pathlib.Path
        Input CSV event filename.
    primary_key: str, optional
        Header primary key (default: `name`)
    header: str, optional
        Optional header definition (to be appended at the beging of the file).

    """
    fields, rows = [], []

    def __init__(self, fname, primary_key='name', header=None):
        super().__init__([])

        self.primary_key = primary_key.lower()
        self.header = header
        self.fname = fname

    def __str__(self):
        return self.fname.name

    def __repr__(self):
        events = super().__str__()
        return f'<{self.__class__.__name__}> {self} {events}'

    def __getitem__(self, key):
        if isinstance(key, str) and key.lower() in self.fields:
            i = self.fields.index(key.lower())
            return [row[i] for row in self.rows]

        return super().__getitem__(key)

    def _ipython_key_completions_(self):
        return list(self.keys()) + self.fields

    @property
    def fname(self):
        """Events filename."""
        return self.__fname

    @fname.setter
    def fname(self, fname):
        """Parse events file."""
        self.__fname = Path(fname)

        if not self.fname.exists():
            raise FileNotFoundError(fname)

        csv_text = (self.header + '\n') if self.header else ''
        csv_text += self.fname.read_text()

        self._parse_csv(csv_text)

    def _parse_csv(self, csv_text):
        """Parse rows content as Events objects."""
        self.fields, self.rows = self._read_csv(csv_text)

        # Extract primary key values
        if self.primary_key not in self.fields:
            raise KeyError(f'Primary key `{self.primary_key}` not found')

        i = self.fields.index(self.primary_key)

        for row in self.rows:
            kwargs = dict(zip(self.fields, row))
            key = row[i]
            k = key.upper()

            if k.endswith('_START') or k.endswith('_DESC'):
                key, _ = key.rsplit('_', 1)  # pop `_START` and `_DESC`

                start = kwargs.pop('event time [utc]')

                kwargs.update({
                    self.primary_key: key,
                    't_start': start,
                    't_end': 'NaT',
                })

            elif k.endswith('_END') or k.endswith('_ASCE'):
                key, _ = key.rsplit('_', 1)  # pop `_END` and `_ASCE`
                stop = kwargs['event time [utc]']

                if key not in self.keys():
                    missing = row[i].replace('_END', '_START').replace('_ASCE', '_DESC')
                    warn.warning(
                        'Found `%s` (at %s) without `%s`.',
                        row[i], stop, missing
                    )
                    continue

                if isinstance(self[key], EventsList):
                    self[key][-1]['t_end'] = stop
                else:
                    self[key]['t_end'] = stop

                continue  # Go to the next row

            if key in self.keys():
                if not isinstance(self[key], EventsList):
                    self[key] = EventsList([self[key]])

                self[key].append(AbstractEvent(key, **kwargs))
            else:
                self[key] = AbstractEvent(key, **kwargs)

    @staticmethod
    def _read_csv(csv_text):
        """Read CSV file."""
        header, *lines = csv_text.splitlines()

        # Parse header columns
        fields = [
            field.lower().replace('#', '').strip() if field else f'column_{i}'
            for i, field in enumerate(header.split(','))
        ]

        # Strip rows content
        rows = [
            tuple(value.strip() for value in line.split(','))
            for line in lines
        ]

        return fields, rows

    @property
    def csv(self):
        """Formatted CSV content."""
        return Html(table(self.rows, header=self.fields))
