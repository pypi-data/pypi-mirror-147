from ..             import BasicFormat
from ...log.message import Message
from typing         import Optional


class Format( BasicFormat[str] ):
    format: Optional[str]

    def __init__( self, format: Optional[str] = None ):
        self.format = format

    def prepare( self, message: Message ) -> str:
        if self.format is None:
            fmt = "\t".join( [ "{}" for _ in range( len( message.__dict__.keys( ) ) ) ] )
            
            return fmt.format( *[ i for i in message ] )
        else:
            return self.format.format( **message.__dict__ )
                            
    def __call__( self, message: Message ) -> str:
        return self.prepare( message )