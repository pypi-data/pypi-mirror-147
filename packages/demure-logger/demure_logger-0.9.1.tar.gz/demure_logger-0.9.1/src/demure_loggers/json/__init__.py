import json

from typing            import TypeVar, Callable, Optional, List, Any, Dict
from ..file            import Logger as TextLoger
from .message          import Message
from .format           import Format
from .writer           import Writer
from demure_logger     import MessageDataType
from demure_logger.log import Level


MessageType = TypeVar( 'MessageType', bound=Message )
FormatType  = TypeVar( 'FormatType' , bound=Format  )
WriterType  = TypeVar( 'WriterType' , bound=Writer  )


class Logger( TextLoger ):
    def __init__( self, 
        writer       : Optional[ Callable[ ..., WriterType  ] | WriterType ] = None,
        format       : Callable[ ..., FormatType  ] | FormatType  = Format( ),
        message_class: Callable[ ..., MessageType ] | MessageType = Message,
        *args,
        **kwargs
    ):
        super( ).__init__( writer, format, message_class, *args, **kwargs ) 

    def _write( self, event: Level, *messages: List[MessageDataType] ) -> List[Message]:
        result = [ ]
 
        for message in messages:
            message = self.message_class( event=event, **message ) if isinstance( message, dict ) else self.message_class( event=event, message=message )

            if event <= self.level:
                self.event_hanler( event, message )
               
                def read_and_write( writer ):
                    state = writer.read( True )
                    state = { } if state is None or len( state ) == 0 else json.loads( state )

                    formated = self.format.prepare( message, state )
                    
                    writer.truncate( True )

                    writer.write( formated, True )

                self.writer.safe( read_and_write )

            result.append( message )

        return result