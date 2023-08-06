import os
import copy
import inspect
import pydantic

from .field        import Field, LogLevelField, NumberField, TextField
from typing        import TypeVar, Callable, List, Any, Optional, Iterable, overload, Dict, Generic
from .exceptions   import MessageWrongFieldType, FieldDoesntExists
from ..levels      import Levels, Level
from ...utils.list import indexof


T = TypeVar( 'T' )
PDModel = TypeVar ( 'PDModel', bound=pydantic.BaseModel )


def field_proxy( field: Field, name: str=None ) -> Field:
    if not isinstance( field, Field ):
        raise MessageWrongFieldType( "field must be child of Field" )                
    
    field.name = name if name is not None else field.name
    clone      = field.build( )

    return clone


class BasicMessage( object ):
    event   = LogLevelField( default=Levels.INFO )
    message = TextField    ( )

    __ordered__ : Iterable[Field]
    __columns__ : List[ Field ]
    __sort_by__ : Optional[ Iterable[str] | Callable[ [ Field ], int|str ] ] = None

    def __init__( self, 
        sort_by:  Optional[ Iterable[str] | Callable[ [ Field ], int|str ] ] = None,
        **columns_values ):
        self.__columns__ = [ ]

        if getattr( self, '__sort_by__' ) and self.__sort_by__ is not None:
            sort_by = getattr( self, '__sort_by__' )

        columns = [
            field_proxy( value, name ) 
            for name, value in inspect.getmembers( self, lambda attr: not inspect.isroutine( attr ) )
            if not name.startswith( '_' )
        ] 
        
        for column in columns:
            if column.name in columns_values.keys( ):
                column.value = columns_values.get( column.name )
            else:
                column.value = column.value

            self.__columns__.append( column )

            setattr( self, column.name, column )

        columns = [ column for column in self.__columns__ ]
        
        if sort_by is None:
            self.__ordered__ = columns
        else:
            if callable( sort_by ):
                self.__ordered__ = sorted( columns, key=sort_by )
            else:
                self.__ordered__ = sorted( columns, key=lambda column: indexof( sort_by, column.name ) )
    
    @property
    def __iter__( self ) -> List[Field[Any]]:
        return self.__ordered__.__iter__

    @property
    def __dict__( self ) -> Dict[ str, Field[Any] ]:
        return {
            column.name : column
            for column in self.__ordered__
        }
    
    @property
    def __jsonable__( self ) -> Dict[str, Any ]:
        return {
            column.name : column.__jsonable__
            for column in self.__ordered__
        }

    def __repr__( self ) -> str:
        return str( self.__ordered__ )

    def __str__( self ) -> str:
        return self.__repr__( )

    @overload
    def column( self, name: str ) -> T: ...
    
    @overload
    def column( self, name: str, value: T ) -> None: ...

    def column( self, *args ) -> None:
        names_collumns = [ column.name for column in self.__columns__ ]
        name           = args[0]

        if len( args ) == 1:
            if name in names_collumns:
                return getattr( self, name ).render( )
            else:
                raise FieldDoesntExists( f"'name' doesn't exists in line" )
        else:
            value          = args[1]
            names_collumns = [ column.name for column in self.__columns__ ]

            if name in names_collumns:
                getattr( self, name ).value = value
            else:
                raise FieldDoesntExists( f"'name' doesn't exists in line" )

    def set_event( self, event: Level ):
        for column in self.__ordered__:
            if isinstance( column, LogLevelField ):
                column.value = event

class Message( BasicMessage ): 
    pid = NumberField  ( default=os.getpid   )

