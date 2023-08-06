import inspect

from .writer        import BasicWriter
from .format        import BasicFormat
from typing         import TypeVar, Type, Dict, Any, Callable, ParamSpec, List, Tuple, Optional
from .log           import BasicMessage
from .log.levels    import Levels, Level
from functools      import wraps
from .configuration import Basic as Config


Level    = TypeVar  ( 'Level'  , bound=Level         )
Writer   = TypeVar  ( 'Writer' , bound=BasicWriter   )
Format   = TypeVar  ( 'Format' , bound=BasicFormat   ) 
Message  = TypeVar  ( 'Message', bound=BasicMessage  )
Logger   = TypeVar  ( 'Logger' , bound='BasicLogger' )
T        = TypeVar  ( 'T' )
P        = ParamSpec( 'P' )
R        = TypeVar  ( 'R' )


def call_if_callable( instance: Callable[ ..., T ] | T, *args, **kwargs ) -> T:
    if inspect.isfunction( instance ):
        return instance( *args, **kwargs )
    else:
        return instance

MessageDataType = Dict[ str, Any ] | str


class BasicLogger:
    count: int = 0

    _writer        : Writer        | Callable[ ..., Writer        ]
    _format        : Format        | Callable[ ..., Format        ]
    _message_class : Type[Message] | Callable[ ..., Type[Message] ]
    _level         : Level
    
    def __init__( self, 
        writer        : Writer        | Callable[ ..., Writer        ],
        format        : Format        | Callable[ ..., Format        ],
        message_class : Type[Message] | Callable[ ..., Type[Message] ],
        level         : Level                               =Levels.debug,
        name          : Optional[str] = None,
        event_hanler  : Callable[ [ Level, Message ], None ]=lambda level, message: ...
    ):
        self.name           = self.__class__.__name__ if name is None else name
        self._writer        =  writer                
        self._format        =  format                 
        self._message_class =  message_class 

        self.level        = level
        self.event_hanler = event_hanler

        self.__class__.count += 1
    
    @property
    def writer( self ) -> Writer: return call_if_callable( self._writer )

    @property
    def format( self ) -> Format: return call_if_callable( self._format )

    @property
    def message_class( self ) -> Type[Message]: return call_if_callable( self._message_class )

    def _write( self, event: Level, *messages: List[MessageDataType] ) -> List[Message]:
        result = [ ]
 
        for message in messages:
            message = self.message_class( event=event, **message ) if isinstance( message, dict ) else self.message_class( event=event, message=message )
          
            if event <= self.level:
                formated = self.format.prepare( message )
                
                self.event_hanler( event, message )
                
                self.writer.write( formated )
            
            result.append( message )

        return result

    def off( self ):
        self.level = Levels.IGNORE

    def fatal( self, *messages: List[MessageDataType] ):
        return self._write( Levels.fatal, *messages )
    
    def error( self, *messages: List[MessageDataType] ):
        return self._write( Levels.error, *messages )

    def warn( self, *messages: List[MessageDataType] ):
        return self._write( Levels.warn, *messages )

    def info( self, *messages: List[MessageDataType] ):
        return self._write( Levels.info, *messages )

    def debug( self, *messages: List[MessageDataType] ):
        return self._write( Levels.debug, *messages )

    def fatal( self, *messages: List[MessageDataType] ):
        return self._write( Levels.fatal, *messages )

    def decorate( self, 
        *args: Tuple[ Level, Callable[ [ Type[Callable] ], str ] ] | Tuple[ Callable[ P, R ] ]
    ):
        event       = Levels.debug
        func_format = lambda f: f.__name__ 

        if len( args ) > 1 or not callable( args[0] ):
            if len( args ) > 0 and args[0] is not None: event       = args[0]
            if len( args ) > 1 and args[1] is not None: func_format = args[1]

        def wrap( func: Callable[ P, R ] ) -> Callable[ P, R ]:
            formated = func_format( func )

            @wraps( func )
            def __( *args: P.args, **kwargs: P.kwargs ) -> R:
                self._write( event, f"start {formated}" )
                
                result = func( *args, **kwargs )

                self._write( event, f"end {formated}" )

                return result

                        
            @wraps( func )
            async def __async( *args: P.args, **kwargs: P.kwargs ) -> R:
                self._write( event, f"start async {formated}" )
                
                result = await func( *args, **kwargs )

                self._write( event, f"end async {formated}" )

                return result

            return __async if inspect.iscoroutinefunction( func ) else __
        
        return wrap( args[0] ) if len( args ) == 1 and callable( args[0] ) else wrap

    def catch( self, 
        *args: Tuple[ Level, Callable[ [ Exception ], str ] ] | Tuple[ Callable[ P, R ] ]
    ):
        event        = Levels.warn
        error_format = lambda error: f"{error}" 

        if len( args ) > 1 or not callable( args[0] ):
            if len( args ) > 0 and args[0] is not None: event        = args[0]
            if len( args ) > 1 and args[1] is not None: error_format = args[1]

        def wrap( func: Callable[ P, R ] ) -> Callable[ P, R ]:
            @wraps( func )
            def __( *args: P.args, **kwargs: P.kwargs ) -> R:
                try:                   
                    return func( *args, **kwargs )
                except Exception as error:
                    self._write( event, error_format( error ) )

                    raise error
           
            @wraps( func )
            async def __async( *args: P.args, **kwargs: P.kwargs ) -> R:
                try:                   
                    return await func( *args, **kwargs )
                except Exception as error:
                    self._write( event, error_format( error ) )

                    raise error

            return __async if inspect.iscoroutinefunction( func ) else __
        
        return wrap( args[0] ) if len( args ) == 1 and callable( args[0] ) else wrap

    @classmethod
    def from_config( cls, config: Config ):
        return cls.__init__( **config.__dict__ )

    @classmethod 
    def convert_config( cls, config: Dict[ str, Any ] ) -> Dict[ str, Any ]:
        return config

    @classmethod
    def from_config( cls, *config: List[Config] ):
        if len( config ) == 1:
            config  = cls.convert_config( config[0] )

            return cls( **config )
        else:
            return cls.multy( *[ cls.convert_config( _ ) for _ in config ] )
    
    @classmethod
    def multy( cls: Type[T], *config: List[Config|T] ):
        class MultyLogger( cls ):
            loggers: List[T]

            def __init__( self ):
                self.loggers = [ 
                    cls( **_ ) if isinstance( _, dict ) else _ 
                    for _ in config 
                ]
            
            def _write( self, event: Level, *messages: List[MessageDataType] ) -> List[Message]:
                result = [ ]

                for logger in self.loggers:
                    for message in logger._write( event, *messages ):
                        result.append( message )

                return result
            
        return MultyLogger( )

    def __repr__( self ) -> str:
        return f"{self.name}({self.level})"