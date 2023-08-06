from typing    import TypeVar, Generic, List
from threading import Lock


T = TypeVar( 'T' )


class Queue( Generic[T] ):
    __data__  : List[T]
    __mutex__ : Lock

    def __init__( self, *args: List[T]):
        self.__data__  = list( *args )
        self.__mutex__ = Lock( )

    async def put( self, value: T ):
        self.__mutex__.acquire(1)

        self.__data__.append( value )

        self.__mutex__.release()

    async def pop( self ) -> T | None:
        self.__mutex__.acquire(1)

        value = None

        if len( self.__data__ ) > 0:
            value = self.__data__.pop( )

        self.__mutex__.release()

        return value
        
    @property
    def __iter__( self ) -> List[T]:
        return self.__data__.__iter__

    def __repr__( self ) -> str:
        return str( self.__data__ )