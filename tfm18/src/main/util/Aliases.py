from typing import Type

# Original package name is Orange3
import Orange.data.table
import collections.abc

OrangeTable: Type[Orange.data.table.Table] = Orange.data.table.Table
Function: Type[collections.abc.Callable] = collections.abc.Callable
Function.__doc__ = \
    """Function type; Function[[int], str] is a function of (int) -> str.

    The subscription syntax must always be used with exactly two
    values: the argument list and the return type.  The argument list
    must be a list of types or ellipsis; the return type must be a single type.

    There is no syntax to indicate optional or keyword arguments,
    such function types are rarely used as callback types.
    """