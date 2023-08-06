"""Event module."""

import re
from collections import UserDict, UserList
from operator import attrgetter

import numpy as np

from ..html import table


def date(numpy_datetime64) -> str:
    """Extract date from numpy.datetime64 as a string."""
    return 'NaT' if np.isnat(numpy_datetime64) else str(numpy_datetime64.item().date())


TIMEDELTA = re.compile(
    r'(?P<value>\d+)\s?(?P<unit>millisecond|month|ms|[smhHdDMyY])s?'
)

NP_TIMEDELTA_UNITS = {
    'millisecond': 'ms',
    'H': 'h',
    'd': 'D',
    'month': 'M',
    'y': 'Y',
}


def timedelta(step):
    """Parse step as :class:`numpy.timedelta64` object.

    The value must be a :obj:`int` followed by an optional
    space and a valid unit.

    Examples of valid units:

    - ``ms``, ``msec``, ``millisecond``
    - ``s``, ``sec``, ``second``
    - ``m``, ``min``, ``minute``
    - ``h``, ``hour``
    - ``D``, ``day``
    - ``M``, ``month``
    - ``Y``, ``year``

    Parameters
    ----------
    step: str
        Step to parse.

    Returns
    -------
    numpy.timedelta64
        Parsed numpy.timedelta64 step.

    Raises
    ------
    ValueError
        If the provided step format or unit is invalid.

    """
    if isinstance(step, np.timedelta64):
        return step

    match = TIMEDELTA.match(step)

    if not match:
        raise ValueError(f'Invalid step format: `{step}`')

    value, unit = match.group('value', 'unit')
    return np.timedelta64(int(value), NP_TIMEDELTA_UNITS.get(unit, unit))


class AbstractEvent(UserDict):
    """Single time event object."""
    def __init__(self, key, *args, **kwargs):
        self.key = key

        if 'contextual info' in kwargs:
            infos = kwargs.pop('contextual info')
            if infos:
                for info in infos.split(';'):
                    key, value = info.split('=', 1)
                    kwargs[key.strip()] = value.strip()

        super().__init__(*args, **kwargs)

        if 't_start' in self and 't_end' in self:
            self.__class__ = EventWindow

        elif 'event time [utc]' in self:
            self.__class__ = Event

        else:
            raise ValueError(f'Event time was not found: {kwargs}')

    def __repr__(self):
        return '\n - '.join([
            f'<{self.__class__.__name__}> {self}:',
            *[f'{k}: {v}' for k, v in self.items()]
        ])

    def _repr_html_(self):
        return table(list(self.items()))

    def _ipython_key_completions_(self):
        return self.keys()

    def __contains__(self, utc):
        if isinstance(utc, str) and utc in self.data.keys():
            return True

        try:
            return self.contains(utc).any()
        except ValueError:
            return False

    def __hash__(self):
        return hash(frozenset(self.items()))

    def __add__(self, other):
        """Add to stop time."""
        return self.stop + timedelta(other)

    def __sub__(self, other):
        """Substract from start time."""
        return self.start - timedelta(other)

    def __gt__(self, other):
        return self.start > np.datetime64(str(other))

    def __ge__(self, other):
        return self.start >= np.datetime64(str(other))

    def __lt__(self, other):
        return self.stop < np.datetime64(str(other))

    def __le__(self, other):
        return self.stop <= np.datetime64(str(other))

    @property
    def start(self) -> np.datetime64:
        """Event start time."""
        raise NotImplementedError

    @property
    def stop(self) -> np.datetime64:
        """Event stop time."""
        raise NotImplementedError

    @property
    def start_date(self):
        """Event start date."""
        return date(self.start)

    @property
    def stop_date(self):
        """Event stop date."""
        return date(self.stop)

    def contains(self, pts):
        """Check if points are inside the temporal windows.

        Parameters
        ----------
        pts: numpy.ndarray
            List of temporal UTC point(s): ``utc`` or ``[utc_0, …]``.
            If an object with :attr:`utc` attribute/property is provided,
            the intersection will be performed on these points.

        Returns
        -------
        numpy.ndarray
            Return ``True`` if the point is inside the pixel corners, and
            ``False`` overwise.

        Note
        ----
        If the point is on the edge of the window it will be included.

        """
        if hasattr(pts, 'utc'):
            return self.contains(pts.utc)

        if isinstance(pts, str):
            return self.contains(np.datetime64(pts))

        if isinstance(pts, (list, tuple)):
            return self.contains(np.array(pts).astype('datetime64'))

        return (self.start <= pts) & (pts <= self.stop)


class Event(AbstractEvent):
    """Single time event object."""

    def __str__(self):
        return f'{self.key} ({self.start_date})'

    @property
    def start(self) -> np.datetime64:
        """Event start time."""
        return np.datetime64(self['event time [utc]'].replace('Z', ''))

    @property
    def stop(self) -> np.datetime64:
        """Event stop time (same as start time)."""
        return self.start


class EventWindow(AbstractEvent):
    """Window time event object."""

    def __str__(self):
        return f'{self.key} ({self.start_date} -> {self.stop_date})'

    @property
    def start(self) -> np.datetime64:
        """Event start time."""
        return np.datetime64(self['t_start'].replace('Z', ''))

    @property
    def stop(self) -> np.datetime64:
        """Event stop time."""
        return np.datetime64(self['t_end'].replace('Z', ''))


class AbstractEventsCollection:
    """Abstract collection of events."""

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __contains__(self, utc):
        try:
            return self.contains(utc).any()
        except ValueError:
            return False

    def __hash__(self):
        raise NotImplementedError

    def _filter(self, func, err_msg):
        """Comparison filter."""
        elements = []
        for event in self:
            if isinstance(event, AbstractEventsCollection):
                try:
                    elements.append(func(event))
                except LookupError:
                    pass
            elif func(event):
                elements.append(event)

        if elements:
            if len(elements) == 1:
                return elements[0]

            if isinstance(self, EventsList):
                return EventsList(elements)

            return EventsDict(elements)

        raise LookupError(err_msg)

    def __gt__(self, other):
        return self._filter(
            lambda event: event > other, f'{self} <= {other}'
        )

    def __ge__(self, other):
        return self._filter(
            lambda event: event >= other, f'{self} < {other}'
        )

    def __lt__(self, other):
        return self._filter(
            lambda event: event < other, f'{self} >= {other}'
        )

    def __le__(self, other):
        return self._filter(
            lambda event: event <= other, f'{self} > {other}'
        )

    @property
    def starts(self) -> list:
        """Event start times."""
        return [event.start for event in self]

    @property
    def stops(self) -> list:
        """Event stop times."""
        return [event.stop for event in self]

    @property
    def windows(self) -> list:
        """Event windows."""
        return [(event.start, event.stop) for event in self]

    @property
    def start(self) -> np.datetime64:
        """Global events start time."""
        return min(self.starts)

    @property
    def stop(self) -> np.datetime64:
        """Global events stop time."""
        return max(self.stops)

    @property
    def start_date(self):
        """global events start date."""
        return date(self.start)

    @property
    def stop_date(self):
        """Global events stop date."""
        return date(self.stop)

    def contains(self, pts):
        """Check if points are inside any temporal window.

        Parameters
        ----------
        pts: numpy.ndarray
            List of temporal UTC point(s): ``utc`` or ``[utc_0, …]``.
            If an object with :attr:`utc` attribute/property is provided,
            the intersection will be performed on these points.

        Returns
        -------
        numpy.ndarray
            Return ``True`` if the point is inside the pixel corners, and
            ``False`` overwise.

        Note
        ----
        If the point is on the edge of the window it will be included.

        """
        return np.any([event.contains(pts) for event in self], axis=0)

    def before(self, date_stop, strict=False):
        """Select all the events before the given date."""
        return self < date_stop if strict else self <= date_stop

    def after(self, date_start, strict=False):
        """Select all the events after the given date."""
        return self > date_start if strict else self >= date_start

    def between(self, date_start, date_stop, strict=False):
        """Select all the events between the given dates.

        Danger
        ------
        The parenthis in the comparison are mandatory here.
        Comparison operator chains (``a < b < c``) will break
        due to short-circuit chain evaluation (``a < b and b < c``)
        where only ``a < b`` if the result is not `False` and
        ``b < c`` otherwise, not the intersection (``(a < b) & (b < c)``).

        """
        return (date_start < self) < date_stop if strict else \
            (date_start <= self) <= date_stop


class EventsDict(AbstractEventsCollection, UserDict):
    """List of events items with different keys.

    Warning
    -------
    The iteration is performed on the values and not the dict keys.

    """

    def __init__(self, events, **kwargs):
        self.data = {
            event.key: event
            for event in sorted(events, key=attrgetter('start'))
        }

    def __str__(self):
        n_events = len(self)
        events = f'{n_events} key' + ('s' if n_events > 1 else '')

        if n_events > 0:
            events = f'({date(self.start)} -> {date(self.stop)} | {events})'

            events += '\n - '.join([':', *[
                str(event) for event in self
            ]])

        return events

    def _repr_html_(self):
        rows = [
            [
                f'<em>{i}</em>',
                event.key,
                len(event) if isinstance(event, AbstractEventsCollection) else '-',
                event.start_date,
                event.stop_date,
            ]
            for i, event in enumerate(self)
        ]
        return table(rows, header=('', 'event', '#', 't_start', 't_stop'))

    def __iter__(self):
        return iter(self.data.values())

    def __getitem__(self, key):
        if isinstance(key, str) and key in self.keys():
            return self.data[key]

        if isinstance(key, int):
            return self.get_by_int(key)

        if isinstance(key, slice):
            return EventsDict(self.get_by_slice(key))

        if isinstance(key, tuple):
            return self.find(*key)

        return self.find(key)

    def _ipython_key_completions_(self):
        return self.keys()

    def __contains__(self, utc):
        if isinstance(utc, str) and utc in self.data.keys():
            return True

        return super().__contains__(utc)

    def __hash__(self):
        return hash(frozenset(self.data.items()))

    def keys(self):
        """Dictionnary keys."""
        return self.data.keys()

    def get_by_slice(self, key) -> list:
        """Get events by slice."""
        return list(self)[key]

    def get_by_int(self, key: int):
        """Get event by int."""
        if -len(self) <= key < len(self):
            return self.get_by_slice(key)

        raise IndexError('Event index out of range')

    def find(self, *regex):
        """Find the events matching a regex expression.

        Parameters
        ----------
        *regex: str
            Search regex expression key(s).

        Raises
        ------
        KeyError
            If none of the provided key was found.

        Note
        ----
        When multiple keys are provided, the duplicates
        will be discarded.

        """
        # Duplicates are removed with the set()
        res = list({
            event
            for expr in regex
            for key, event in self.data.items()
            if re.search(expr, key, flags=re.IGNORECASE)
        })

        if not res:
            raise KeyError(f'`{"`, `".join(regex)}` not found')

        return res[0] if len(res) == 1 else EventsDict(res)

    def startswith(self, *keys):
        """Find the events starting with a given key

        Parameters
        ----------
        *keys: str
            Search expression key(s).

        """
        return self.find(*[f'^{key}' for key in keys])

    def endswith(self, *keys):
        """Find the events ending with a given key

        Parameters
        ----------
        *keys: str
            Search expression key(s).

        """
        return self.find(*[f'{key}$' for key in keys])


class EventsList(AbstractEventsCollection, UserList):
    """List of events with the same key."""

    def __str__(self):
        return (
            f'{self.key} ({self.start_date} -> {self.stop_date} | {len(self)} events)'
        )

    def _repr_html_(self):
        return table([
            [f'<em>{i}</em>'] + list(event.values())
            for i, event in enumerate(self)
        ], header=('', *self[0]))

    def __getitem__(self, item):
        """Items can be queried by index or flyby crema name."""
        if isinstance(item, str):
            keys = self.crema_names
            if item not in keys:
                raise KeyError(f'Unknown flyby: `{item}`')
            return self[keys.index(item)]

        if isinstance(item, slice):
            return EventsList(self.data[item])

        if isinstance(item, tuple):
            return EventsList([self[i] for i in item])

        return self.data[item]

    def _ipython_key_completions_(self):
        return self.crema_names

    def __hash__(self):
        return hash(tuple(self.data))

    @property
    def key(self):
        """Events key."""
        return getattr(self[0], 'key', None)

    @property
    def crema_names(self) -> list:
        """Crema names when present in contextual info field."""
        return [item.get('Crema name') for item in self]
