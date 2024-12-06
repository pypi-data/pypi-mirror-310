"""
prozt
----------
Simple print wrapper to add color support to python using ANSI color codes
"""

from typing_extensions import Literal, Final
from colorama import Fore, Back, Style

__COLOR_LIST : Final = [
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.CYAN,
    Fore.BLUE,
    Fore.MAGENTA,
]
"""Only used internally"""

def prozt(*values : object, sep : str | None = " ", end : str | None = "\n", file = None, flush : Literal[False] = False, fg_color : str | None = None, bg_color : str | None = None, style : str | None = None) -> None:
    """
    Print the values to the console with ANSI color support!

    Args:
        sep (str | None, optional): string inserted between values, default a space.
        end (str | None, optional): string appended after the last value, default a newline.
        file (_type_, optional): a file-like object (stream), defaults to the current sys.stdout.
        flush (Literal[False], optional): whether to forcibly flush the stream.
        fg_color (str | None, optional): ANSI Code for Foreground color of the text. Use colorama.Fore for simple colors.
        bg_color (str | None, optional): ANSI Code for Background color of the text. Use colorama.Back for simple colors.
        style (str | None, optional): ANSI Code for Style of the text. Use colorama.Style for simple colors.
    """
            
    if(fg_color):
        print(fg_color, sep="", end="")
        
    if(bg_color):
        print(bg_color, sep="", end="")
    
    if(style):
        print(style, sep="", end="")
    
    print(*values, sep=sep, end=end, file=file, flush=flush)
    
    print(Fore.RESET, sep="", end="")
    print(Back.RESET, sep="", end="")
    print(Style.RESET_ALL, sep="", end="")
    
def prozt_rainbow(*values : object, sep : str | None = " ", end : str | None = "\n", flush : Literal[False] = False):
    """
    Print something to the console in style.

    Args:
        sep (str | None, optional): string inserted between values, default a space.
        end (str | None, optional): string appended after the last value, default a newline.
        file (_type_, optional): a file-like object (stream), defaults to the current sys.stdout.
        flush (Literal[False], optional): whether to forcibly flush the stream.
    """
    rain_index = 0
    for val in values:
        for letter in str(val):
            prozt(letter, fg_color=__COLOR_LIST[rain_index], sep = "", end = "")
            rain_index = (rain_index + 1) % 6
        print(sep, sep="", end="")
    print(end, sep = "", end = "")