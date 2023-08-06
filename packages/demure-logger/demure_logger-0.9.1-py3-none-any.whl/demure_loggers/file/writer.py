import json
import uuid
import tempfile
import warnings
import threading
import time
import psutil
import random

from glob                 import glob
from os                   import path as os_path, remove as os_remove
from demure_logger.writer import BasicWriter
from typing               import Callable, Optional, TypeVar, Any
from io                   import TextIOWrapper


WriterPath   = str | Callable[ ..., str ]
WriterStream = Callable[ ..., TextIOWrapper ]

T    = TypeVar( 'T' )
Self = TypeVar( 'Self' )


class Writer( BasicWriter[str] ):
    _mode: str = 'a+'

    __threard  = threading.current_thread( ).ident
    __mutex    = threading.Lock( )

    _path   : Optional[ WriterPath   ]
    _stream : Optional[ WriterStream ]

    __mutex_owner: int | None

    def __init__( self, 
        path   : Optional[ WriterPath   ] = None,
        stream : Optional[ WriterStream ] = None, 
        *args, **kwargs
    ):
        super( ).__init__( *args, **kwargs )
        
        self.__mutex_owner = None

        if path is not None:
            self._path = path
        elif stream is not None:
            self._stream = stream
        else:
            self._path = os_path.join( tempfile.gettempdir( ), str( uuid.uuid4() ) + '.log' )

            warnings.warn( f"stream and path is None, will use default path for log '{self._path}'" )

        stream = self.stream

        stream.close( )
    
    @property
    def stream( self ) -> TextIOWrapper:
        if self._path is not None:
            path = os_path.abspath( self._path( ) if callable( self._path ) else self._path )
            
            return open( path, self._mode )
        else:
            return self._stream( )
    
    def __write( self, message: str ):
        stream = self.stream
            
        stream.write( f"{message}\n" )

        stream.close( )

    def __truncate( self ) -> str:
        tmp = self._mode

        self._mode = 'r+'

        stream = self.stream

        content = str( stream.read( ) )

        self._mode = tmp
        
        stream.seek( 0 )
        stream.truncate( )
        
        stream.close( )

        return content
    
    def __read( self ) -> str:
        tmp = self._mode

        self._mode = 'r+'

        steam = self.stream

        content = str( steam.read( ) )

        self._mode = tmp
        
        steam.close( )

        return content

    @property
    def current_thread( self ) -> str:
        return str( threading.current_thread( ).ident )

    @property
    def locker_prefix( self ) -> str:
        path = os_path.abspath( self._path( ) if callable( self._path ) else self._path )

        return f"{path}.lock" 

    @property
    def locker_path( self ) -> str:
        return f"{self.locker_prefix}.{self.current_thread}"
        
    def lock( self, retry: int=100 ) :
        locker = glob( f"{self.locker_prefix}.*" )
        locker = locker[-1] if len( locker ) > 0 else None
 
        if locker is not None:
            time.sleep( 0.01 )

            pid = int( locker.strip( ).split( "." )[-1] )
        
            if not psutil.pid_exists( pid ):
                self.unlock( locker )

                return self.lock( retry - 1 )
            elif retry > 0:
                return self.lock( retry - 1 )
            else:
                raise RuntimeError( f"Can't unlock file '{self.locker_path}' blocked by '{pid}'" )
        else:
            with open( self.locker_path, 'a+' ) as file:
                file.write( self.current_thread ) 

    def unlock( self, path: str ) : 
        if os_path.exists( path ):
            os_remove( path )
    
    def write( self, message: str, unsafe: bool = False ):
        return self.safe( lambda _ : self.__write( message ), unsafe )

    def truncate( self, unsafe: bool = False ) -> str:
        return self.safe( lambda _ : self.__truncate( ), unsafe )

    def read( self, unsafe: bool = False ) -> str:
        return self.safe( lambda _ : self.__read( ), unsafe )

    def safe( self: Self, func: Callable[ Self, T ], unsafe: bool = False ) -> T:
        pid = threading.current_thread( ).ident

        if self.__threard != pid and not unsafe:
            self.__mutex.acquire( 1 )

            self.__mutex_owner = pid

            try:
                self.lock( )

                return func( self )  
            finally:
                self.__mutex_owner = None

                self.unlock( self.locker_path )

                self.__mutex.release( )
        else:
            return func( self )  

  
