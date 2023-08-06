import re
import sys
import os 

from typing           import Dict, TextIO, List, Callable, Type, TypeVar, Any
from ..log            import Levels, Level
from .basic           import Handler as BasicHandler, Logger, Queue, Event, MessageDataType


T = TypeVar( 'T' )


class Handler( BasicHandler ):
    stream             : TextIO
    mapping            : Dict[ str, str ] | Callable[ [ MessageDataType ], Level ]
    default_event_type : Level

    def __init__( self, 
        stream  : TextIO           = sys.stdin,  
        mapping : Dict[ str, str ] | Callable[ [ MessageDataType ], Level ]= {
            'FATAL' : r'fatal|critical',
            'ERROR' : r'error',
            'WARN'  : r'warning|\bwarn\b',
            'DEBUG' : r'debug',
            'INFO'  : r''
        },
        default_event_type : Level        = Levels.debug,
        loggers            : List[Logger] = [],
        queue              : Queue[Event] = Queue( )
    ):
        super( ).__init__( loggers, queue )

        self.stream             = stream
        self.mapping            = mapping
        self.default_event_type = default_event_type

    def parse_event( self, message: MessageDataType ) -> Level:
        event = None

        if callable( self.mapping ):
            event = self.mapping( message ) 
        else:
            for event_type, regex in self.mapping.items( ):
                matched = re.findall( regex, message )

                if len( matched ) > 0:
                    event = getattr( Levels, event_type )
                    
                    break
            
        return event or self.default_event_type

    async def run( self, max_recursion: int = None ) : 
        async def _( ):
            message = self.stream.readline( )
           
            if len( message ) == 0:
                self.stop( )
            else:
                event = self.parse_event( message )
                
                await self.queue.put( Event( event, message.strip( ).replace( "\n", "" ) ) )
            
        self.event_updater = _

        await super( ).run( max_recursion )


class Config( dict ):
    loggers            : List[Logger]
    stream             : TextIO
    queue              : Queue[Event]
    mapping            : Dict[ str, str ] | Callable[ [ MessageDataType ], Level ]
    default_event_type : Level        

    @classmethod
    def from_module( cls: Type[T], mdl: Dict[ str, Any ] ) -> T:
        kwargs = cls()

        kwargs[ 'loggers' ] = getattr( mdl, 'loggers', [ ]       )
        kwargs[ 'stream'  ] = getattr( mdl, 'stream' , sys.stdin )

        if getattr( mdl, 'queue' , None ) is not None:
            kwargs['queue'] = getattr( mdl, 'queue', sys.stdin )
        
        if getattr( mdl, 'mapping' , None ) is not None:
            kwargs['mapping'] = getattr( mdl, 'mapping', sys.stdin )
    
        if getattr( mdl, 'default_event_type' , None ) is not None:
            kwargs['default_event_type'] = getattr( mdl, 'default_event_type', sys.stdin )
        
        return kwargs