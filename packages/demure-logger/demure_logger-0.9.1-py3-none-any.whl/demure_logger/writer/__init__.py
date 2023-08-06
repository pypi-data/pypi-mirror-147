from typing          import TypeVar, Generic, List
from ..configuration import Writer as Config


T = TypeVar( 'T' )


class BasicWriter( Generic[T] ):
    def write( self, message: T ) -> None: ...

    def __call__( self, *messages: List[T] ) -> None: 
        for message in messages:
            self.write( message )
    
    @classmethod
    def from_config( cls, config: Config ):
        return cls.__init__( **config.__dict__ )
