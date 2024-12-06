from __future__ import annotations

import inspect
import logging
import sys
import warnings
from collections.abc import Callable, MutableMapping
from contextlib import contextmanager
from importlib import import_module
from types import ModuleType
from typing import Dict, Optional, Union, Any, Hashable, TypeVar
from unittest.mock import MagicMock


@contextmanager
def all_logging_disabled(highest_level=logging.CRITICAL):
    """
    A context manager that will prevent any logging messages
    triggered during the body from being processed.
    :param highest_level: the maximum logging level in use.
    This would only need to be changed if a custom level greater than CRITICAL
    is defined.

    https://gist.github.com/simon-weber/7853144
    """
    # two kind-of hacks here:
    #    * can't get the highest logging level in effect => delegate to the user
    #    * can't get the current module-level override => use an undocumented
    #       (but non-private!) interface

    previous_level = logging.root.manager.disable

    logging.disable(highest_level)

    try:
        yield
    finally:
        logging.disable(previous_level)


@contextmanager
def filter_warnings(action, category=Warning, lineno=0, append=False, *,
                    record=False, module=None):
    """A context manager that combines catching and filtering warnings."""
    with warnings.catch_warnings(record=record, module=module) as manager:
        warnings.simplefilter(action, category, lineno, append)
        try:
            yield manager
        finally:
            pass


@contextmanager
def key_set_to(dct: MutableMapping, key: Hashable, val: Any):
    """Temporarily set `key` in `dct` to `val`.

    Examples
    --------
    >>> my_dict = {'a': 2, 3: 'b'}
    >>> my_dict['a']
    2
    >>> with key_set_to(my_dict, 'a', 3):
    ...     print(my_dict['a'])
    3
    >>> my_dict['a']
    2

    Also works with previously nonexisting keys:

    >>> with key_set_to(my_dict, 1, 2):
    ...     print(my_dict[1])
    2
    >>> 1 in my_dict
    False

    """
    missing_sentinel = object()
    previous = dct.get(key, missing_sentinel)

    try:
        dct[key] = val
        yield dct
    finally:
        try:
            if previous is missing_sentinel:
                del dct[key]
            else:
                dct[key] = previous
        except:
            pass


@contextmanager
def attr_set_to(obj: Any, attr: str, val: Any, allow_missing: bool = False):
    """Temporarily set `attr` in `obj` to `val`.

    If `allow_missing` is `True`, `attr` will also be set if it did not
    exist before.

    Examples
    --------
    >>> class Foo:
    ...     a = 3
    >>> foo = Foo()
    >>> foo.a
    3
    >>> with attr_set_to(foo, 'a', 4):
    ...     print(foo.a)
    4
    >>> foo.a
    3
    >>> with attr_set_to(foo, 'b', 1, allow_missing=True):
    ...     print(foo.b)
    1
    >>> hasattr(foo, 'b')
    False

    """
    missing_sentinel = object()
    try:
        previous = getattr(obj, attr)
    except AttributeError:
        if allow_missing:
            previous = missing_sentinel
        else:
            raise

    try:
        setattr(obj, attr, val)
        yield obj
    except AttributeError:
        raise
    finally:
        try:
            if previous is missing_sentinel:
                delattr(obj, attr)
            else:
                setattr(obj, attr, previous)
        except:
            pass


def import_or_mock(
        name: str, package: Optional[str] = None, local_name: Optional[str] = None
) -> Dict[str, Union[ModuleType, MagicMock]]:
    """Imports a module or, if it cannot be imported, mocks it.

    If it is importable, equivalent to::
        from name import package as local_name

    Parameters
    ----------
    name : str
        See :func:`importlib.import_module`.
    package : str | None
        See :func:`importlib.import_module`.
    local_name : str
        Either the name assigned to the module or the object to be
        imported from the module.

    Returns
    -------
    dict[str, ModuleType | MagicMock]
        A dictionary with the single entry {local_name: module}.

    Examples
    --------
    >>> locals().update(import_or_mock('numpy', None, 'pi'))
    >>> pi
    3.141592653589793
    >>> locals().update(import_or_mock('owiejlkjlqz'))
    >>> owiejlkjlqz
    <MagicMock name='mock.owiejlkjlqz' id='...'>

    """
    local_name = local_name or name
    try:
        module = import_module(name, package)
    except ImportError:
        module = MagicMock(__name__=name)
    return {local_name: getattr(module, local_name, module)}
