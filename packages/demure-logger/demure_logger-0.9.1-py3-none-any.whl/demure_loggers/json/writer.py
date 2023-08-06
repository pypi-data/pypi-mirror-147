import uuid
import warnings
import tempfile
import os.path as os_path

from io            import TextIOWrapper
from typing        import Optional, TypeVar, Callable
from ..file.writer import Writer as FileWriter, WriterPath, WriterStream


T    = TypeVar( 'T'    )
Self = TypeVar( 'Self' )


class Writer( FileWriter ): 
    _mode = 'w'

    def __init__( self, 
        path       : Optional[ WriterPath   ] = None,
        stream     : Optional[ WriterStream ] = None, 
        *args, **kwargs
    ):
        if path is not None:
            self._path = path
        elif stream is not None:
            self._stream = stream
        else:
            self._path = os_path.join( tempfile.gettempdir( ), str( uuid.uuid4() ) + '.log' )

            warnings.warn( f"stream and path is None, will use default path for log '{self._path}'" )

        super( ).__init__( *args, **kwargs )
