import os
import inspect
import threading

from typing                          import Dict, Any
from demure_logger.log.message.field import TextField, NumberField, DatetimeField, LogLevelField, Field
from datetime                        import datetime     
from dateutil.tz                     import tzlocal
from demure_logger.log.message       import BasicMessage
from demure_logger.log               import Levels


class Message( BasicMessage ): 
    pid       = NumberField  ( default=lambda : threading.current_thread( ).ident )
    event     = LogLevelField( default=Levels.INFO                                )
    timestamp = DatetimeField( default=lambda : datetime.now( tzlocal( ) )        )
    message   = TextField    (                                                    )

    __sort_by__ = [ 'event', 'pid', 'timestamp', 'message' ]


class TraceMixin( Message ):
    trace = TextField    ( default=lambda : ":".join( 
        str( line ) for line in inspect.getouterframes( inspect.currentframe( ) )[-1][1:3] 
    ) )


class OsEnvironMixin( Message ):
    @property
    def __dict__( self ) -> Dict[ str, Field[Any] ]:
        return dict(
            **{
                column.name : column
                for column in self.__ordered__
            },
            **os.environ
        )