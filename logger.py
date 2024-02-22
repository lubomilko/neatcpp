import sys
from enum import IntEnum
from typing import Callable


class Logger():
    class ErrSeverity(IntEnum):
        INFO = 0
        WARNING = 1
        CRITICAL = 2
        SEVERE = 3

    def __init__(self, verbosity: int = 0, min_err_severity: int = 0, enable_debug_msg: bool = False) -> None:
        self.verbosity: int = verbosity
        self.min_err_severity: int = min_err_severity
        self.debug_msg_enabled: bool = enable_debug_msg
        self.__msg_printer: Callable[[str, bool, str], None] = self.__default_msg_printer
        self.__err_printer: Callable[[str, self.ErrSeverity, str], None] = self.__default_err_printer

    def config(self, verbosity: int = 0, min_err_severity: int = 0, enable_debug_msg: bool = False) -> None:
        self.verbosity = verbosity
        self.min_err_severity = min_err_severity
        self.debug_msg_enabled = enable_debug_msg

    def set_printers(
            self, msg_printer: Callable[[str, str], None] | None = None,
            err_printer: Callable[[str, ErrSeverity, str], None] | None = None) -> None:
        self.__msg_printer = msg_printer if msg_printer else self.__default_msg_printer
        self.__err_printer = err_printer if err_printer else self.__default_err_printer

    def dbg(self, text: str, end: str = "\n") -> None:
        if self.debug_msg_enabled:
            self.__msg_printer(text, True, end)

    def msg(self, text: str, msg_verbosity: int = 1, max_msg_verbosity: int = 0, end: str = "\n") -> None:
        max_verbosity = max(max_msg_verbosity, msg_verbosity) if max_msg_verbosity > 0 else self.verbosity
        if msg_verbosity <= self.verbosity <= max_verbosity:
            self.__msg_printer(text, False, end)

    def err(self, text: str, severity: ErrSeverity = ErrSeverity.WARNING, end: str = "\n") -> None:
        if self.min_err_severity <= severity:
            self.__err_printer(text, severity, end)

    @staticmethod
    def __default_msg_printer(text: str, debug_msg: bool, end: str) -> None:
        if debug_msg:
            text = f"DEBUG: {text}"
        print(text, file=sys.stdout, end=end)

    @staticmethod
    def __default_err_printer(text: str, severity: ErrSeverity, end: str) -> None:
        severity_text = {0: "INFO", 1: "WARNING", 2: "CRITICAL", 3: "SEVERE"}
        sev = severity_text.get(severity, "UNDEFINED")
        print(f"ERROR ({sev}): {text}", file=sys.stderr, end=end)


log = Logger()
