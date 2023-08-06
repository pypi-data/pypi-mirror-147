from typing                      import TypeVar, Callable, Optional, List, Any, Dict
from demure_logger               import BasicLogger
from demure_logger.configuration import Constructor
from .message                    import Message
from demure_logger.format.text   import Format
from .writer                     import Writer, WriterPath, WriterStream 
from demure_logger.log           import Levels


MessageType = TypeVar( 'MessageType', bound=Message )
FormatType  = TypeVar( 'FormatType' , bound=Format  )
WriterType  = TypeVar( 'WriterType' , bound=Writer  )

class Logger( BasicLogger ):
    def __init__( self, 
        writer       : Optional[ Callable[ ..., WriterType  ] | WriterType ] = None,
        format       : Callable[ ..., FormatType  ] | FormatType  = Format( ),
        message_class: Callable[ ..., MessageType ] | MessageType = Message,
        path         : Optional[ WriterPath   ] = None,
        stream       : Optional[ WriterStream ] = None,
        *args,
        **kwargs
    ):
        if writer is None:
            writer = Writer( path, stream )
        elif stream is not None:
            writer.stream = stream
        elif path is not None:
            writer.path = path

        super( ).__init__( writer, format, message_class, *args, **kwargs ) 

    @classmethod
    def convert_config( cls, config: Dict[ str, Any ] ) -> Dict[ str, Any ]:
        writer        = config.get( "writer", { } )
        format        = config.get( "format", { } )
        message_class = config.get( "message_class", "demure_loggers.file.message.Message" )

        if writer.get( '__constructor__', None ) is None:
            writer['__constructor__'] = "demure_loggers.file.writer.Writer"
        
        if writer.get( 'props', None ) is None:
            writer['props'] = { }
        
        if format.get( '__constructor__', None ) is None:
            format['__constructor__'] = "demure_logger.format.text.Format"
        
        if format.get( 'props', None ) is None:
            format['props'] = { }
        
        cfg = dict(
            name          = config.get( "name", f"{cls.__class__.__name__.lower( )}-{cls.count}" ),
            level         = getattr( Levels, config.get( "level" ) ) if "level" in config else Levels.DEBUG,
            writer        = Constructor[WriterType]( **writer ).build( ),
            format        = Constructor[FormatType]( **format ).build( ),
            message_class = Constructor.load_class_from_package( message_class ) 
        )

        if config.get( "event_handler", None ) is not None:
            cfg['event_handler'] = Constructor.load_class_from_package( cfg['event_handler'] )

        return { **config, **cfg }