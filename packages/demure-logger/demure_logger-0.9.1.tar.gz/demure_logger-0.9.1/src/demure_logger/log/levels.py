from .exceptions import LevelDoesntExists, LogLevelsDigestReadOnlyExists
from typing      import Any
from functools   import total_ordering
from pydantic    import BaseModel

class LevelConstant:
    IGNORE = 0
    FATAL  = 1	
    ERROR  = 2
    WARN   = 3	
    INFO   = 4	
    DEBUG  = 5


@total_ordering
class Level:
    __name: str
    __value: int

    @classmethod
    def get_schema( cls ) -> BaseModel:
        class PDLevel( BaseModel ):
            name: str
            value: int

        return PDLevel
    
    def __init__( self, name: str, value: int ) :
        self.__name  = name
        self.__value = value

    def to_schema( self ) -> BaseModel:
        return self.__class__.get_schema( value=self.value, name=self.name )
    
    @property
    def name( self ) -> str: return self.__name

    @property
    def value( self ) -> int: return self.__value

    def __convert_other( self, other: Any ) -> int:
        if isinstance( other, Level ):
            return other.value
        elif isinstance( other, int ):
            return other
        else:
            raise TypeError( f"Can't compare Level with '{ type( other ) }'" )

    def __lt__( self, other: Any ) -> bool : return self.value <  self.__convert_other( other )  
    def __le__( self, other: Any ) -> bool : return self.value <= self.__convert_other( other )  
    def __eq__( self, other: Any ) -> bool : return self.value == self.__convert_other( other )  
    def __ne__( self, other: Any ) -> bool : return self.value != self.__convert_other( other )  
    def __gt__( self, other: Any ) -> bool : return self.value >  self.__convert_other( other )  
    def __ge__( self, other: Any ) -> bool : return self.value >= self.__convert_other( other )  

    def __repr__( self ) -> str:
        return self.name

    def __str__( self ) -> str:
        return self.__repr__( )

    def __bool__( self ) -> bool:
        return True


class Levels:
    def __getattr__( self, level: str ) -> Level:
        level = level.upper( )

        try:
            return Level( level, getattr( LevelConstant, level ) )
        except Exception as _:
            raise LevelDoesntExists( f"'{level}' doen't exists" ) 
   
    def __setattr__( cls, *_ ) -> int:
        raise LogLevelsDigestReadOnlyExists( "Log level digest is readonly class" ) 

    def __repr__( self ) -> str:
        return str( LevelConstant )

    def __str__( self ) -> str:
        return self.__repr__( )


Levels = Levels( )