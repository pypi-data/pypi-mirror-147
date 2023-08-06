import os
import inspect

from .field                    import TextField, NumberField, DatetimeField, LogLevelField
from datetime                  import datetime     
from dateutil.tz               import tzlocal
from demure_logger.log.message import BasicMessage, Message as MessageTemplate
from demure_logger.log         import Levels


colors = dict ( 
    FATAL  = 'LIGHTRED_EX',
    ERROR  = 'red',
    WARN   = 'yellow',	
    INFO   = 'blue',
    DEBUG  = 'cyan'
)


class Message( BasicMessage ): 
    pid       = NumberField  ( default=os.getpid, color='white', background='black', style='BRIGHT' )
    event     = LogLevelField( default=Levels.INFO, color=lambda level: colors.get( level.name, None ) )
    timestamp = DatetimeField( default=lambda : datetime.now( tzlocal( ) ) )
    message   = TextField    ( )

    __sort_by__ = [ 'event', 'pid', 'timestamp', 'message' ]