"""ESA specific module."""

from .api import debug_esa_api, get_mk, get_tag
from .crema import ESA_CREMAS, JUICE_CREMAS, EsaCremasCollection
from .event_file import EsaMissionEvents, EsaMissionPhases, EsaMissionTimeline
from .export import export_timeline
from ..misc import DeprecationHelper
from ..spice import MetaKernel


__all__ = [
    'ESA_CREMAS',
    'JUICE_CREMAS',
    'EsaCremasCollection',
    'EsaMissionEvents',
    'EsaMissionPhases',
    'EsaMissionTimeline',
    'export_timeline',
    'get_mk',
    'get_tag',
    'debug_esa_api',
]


# Depreciations
CReMAs = DeprecationHelper('CReMAs', 'ESA_CREMAS', ESA_CREMAS)
JUICE_CReMA = DeprecationHelper('JUICE_CReMA', 'JUICE_CREMAS', JUICE_CREMAS)
CReMAMetaKernel = DeprecationHelper('CReMAMetaKernel', 'MetaKernel', MetaKernel)
debug_esa_crema = DeprecationHelper('debug_esa_crema', 'debug_esa_api', debug_esa_api)
