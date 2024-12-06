#  type: ignore
"""
typedload

You should not import this module before python3.12

It is meant to deal with TypeAliasType defined in PEP 695.
"""

# Copyright (C) 2024 Salvo "LtWorf" Tomaselli
#
# typedload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

from functools import lru_cache
from typing import TypeAliasType, Union, List, Set, Tuple, FrozenSet
from .typechecks import *


__all__ = [
    'unalias'
]


def is_alias(t) -> bool:
    '''
    It returns true if the type is an alias
    '''
    return isinstance(t, TypeAliasType)


@lru_cache
def unalias(t):
    '''
    It tries to resolve the alias.

    For example

    type i = tuple[list[int | float], ...]

    will be converted into the actual

    Tuple[List[Union[int, float]], ...]

    that is possible to match with type handlers.
    '''
    # Resolve all nested stuff (hopefully)
    if is_union(t):
        args = [unalias(i) for i in t.__args__]
        t = Union[*args]
    elif is_list(t):
        t = List[unalias(t.__args__[0])]
    elif is_set(t):
        t = Set[unalias(t.__args__[0])]
    elif is_tuple(t):
        args = [unalias(i) for i in t.__args__]
        t = Tuple[*args]
    elif is_frozenset(t):
        t = FrozenSet[unalias(t.__args__[0])]
    elif is_alias(t):
        t = unalias(t.__value__)

    return t
