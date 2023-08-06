from typing import Iterable, TypeVar, Callable


T = TypeVar( 'T' )


def indexof( iter: Iterable[T], elem: T, method: Callable[ [ T, T ], bool ]=lambda a, b: a == b ) -> int:
    index = -1

    for i, element in enumerate( iter ):
        if method( elem, element ):
            return i

    return index
