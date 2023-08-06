import asyncio
import random
import inspect

from ..structure.queue import Queue
from typing            import TypeVar, List, Any, Callable
from ..                import BasicLogger, MessageDataType
from ..log             import Level


Logger  = TypeVar( 'Logger' , bound=BasicLogger  )
    

class Event:
    type: Level
    data: MessageDataType

    def __init__( self, 
        type: Level,
        data: MessageDataType
    ):
        self.type = type
        self.data = data
    

class Handler:
    queue         : Queue[Event]
    event_updater : Callable[ ..., None ]
    running       : bool

    def __init__( self, 
        loggers       : List[Logger]=[],
        queue         : Queue[Event]=Queue( ),
        event_updater : Callable[ ..., None ]=None
    ):
        self.event_updater = event_updater
        self.loggers       = loggers
        self.queue         = queue
        self.running       = False

    def handle( self, event: Any ):
        if isinstance( event, Event ):
            for logger in self.loggers:
                logger._write( event.type, event.data )

    def stop( self ):
        self.running = False
    
    async def run( self, max_recursion: int = None ):
        self.running = True

        while self.running:
            if self.event_updater is not None:
                if inspect.iscoroutinefunction( self.event_updater ):
                    await self.event_updater( )
                else:
                    self.event_updater( )

            event = await self.queue.pop( )

            if event is not None:
                self.handle( event )
            else:
                await asyncio.sleep( random.uniform( 0.01, 0.1 ) )

            if max_recursion is not None:
                max_recursion -= 1

                if max_recursion == 0: break 

    