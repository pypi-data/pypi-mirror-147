import uuid

from ...file.message                 import OsEnvironMixin
from demure_logger.log.message.field import UUIDField


class Message( OsEnvironMixin ): 
    id = UUIDField( default=uuid.uuid4 )