import sys
import re

from . import Colorizer
from .terminal_colors import TerminalColors


class Printer:
    _newline: bool = True
    _previous_newline: bool = False
    _single_line: bool = False

    @staticmethod
    def clear_line() -> None:
        """Clears the current line in the console."""
        sys.stdout.write(u"\u001b[K")
        sys.stdout.write(u"\u001b[1000D")
        sys.stdout.flush()

    @staticmethod
    def error(text: str, bold: bool = False, italic: bool = False,
              underlined: bool = False, strikethrough: bool = False) -> None:
        """Prints an error message to the console."""
        Printer.print(text, TerminalColors.ERROR, bold=bold, italic=italic,
                      underlined=underlined, strikethrough=strikethrough)

    @staticmethod
    def info(text: str, bold: bool = False, italic: bool = False,
             underlined: bool = False, strikethrough: bool = False) -> None:
        """Prints an info message to the console."""
        Printer.print(text, TerminalColors.INFO, bold=bold, italic=italic,
                      underlined=underlined, strikethrough=strikethrough)

    @staticmethod
    def prevent_newline(prevent: bool = True) -> None:
        """Prevents a newline from being printed to the console."""
        if Printer._newline != prevent:
            return
        Printer._newline = not prevent
        if Printer._newline:
            print()

    @staticmethod
    def print(text: str, color: str | tuple[int, int, int] | None = None,
              background: str | tuple[int, int, int] | None = None,
              bold: bool = False, italic: bool = False,
              underlined: bool = False, strikethrough: bool = False) -> None:
        """Prints a message to the console. Colors strings can be in 6-digit hex format or RGB format."""
        if Printer._single_line:
            Printer.clear_line()
        colored_text = Colorizer.colorize(text, color, background, bold, italic, underlined, strikethrough)
        print(colored_text, end='\n' if Printer._newline else '', flush=True)

    @staticmethod
    def set_single_line_mode(mode: bool):
        Printer._previous_newline = Printer._newline
        Printer._single_line = mode
        Printer.prevent_newline(mode if mode else Printer._previous_newline)

    @staticmethod
    def success(text: str, bold: bool = False, italic: bool = False,
                underlined: bool = False, strikethrough: bool = False) -> None:
        """Prints a success message to the console."""
        Printer.print(text, TerminalColors.SUCCESS, bold=bold, italic=italic,
                      underlined=underlined, strikethrough=strikethrough)

    @staticmethod
    def strip_ansi(text: str) -> str:
        """Strips ANSI escape sequences from a string."""
        return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

    @staticmethod
    def strip_colors(text: str) -> str:
        stripped_text = re.sub(r'\x1b[\[\d;]+m', '', text)
        return Printer.strip_ansi(stripped_text)

    @staticmethod
    def warning(text: str, bold: bool = False, italic: bool = False,
                underlined: bool = False, strikethrough: bool = False) -> None:
        """Prints a warning message to the console."""
        Printer.print(text, TerminalColors.WARNING, bold=bold, italic=italic,
                      underlined=underlined, strikethrough=strikethrough)
