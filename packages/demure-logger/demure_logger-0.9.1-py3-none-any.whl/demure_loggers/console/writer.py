import sys

from demure_logger.writer import BasicWriter
from typing               import TextIO


class Writer( BasicWriter[str] ):
    def write( self, message: str ):
        print( message )