import inspect 

from typing           import Callable, Optional
from functools        import wraps
from ....types.simple import P
from .controller      import paint as _paint


def paint( text_color: str='RESET', background_color: str='RESET', style: Optional[str]=None ) -> Callable[ P, str ]:
    def _( func: Callable[ P, str ] ) -> Callable[ P, str ]: 
        @wraps( func )
        async def __async ( *args: P.args, **kwargs: P.kwargs ) -> str:
            result = await func( *args, **kwargs )

            return _paint( result, text_color, background_color, style )

        @wraps( func )
        def __( *args: P.args, **kwargs: P.kwargs ) -> str:
            result = func( *args, **kwargs )

            return _paint( result, text_color, background_color, style )
        
        return __async if inspect.iscoroutinefunction( func ) else __
    
    return _