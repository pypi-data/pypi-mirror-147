import json

from demure_logger.format.text import Format as TextFormat
from demure_logger.log.message import Message
from typing                    import Dict, Any, Callable, List


DescriptionValue = str|int|bool|float | Dict[ str, str|int|bool|float ] | List[str|int|bool|float]


class Format( TextFormat ):
    _description : Dict[ str, Callable[ ..., DescriptionValue ] | DescriptionValue ]
    pretty       : bool = True
    record_type  : list|Callable[ [ Message ], str|int ]

    def __init__( self, record_type: list|Callable[ [ Message ], str|int ]=list, pretty: bool = True, **description: Dict[ str, str ] ):
        self._description = description
        self.pretty       = pretty
        self.record_type  = record_type 

    @property
    def description( self ) -> Dict[ str, DescriptionValue ] :
        result = { }

        for key, value in self._description.items( ):
            result[ key ] = value( ) if callable( value ) else value

        return result
    
    def prepare( self, message: Message, state: Dict[ str, Any ]={} ) -> str:
        state = { **state, **self.description }

        if self.record_type == list:
            records = state.get( 'records', [ ] )

            state['records'] = [ message.__jsonable__, *records ]
        else:
            records = state.get( 'records', { } )
            record  = { self.record_type( message ) : message.__jsonable__ }

            state['records'] = { **record, **records }

        json_params = dict( indent=4, sort_keys=True ) if self.pretty else { }

        return json.dumps( state, **json_params )