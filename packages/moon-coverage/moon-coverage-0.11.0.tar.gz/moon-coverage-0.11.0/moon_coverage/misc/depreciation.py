"""Depreciation decorator."""

from functools import wraps
from inspect import getmro

from .logger import logger


warn, _ = logger('DepreciationWarning')


def depreciated_renamed(cls):
    """Depreciation renamed class decorator."""

    @wraps(cls, updated=())
    class DeprecationRenamed(cls):
        """Depreciation renamed class."""

        def __init__(self, *args, **kwargs):
            warn.warning('`%s` has been renamed `%s`. '
                         'Please update your code to use this new denomination.',
                         cls.__name__, getmro(cls)[1].__name__)

            super().__init__(*args, **kwargs)
            self.__doc__ = '[Depreciated] ' + self.__doc__

    return DeprecationRenamed


def depreciated_replaced(func):
    """Depreciation replaced function decorator."""

    @wraps(func)
    def wrapper(_self, *args, **kwargs):
        """Depreciation replaced function."""
        if not (func.__name__ == '__getattr__' and args and args[0].startswith('_')):
            warn.warning('`%s` has been replaced by `%s`. '
                         'Please update your code to use this new denomination.',
                         _self.old_name, _self.new_name)

        return func(_self, *args, **kwargs)

    return wrapper


class DeprecationHelper:
    """Depreciation helper.

    Parameters
    ----------
    old_name: str
        Original object name.
    new_name: str
        New object name.
    new_target: object
        New object target.

    """

    def __init__(self, old_name, new_name, new_target):
        self.old_name = old_name
        self.new_name = new_name
        self.new_target = new_target

    @depreciated_replaced
    def __repr__(self):
        return repr(self.new_target)

    @depreciated_replaced
    def __call__(self, *args, **kwargs):
        return self.new_target(*args, **kwargs)

    @depreciated_replaced
    def __getitem__(self, item):
        return self.new_target[item]

    @depreciated_replaced
    def __getattr__(self, attr):
        return getattr(self.new_target, attr)

    @depreciated_replaced
    def __contains__(self, item):
        return item in self.new_target
