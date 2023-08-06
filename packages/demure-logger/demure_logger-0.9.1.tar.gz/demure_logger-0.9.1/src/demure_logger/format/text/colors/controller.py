from typing         import Optional
from colorama       import Fore, Back, Style
from .exceptions    import ColorDoesntExists, StyleDoesntExists


def get_code( code: str, bg: bool = False ) -> str:
    cls   = Back if bg else Fore
    color = getattr( cls, code.upper( ), None )
        
    if color is None:
        raise ColorDoesntExists( code )
    else:
        return color 

def get_style( code: str ) -> str:
    style = getattr( Style, code.upper( ), None )
        
    if style is None:
        raise StyleDoesntExists( code )
    else:
        return style

def set( content: str, color: str, style=str, bg: bool = False ) -> str:
    color   = get_code ( color, bg )
    style   = "" if style is None else get_style( style )
    resetor = Back.RESET if bg else Fore.RESET

    return color + style + content + resetor + Style.RESET_ALL


def text( content: str, color: str, style: Optional[str]=None ) -> str:
    return set( content, color, style )

def background( content: str, color: str, style: Optional[str]=None ) -> str:
    return set( content, color, style, True )

def paint( content: str, text_color: str='RESET', background_color: str='RESET', style: Optional[str]=None ) -> str:
    color   = get_code ( text_color )
    bg      = get_code ( background_color, True )
    style   = "" if style is None else get_style( style )

    return style + bg + color + content + Fore.RESET + Back.RESET + Style.RESET_ALL
