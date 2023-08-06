"""ESA CReMA module."""

from .api import get_mk, get_tag
from ..misc import cached_property


class EsaCremasCollection:
    """ESA Consolidated Report on Mission Analysis (CReMA) metakernel.

    Parameters
    ----------
    mission: str
        Name of the mission.
    doi: str, optional
        DOI of the dataset.

    """

    def __init__(self, mission, doi=None):
        self.mission = mission.lower()
        self.doi = doi

    def __str__(self):
        return f'{self.mission.title()}CremaCollection'

    def __repr__(self):
        n = len(self)
        if n == 0:
            mks = 'No metakernel is available.'
        else:
            mks = '\n - '.join([
                f'{n} metakernel' + ('s are ' if n > 1 else ' is ') + 'available:',
                *self.mks
            ])

        return f'<{self}> Latest version: {self.latest} | {mks} '

    def __len__(self):
        return len(self.mks)

    def __iter__(self):
        return iter(self.mks)

    def __contains__(self, other):
        return other in self.mks

    def __getitem__(self, item):
        """Get a single metakernel for the latest or a specific version."""
        if isinstance(item, (int, float, str)):
            return get_mk(self.mission, mk=str(item), version=self.latest)

        if isinstance(item, tuple) and len(item) == 2:
            mk, version = item
            return get_mk(self.mission, mk=str(mk), version=version)

        raise KeyError('You need to provide a `mk` key (with an optional `version` key).')

    @cached_property
    def latest(self) -> str:
        """Latest version."""
        return get_tag(self.mission, version='latest')

    @property
    def versions(self) -> list:
        """Get all the releases available for a given mission."""
        return get_tag(self.mission, version='all')

    def version(self, version) -> list:
        """List of all the metakernels for a given version."""
        return get_mk(self.mission, mk='all', version=version)[::-1]

    @cached_property
    def mks(self) -> list:
        """List of all the latest metakernels."""
        return self.version(self.latest)


# Default ESA CReMAs
JUICE_CREMAS = EsaCremasCollection('JUICE', doi='10.5270/esa-ybmj68p')

ESA_CREMAS = {
    'JUICE': JUICE_CREMAS,
}
