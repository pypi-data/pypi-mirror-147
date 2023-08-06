from typing import TypeVar, List, Callable, Any


T = TypeVar( 'T' )
V = TypeVar( 'V' )


def read_only_class( cls: T ) -> T:
    class Wraped( cls ):
        def __setattr__( self, _: str ) -> None:
            raise AttributeError( "Attributes is read only" )

    return Wraped


class ReadOnlyInstance( object ):
    __frozen: bool

    def __init__( self, frozen: bool = True ):
        self.__frozen__ = frozen
        
        super( ).__init__( )
    
    def freeze( self ):
        self.__frozen__ = True
    
    def unfreeze( self ):
        self.__frozen__ = False

    def __setattr__( self, attr: str, value: Any ) -> None:
        if attr == '__frozen__':
            super( ).__setattr__( '__frozen__', value )
        elif not self.__frozen__:
            super( ).__setattr__( attr, value )
        else:
            raise AttributeError( f"Attributes '{attr}' is read only" )