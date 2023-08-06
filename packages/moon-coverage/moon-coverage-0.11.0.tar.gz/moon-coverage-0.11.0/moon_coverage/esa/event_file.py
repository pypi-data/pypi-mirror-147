"""ESA events files module."""

from ..events import EventsFile


class EsaMissionPhases(EventsFile):
    """ESA mission phases event file."""

    def __init__(self, fname):
        super().__init__(fname, primary_key='Name')


class EsaMissionTimeline(EventsFile):
    """ESA mission timeline event file."""

    def __init__(self, fname):
        super().__init__(fname, primary_key='Event Name')


class EsaMissionEvents(EventsFile):
    """Generic ESA mission events file.

    By default, a header is appended to the file with the
    following parameters:

    .. code-block:: text

        # name, t_start, t_end, subgroup, working_group

    but you can provide your own or set it to ``None`` is
    the first row is already the header.

    The primary key is also initialized at ``name`` but you
    can use any other column.

    """

    def __init__(
        self, fname,
        primary_key='name',
        header='# name, t_start, t_end, subgroup, working_group'
    ):
        super().__init__(fname, primary_key=primary_key, header=header)
