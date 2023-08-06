class ColorExceptionBasic( Exception ):
    def __init__( self, color: str, message: str ):
        super( ).__init__( f"'{ color.capitalize( ) }' { message }" )


class DoesntExists( ColorExceptionBasic ): 
    def __init__( self, code: str ):
        super( ).__init__( code, "Doesn't exists" )
    

class ColorDoesntExists( DoesntExists ): ...
class StyleDoesntExists( DoesntExists ): ...