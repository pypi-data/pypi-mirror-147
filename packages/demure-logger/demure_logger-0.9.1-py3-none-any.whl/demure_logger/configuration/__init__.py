import uuid

from ..utils.cls import ReadOnlyInstance
from typing      import Dict, TypeVar, Any, Type, Generic
from .exceptions import StaticAttributesIsRequired, InvalideValueType, AttributeIsRequired
from ..log       import Level


T = TypeVar( 'T' )


class Basic( ReadOnlyInstance ):
    def __init__( self, **kwargs: Dict[ str , any ] ):        
        annotation = getattr( self, '__annotations__', None ) 

        if annotation is None:
            raise StaticAttributesIsRequired( "You must set static attribute for configuration class" )
        else:
            super( ).__init__( False )

            for attr, _type in annotation.items( ):
                __default_value = str( uuid.uuid4( ) )

                if attr in kwargs:
                    if kwargs[attr] is not None:
                        if isinstance( kwargs[attr], _type ):
                            setattr( self, attr, kwargs[attr] )
                        else:
                            raise InvalideValueType( f"Valus is not '{_type}'" )
                    else:
                        setattr( self, attr, kwargs[attr] )
                elif getattr( self, attr, __default_value ) == __default_value:
                    raise AttributeIsRequired( f"{attr} is required" )
                else:
                    setattr( self, attr, getattr( self, attr ) )

        self.freeze( )



class Format( Basic ): ...
class Writer( Basic ): ...


class Constructor( Basic, Generic[T] ): 
    __constructor__  : str              
    props            : dict
    
    @classmethod
    def load_class_from_package( cls, path: str ) -> Type[T]:
        _   = path.split( "." )[-1]
        pkg = __import__( path.replace( "." + _, "" ), globals(), locals(), [ _ ], 0 )

        return getattr( pkg, _ )
        
    def build( self ) -> T:
        cls = self.__class__.load_class_from_package( self.__constructor__ )

        return cls( **self.props )