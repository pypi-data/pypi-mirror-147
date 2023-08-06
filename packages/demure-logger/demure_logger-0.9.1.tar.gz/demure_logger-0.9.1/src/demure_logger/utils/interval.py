import inspect
import asyncio
import threading

from typing import Callable


def set_interval( func: Callable[ ..., None ], seconds: int | float ) -> threading.Timer:
    def _():
        set_interval( func, seconds )

        if inspect.iscoroutinefunction( func ):
            loop = asyncio.get_event_loop( )

            asyncio.set_event_loop( loop )

            loop.run_until_complete( func( ) )
        else:
            func( )
    
    interval = threading.Timer( seconds, _ )
    
    interval.start( )

    return interval