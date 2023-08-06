from typing                           import Optional, TypeVar, Callable, Generic, get_args
from datetime                         import datetime 
from demure_logger.log                import Level
from demure_logger.log.message        import field
from demure_logger.format.text.colors import controller as color
from demure_logger.types              import get_parent_type_parameter


T = TypeVar( 'T', bound=field.Field )


def fabric( cls: field.Field ) -> T:
    class Field( cls ): 
        color      : Optional[str] | Callable[ [ T ], Optional[str] ]
        background : Optional[str] | Callable[ [ T ], Optional[str] ]
        style      : Optional[str] | Callable[ [ T ], Optional[str] ]
        
        def __init__( self, 
            color      : Optional[str]=None,
            background : Optional[str]=None,
            style      : Optional[str]=None,
            **kwargs )  :
            super( ).__init__( **kwargs )

            self.color      = color
            self.background = background
            self.style      = style

        def __repr__( self ) -> str:
            kwargs = dict( content=str( self.value ) )
            
            if self.color:
                kwargs['text_color'] = self.color( self.value ) if callable( self.color ) else self.color
            
            if self.style:
                kwargs['style'] = self.style( self.value ) if callable( self.style ) else self.style

            if self.background:
                kwargs['background_color'] = self.background( self.value ) if callable( self.background ) else self.background
            
            return color.paint( **kwargs )
            
    return Field 


TextField     = fabric( field.TextField     )
DatetimeField = fabric( field.DatetimeField )
NumberField   = fabric( field.NumberField   )
LogLevelField = fabric( field.LogLevelField )

