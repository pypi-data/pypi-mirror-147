from typing          import Generic, TypeVar
from ..log.message   import Message
from ..configuration import Format as Configuration


T = TypeVar( 'T' )


class BasicFormat( Generic[T] ):
    def __call__( self, message: Message ) -> T: ...

    @classmethod
    def from_configuration( cls, config: Configuration ):
        return cls.__init__( **config.__dict__ )