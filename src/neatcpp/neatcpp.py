"""
neatcpp - A minimalistic C preprocessor preserving the original C code formatting.

Copyright (C) 2025 Lubomir Milko
This file is part of neatcpp <https://github.com/lubomilko/neatcpp>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# pylint: disable=missing-class-docstring, missing-function-docstring

import re
import sys
import argparse
from enum import IntEnum
from typing import Callable, Generator
from textwrap import dedent
from pathlib import Path


__author__ = "Lubomir Milko"
__copyright__ = "Copyright (C) 2025 Lubomir Milko"
__version__ = "1.2.0"
__license__ = "GPLv3"
__module_name__ = "neatcpp"
__summary__ = "A minimalistic C preprocessor preserving the original C code formatting."


CLI_DESCRIPTION = f"{__module_name__} {__version__}\n{(len(__module_name__) + len(__module_name__) + 1) * '-'}\n{__summary__}"
CLI_EPILOG = __copyright__
CLI_DEBUG_ARGS_LIST = None


class Logger():
    class ErrSeverity(IntEnum):
        INFO = 0
        WARNING = 1
        CRITICAL = 2
        SEVERE = 3

    def __init__(self, verbosity: int = 0, min_err_severity: int = ErrSeverity.INFO, enable_debug_msg: bool = False) -> None:
        self.verbosity: int = verbosity
        self.min_err_severity: int = min_err_severity
        self.debug_msg_enabled: bool = enable_debug_msg
        self.__msg_printer: Callable[[str, bool, str], None] = self.default_msg_printer
        self.__err_printer: Callable[[str, Logger.ErrSeverity, str], None] = self.default_err_printer

    def config(self, verbosity: int = 0, min_err_severity: int = ErrSeverity.INFO, enable_debug_msg: bool = False) -> None:
        self.verbosity = verbosity
        self.min_err_severity = min_err_severity
        self.debug_msg_enabled = enable_debug_msg

    def set_printers(
            self, msg_printer: Callable[[str, bool, str], None] | None = None,
            err_printer: Callable[[str, ErrSeverity, str], None] | None = None) -> None:
        self.__msg_printer = msg_printer if msg_printer else self.default_msg_printer
        self.__err_printer = err_printer if err_printer else self.default_err_printer

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
    def default_msg_printer(text: str, debug_msg: bool, end: str) -> None:
        if debug_msg:
            text = f"DEBUG: {text}"
        print(text, file=sys.stdout, end=end)

    @staticmethod
    def default_err_printer(text: str, severity: ErrSeverity, end: str) -> None:
        severity_text = {0: "INFO", 1: "WARNING", 2: "CRITICAL", 3: "SEVERE"}
        sev = severity_text.get(severity, "UNDEFINED")
        print(f"ERROR ({sev}): {text}", file=sys.stderr, end=end)


class PreprocLogger(Logger):
    def __init__(self, verbosity: int = 0, min_err_severity: int = Logger.ErrSeverity.INFO, enable_debug_msg: bool = False) -> None:
        super().__init__(verbosity, min_err_severity, enable_debug_msg)
        self.proc_file_name: str = ""
        self.proc_file_line: int = 0
        self.set_printers(self.msg_printer, self.err_printer)

    def msg_printer(self, text: str, debug_msg: bool, end: str) -> None:
        text = self.__fill_location_tag(text)
        self.default_msg_printer(text, debug_msg, end)

    def err_printer(self, text: str, severity: Logger.ErrSeverity, end: str) -> None:
        text = self.__fill_location_tag(text)
        self.default_err_printer(text, severity, end)

    def __fill_location_tag(self, text: str) -> str:
        if self.proc_file_name:
            loc = f"Processed file: {self.proc_file_name}, start line: {self.proc_file_line + 1}"
        else:
            loc = f"Processed start line: {self.proc_file_line + 1}"
        return text.replace("%l", loc)

    def get_code_sample(self, code: str, sample_len: int = 80) -> str:
        sample = code.replace("\n", "").lstrip()[:sample_len]
        if len(code) > sample_len:
            sample = f"{sample} ..."
        return sample


log = PreprocLogger()


class CodeFormatter():
    RE_PTRN_MLINE_CMNT = re.compile(r"/\*.*?\*/", re.ASCII + re.DOTALL)
    RE_PTRN_SLINE_CMNT = re.compile(r"[ \t]*//[^\n]*", re.ASCII)
    RE_PTRN_LINE_CONT = re.compile(r"[ \t]*\\[ \t]*\n", re.ASCII)
    RE_PTRN_NUM_CONST = re.compile(r"(?P<num>\d[\d.]*\d*)(?:[uUlLfF]+)", re.ASCII)

    @staticmethod
    def replace_tabs(code: str, tab_size: int = 4) -> str:
        out_code = ""
        for line in code.splitlines():
            tab_pos = line.find("\t")
            while tab_pos >= 0:
                line = line.replace("\t", f"{(tab_size - (tab_pos % tab_size)) * ' '}", 1)
                tab_pos = line.find("\t")
            out_code = f"{out_code}{line}\n"
        return out_code

    @staticmethod
    def remove_line_escapes(code: str, keep_newlines: bool = False) -> str:
        repl_str = "\n" if keep_newlines else ""
        out_code = CodeFormatter.RE_PTRN_LINE_CONT.sub(repl_str, code)
        return out_code

    @staticmethod
    def remove_empty_lines(code: str) -> str:
        out_lines = [line for line in code.splitlines() if line.strip()]
        return "\n".join(out_lines)

    @staticmethod
    def remove_comments(code: str, replace_with_spaces: bool = False, replace_with_newlines: bool = False) -> str:
        def __repl_with_spaces(match: re.Match) -> str:
            return re.sub("[^\n]+", lambda m: " " * len(m.group()), match.group())

        def __repl_with_newlines(match: re.Match) -> str:
            return "\n" * match.group().count("\n")

        out_code = code
        if replace_with_spaces:
            out_code = CodeFormatter.RE_PTRN_MLINE_CMNT.sub(__repl_with_spaces, out_code)
            out_code = CodeFormatter.RE_PTRN_SLINE_CMNT.sub(__repl_with_spaces, out_code)
        elif replace_with_newlines:
            out_code = CodeFormatter.RE_PTRN_MLINE_CMNT.sub(__repl_with_newlines, out_code)
            out_code = CodeFormatter.RE_PTRN_SLINE_CMNT.sub(__repl_with_newlines, out_code)
        return out_code

    @staticmethod
    def remove_num_type_suffix(code: str) -> str:
        def __repl_num_wo_suffix(match: re.Match) -> str:
            return match.group("num")

        out_code = CodeFormatter.RE_PTRN_NUM_CONST.sub(__repl_num_wo_suffix, code)
        return out_code

    @staticmethod
    def get_enclosed_subst_pos(code: str, start_pos: int = 0, start_str: str = "(", end_str: str = ")",
                               ignored_prefix_re_ptrn: re.Pattern = re.compile(r"\s*", re.ASCII)) -> tuple[int, int]:
        s_pos = code.find(start_str, start_pos)
        e_pos = -1
        if s_pos >= 0 and ignored_prefix_re_ptrn.match(code, start_pos, s_pos) is not None:
            e_pos = code.find(end_str, s_pos + 1)
            while e_pos >= 0 and (code[s_pos: e_pos + 1].count(start_str) != code[s_pos: e_pos + 1].count(end_str)):
                e_pos = code.find(end_str, e_pos + 1)
            if e_pos < 0:
                s_pos = -1
        return (s_pos, e_pos)

    @staticmethod
    def is_in_comment(code: str, pos: int) -> bool:
        in_comment = False
        if 0 <= pos < len(code):
            cmnt_pos = code.rfind("/*", 0, pos)
            if cmnt_pos >= 0:
                cmnt_pos = code.find("*/", cmnt_pos, pos)
                if cmnt_pos < 0:
                    in_comment = True
            if not in_comment:
                cmnt_pos = code.rfind("//", 0, pos)
                if cmnt_pos >= 0:
                    newline_pos = code.find("\n", cmnt_pos, pos)
                    if newline_pos < 0:
                        in_comment = True
        return in_comment

    @staticmethod
    def is_in_string(code: str, pos: int) -> bool:
        in_string = False
        if 0 <= pos < len(code):
            newline_pos = code.rfind("\n", 0, pos) + 1
            dbl_quote_count = code[newline_pos: pos].count("\"")
            sgl_quote_count = code[newline_pos: pos].count("\'")
            if dbl_quote_count & 1 or sgl_quote_count & 1:
                in_string = True
        return in_string


class FileIO():
    def __init__(self) -> None:
        self.incl_dir_paths: list[Path] = [Path("")]

    def reset(self) -> None:
        self.incl_dir_paths = [Path("")]

    def add_include_dir(self, *dir_paths: str | Path) -> None:
        for dir_path in dir_paths:
            log.msg(f"Adding include directory '{Path(dir_path).name}'.")
            incl_dir_path = Path(dir_path).resolve()
            if incl_dir_path.is_file():
                incl_dir_path = incl_dir_path.parent
            if incl_dir_path.is_dir():
                if incl_dir_path not in self.incl_dir_paths:
                    self.incl_dir_paths.append(incl_dir_path)
            else:
                log.err(f"Include dir '{dir_path}' not found.")

    def read_file(self, file_path: str | Path) -> str:
        for incl_dir_path in self.incl_dir_paths:
            incl_file_path = Path(incl_dir_path, Path(file_path))
            if incl_file_path.is_file():
                with open(incl_file_path, "r", encoding="utf-8") as file:
                    file_code = file.read()
                break
        else:
            log.err(f"File '{file_path}' not found.", log.ErrSeverity.INFO)
            file_code = ""
        return file_code


class ConditionManager():
    class BranchState(IntEnum):
        ACTIVE = 0  # if/elif/else branch code is enabled and if/elif/else condition is true (active).
        SEARCH = 1  # if/elif/else branch code is enabled and if condition is not true, so search for true elif/else condition.
        IGNORE = 2  # if/elif/else branch code is not enabled, i.e. the condition does not have to be evaluated anymore.

    def __init__(self) -> None:
        self.branch_state: ConditionManager.BranchState = self.BranchState.ACTIVE
        self.branch_state_stack: list[ConditionManager.BranchState] = []

    def reset(self) -> None:
        self.branch_state = self.BranchState.ACTIVE
        self.branch_state_stack = []

    @property
    def branch_depth(self) -> int:
        return len(self.branch_state_stack)

    @property
    def branch_active(self) -> bool:
        return bool(self.branch_state == self.BranchState.ACTIVE)

    @property
    def branch_search_active(self) -> bool:
        return bool(self.branch_state in (self.BranchState.SEARCH, self.BranchState.ACTIVE))

    def enter_if(self, is_true: bool) -> None:
        self.branch_state_stack.append(self.branch_state)
        if self.branch_state == self.BranchState.ACTIVE:
            if not is_true:
                self.branch_state = self.BranchState.SEARCH
        else:
            self.branch_state = self.BranchState.IGNORE

    def enter_elif(self, is_true: bool) -> None:
        if self.branch_state == self.BranchState.SEARCH:
            if is_true:
                self.branch_state = self.BranchState.ACTIVE
        else:
            self.branch_state = self.BranchState.IGNORE

    def exit_if(self) -> None:
        if self.branch_depth > 0:
            self.branch_state = self.branch_state_stack.pop()
        else:
            log.err("Unexpected #endif detected (%l).", log.ErrSeverity.CRITICAL)


class CodeType(IntEnum):
    CODE = 0
    DIRECTIVE = 1
    COMMENT = 2
    SPACE = 3


class PreprocInput():
    def yield_code_parts(self, code: str) -> Generator[tuple[CodeType, str], None, None]:
        in_lines = code.splitlines()
        line_idx = 0
        code_lines_num = len(in_lines)
        while line_idx < code_lines_num:
            out_lines = []
            in_line = in_lines[line_idx].rstrip()
            out_lines.append(in_line)
            log.proc_file_line = line_idx
            line_idx += 1
            # Detect and extract continuous line split to lines ending with "\".
            if in_line.endswith("\\"):
                while line_idx < code_lines_num:
                    in_line = in_lines[line_idx].rstrip()
                    out_lines.append(in_line)
                    line_idx += 1
                    if not in_line.endswith("\\"):
                        break
            # Detect and extract multiline comment.
            elif "/*" in in_line and "*/" not in in_line:
                while line_idx < code_lines_num:
                    in_line = in_lines[line_idx].rstrip()
                    out_lines.append(in_line)
                    line_idx += 1
                    if "*/" in in_line:
                        break
                else:
                    log.err("Unterminated comment detected (%l).", log.ErrSeverity.CRITICAL)
            # Detect and extract multiple empty lines.
            elif not in_line:
                while line_idx < code_lines_num and not in_lines[line_idx].strip():
                    out_lines.append("")
                    line_idx += 1

            out_code = "\n".join(out_lines)
            out_code_stripped = out_code.strip()
            if out_code_stripped.startswith("#"):
                out_type = CodeType.DIRECTIVE
            elif not out_code_stripped:
                out_type = CodeType.SPACE
            elif ((out_code_stripped.startswith("/*") and out_code_stripped.endswith("*/")) or
                    out_code_stripped.startswith("//")):
                out_type = CodeType.COMMENT
            else:
                out_type = CodeType.CODE
            yield (out_type, out_code)


class PreprocOutput():
    def __init__(self) -> None:
        self.last_space: str = ""
        self.last_comment: str = ""
        self.non_empty: bool = False
        self.code: str = ""
        self.code_all: str = ""

    def reset(self) -> None:
        self.last_space = ""
        self.last_comment = ""
        self.non_empty = False
        self.code = ""
        self.code_all = ""

    def add_code_part(self, code_part: str, code_type: CodeType) -> None:
        self.code_all = f"{self.code_all}{code_part}\n"
        match code_type:
            case CodeType.SPACE:
                if self.non_empty:
                    self.last_space = f"{code_part}\n"
                self.last_comment = ""
            case CodeType.COMMENT:
                self.last_comment = f"{self.last_comment}{code_part}\n"
            case CodeType.DIRECTIVE:
                self.last_space = ""
                self.last_comment = ""
            case CodeType.CODE:
                self.code = f"{self.code}{self.last_space}{self.last_comment}{code_part}\n"
                self.last_space = ""
                self.last_comment = ""
                self.non_empty = True


class DirectiveGroup(IntEnum):
    STANDARD = 0
    CONDITIONAL = 1


class Directive():
    def __init__(self, re_ptrn: re.Pattern | None = None, handler: Callable[[dict[str, str | None], str], None] | None = None) -> None:
        self.re_ptrn: re.Pattern | None = re_ptrn
        self.handler: Callable[[dict[str, str | None], str], None] | None = handler

    def process(self, code: str) -> bool:
        processed = False
        if self.re_ptrn and self.handler:
            joined_code = CodeFormatter.remove_line_escapes(code)
            re_match = self.re_ptrn.match(joined_code)
            if re_match:
                self.handler(re_match.groupdict(), code)
                processed = True
        return processed


class Macro():
    def __init__(self, identifier: str = "", args: list[str] | None = None, body: str = "") -> None:
        self.identifier: str = identifier
        self.args: list[str] = args if args is not None else []
        self.body: str = body

    def expand_args(self, arg_vals: list[str] | None = None, fully_exp_arg_vals: list[str] | None = None) -> str:
        exp_code = self.body
        if arg_vals is not None and fully_exp_arg_vals is not None:
            for (arg_idx, arg_name) in enumerate(self.args):
                # Handle variadic arguments.
                if arg_name == "...":
                    arg_name = "__VA_ARGS__"
                    arg_val = ""
                    fully_exp_arg_val = ""
                    for arg_val_idx in range(arg_idx, len(arg_vals)):
                        arg_val = f"{arg_val}{arg_vals[arg_val_idx]}, "
                        fully_exp_arg_val = f"{fully_exp_arg_val}{fully_exp_arg_vals[arg_val_idx]}, "
                    arg_val = arg_val[:-2]  # Remove the last two characters, i.e. ", " that is used for argument separation.
                    fully_exp_arg_val = fully_exp_arg_val[:-2]
                else:
                    # If argument value is specified, then use it. Otherwise use empty string (not enough parameters in a macro reference).
                    arg_val = arg_vals[arg_idx] if arg_idx < len(arg_vals) else ""
                    fully_exp_arg_val = fully_exp_arg_vals[arg_idx] if arg_idx < len(fully_exp_arg_vals) else ""
                # Perform concatenatenation of macro arguments specified by the ## operator.
                exp_code = re.sub(rf"[\s\\]*##[\s\\]*{arg_name}", rf"##{arg_val}", exp_code, count=0, flags=re.ASCII + re.MULTILINE)
                exp_code = re.sub(rf"{arg_name}[\s\\]*##[\s\\]*", rf"{arg_val}##", exp_code, count=0, flags=re.ASCII + re.MULTILINE)
                # Perform stringification specified by the # operator.
                exp_code = re.sub(rf"(^|[^#])#\s*{arg_name}($|[^\w])", r'\g<1>"' + arg_val.replace("\\", "\\\\") + r'"\g<2>',
                                  exp_code, count=0, flags=re.ASCII + re.MULTILINE)
                # Replace the macro argument in macro body with the fully expanded argument value.
                exp_code = re.sub(rf"(^|[^\w]){arg_name}($|[^\w])", rf"\g<1>{fully_exp_arg_val}\g<2>",
                                  exp_code, count=0, flags=re.ASCII + re.MULTILINE)
        # Perform concatenatenations specified by the ## operator by removing the operator and its surrounding spaces.
        exp_code = re.sub(r"[\s\\]*##[\s\\]*", "", exp_code, count=0, flags=re.ASCII + re.MULTILINE)
        # Perform an lstrip in case some of the expanded arguments are empty and generate a whitespace at the beginning of the macro body.
        return exp_code.lstrip()


class NeatCpp():
    """A minimalistic C preprocessor class.

    Attributes:
        macros (dict[str, Macro]): A dictionary with all macros defined by the processed ``#define`` directives. This dictionary is
            typically updated and used by this class itself, but can be modified by the user if necessary.
        exclude_macros_files (list[str]): A list of user-defined macro names and file names to be excluded from processing.
            The ``#define`` and ``#include`` directives for the specified macros and files will not be processed.
    """
    def __init__(self) -> None:
        self.__file_io: FileIO = FileIO()
        self.__output: PreprocOutput = PreprocOutput()
        self.__cond_mngr: ConditionManager = ConditionManager()
        self.__directives: tuple[tuple[Directive, ...], ...] = (
            # DirectiveGroup.STANDARD
            (Directive(re.compile(r"^[ \t]*#[ \t]*define[ \t]+(?P<ident>\w+)(?:\((?P<args>[^\)]*)\))?", re.ASCII), self.__process_define),
             Directive(re.compile(r"^[ \t]*#[ \t]*undef[ \t]+(?P<ident>\w+)", re.ASCII), self.__process_undef),
             Directive(re.compile(r"^[ \t]*#[ \t]*include[ \t]+(?:\"|<)(?P<file>[^\">]+)(?:\"|>)", re.ASCII), self.__process_include)),
            # DirectiveGroup.CONDITIONAL
            (Directive(re.compile(r"^[ \t]*#[ \t]*if[ \t]+(?P<expr>.*)", re.ASCII), self.__process_if),
             Directive(re.compile(r"^[ \t]*#[ \t]*elif[ \t]+(?P<expr>.*)", re.ASCII), self.__process_elif),
             Directive(re.compile(r"^[ \t]*#[ \t]*else(?:\s|$)", re.ASCII), self.__process_else),
             Directive(re.compile(r"^[ \t]*#[ \t]*endif(?:\s|$)", re.ASCII), self.__process_endif),
             Directive(re.compile(r"^[ \t]*#[ \t]*ifdef[ \t]+(?P<expr>.*)", re.ASCII), self.__process_ifdef),
             Directive(re.compile(r"^[ \t]*#[ \t]*ifndef[ \t]+(?P<expr>.*)", re.ASCII), self.__process_ifndef)))
        self.macros: dict[str, Macro] = {}
        self.exclude_macros_files: list[str] = []

    # ----- INTERFACE METHODS ----- #
    @property
    def output(self) -> str:
        """Processed output string.

        Returns:
            str: Processed output string without the preprocessor directives, comments and whitespaces between them.
        """
        return self.__output.code

    @output.setter
    def output(self, code: str) -> None:
        self.__output.code = code

    @property
    def output_full(self) -> str:
        """Processed full output string including all preprocessor directives, comments and whitespaces.

        Returns:
            str: Full processed output string including all preprocessor directives, comments and whitespaces.
        """
        return self.__output.code_all

    @output_full.setter
    def output_full(self, code: str) -> None:
        self.__output.code_all = code

    def reset(self) -> None:
        """Resets the preprocessor including its output and all other internal values.
        """
        self.__file_io.reset()
        self.__output.reset()
        self.__cond_mngr.reset()
        self.macros = {}
        self.exclude_macros_files = []

    def reset_output(self) -> None:
        """Resets the preprocessor output only. Other internal values remain unchanged.
        """
        self.__output.reset()

    def save_output_to_file(self, file_path: str | Path, full_output: bool = False) -> None:
        """Saves the processed output to file.

        Args:
            file_path (str): Save file path.
            full_output (bool, optional): Flag to save the full output, i.e., including all preprocessor directives,
                all comments and whitespaces. Defaults to False.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            log.msg(f"Saving processed output to file '{Path(file_path).name}'.")
            output = self.output_full if full_output else self.output
            file.write(output)

    def add_include_dirs(self, *dir_paths: str | Path) -> None:
        """Adds paths to the included directories for searching files specified either manually or by the #include directives.

        Args:
            dir_paths (str): One or more arguments specifying paths to include directories.
        """
        self.__file_io.add_include_dir(*dir_paths)

    def process_files(self, *file_paths: str | Path, global_output: bool = True, full_local_output: bool = False) -> str:
        """Processes the specified C source files

        Args:
            file_paths (str): One or more arguments specifying paths to processed files.
            global_output (bool, optional): Flag to add the processed output to the global internal preprocessor output.
                Defaults to True.
            full_local_output (bool, optional): Flag to return the full output (including directives, etc.) instead of
                the standard output (without directives). Defaults to False.

        Returns:
            str: Local output for the processed file. Generated always, regardless of the ``global_output`` argument value.
        """
        file_code = ""
        local_output_code = ""
        for file_path in file_paths:
            file_code = self.__file_io.read_file(file_path)
            if file_code:
                local_output_code += self.process_code(file_code, global_output, full_local_output, Path(file_path).name)
        return local_output_code

    def process_code(self, code: str, global_output: bool = True, full_local_output: bool = False, proc_file_name: str = "") -> str:
        """Processes the specified source code string.

        Args:
            code (str): Source code to be processed.
            global_output (bool, optional): Flag to add the processed output to the global internal preprocessor output.
                Defaults to True.
            full_local_output (bool, optional): Flag to return the full output (including directives, etc.) instead of
                the standard output (without directives). Defaults to False.
            proc_file_name (str, optional): File name to be assigned to the specified source code. Used only for
                console logging purposes. Defaults to "".

        Returns:
            str: Local output for the processed code. Generated always, regardless of the ``global_output`` argument value.
        """
        if proc_file_name:
            log.msg(f"Processing file '{Path(proc_file_name).name}'.")
        else:
            log.msg(f"Processing source code '{log.get_code_sample(code)}'.")
        log.proc_file_name = proc_file_name
        orig_branch_depth = self.__cond_mngr.branch_depth
        # General code processing.
        code = CodeFormatter.replace_tabs(code)
        # Extraction and processing of directives, comments, whitespaces and other code parts.
        code_input = PreprocInput()
        local_output = PreprocOutput()
        for (code_type, code_part) in code_input.yield_code_parts(code):
            if code_type == CodeType.DIRECTIVE:
                log.msg(f"    Processing directive '{log.get_code_sample(code_part)}'.", 2)
                self.__process_directives(code_part)
            else:
                if self.__cond_mngr.branch_active:
                    if code_type == CodeType.CODE:
                        code_part = self.expand_macros(code_part)
            if global_output:
                self.__output.add_code_part(code_part, code_type)
            local_output.add_code_part(code_part, code_type)
        if self.__cond_mngr.branch_depth != orig_branch_depth:
            log.err("Unterminated #if detected in a previous code (%l).", log.ErrSeverity.CRITICAL)
        return local_output.code_all if full_local_output else local_output.code

    def evaluate(self, expr_code: str) -> object:
        """Evaluates the specified C expression to the numerical value. Only simple C code expressions are supported.
        Ternary operator is not supported. Multiline or other more complex expressions might not be evaluated correctly.

        .. warning::
            Python's ``eval()`` function is used, so this method could be potentially dangerous.

        Args:
            expr_code (str): C code expression to be evaluated.

        Returns:
            any: Value corresponding to the evaluated C expression.
        """
        expr_code = self.__preproc_eval_expr(expr_code)
        # Expression must already be preprocessed, i.e., lines joined, comments removed, macros expanded.
        expr_code = expr_code.replace("&&", " and ").replace("||", " or ").replace("/", "//")
        re.sub(r"!([^?==])", r" not \1", expr_code)
        try:
            # Make eval a little bit safer by removing the import keyword.
            expr_code = expr_code.replace("import", "")
            output = eval(expr_code)    # pylint: disable = eval-used
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            output = False
        return output

    def is_true(self, expr_code: str) -> bool:
        """Evaluates the specified C expression to the boolean true or false value.

        .. warning::
            The limitations and warnings specified for the :py:meth:`neatcpp.NeatCpp.evaluate` method apply also to this method.

        Args:
            expr_code (str): C code expression to be evaluated to the boolean value.

        Returns:
            bool: Boolean value corresponding to the evaluated C expression.
        """
        expr_code = self.__preproc_eval_expr(expr_code)
        state = self.evaluate(expr_code)
        if isinstance(state, str):
            return False
        return bool(state)

    def expand_macros(self, code: str, exp_depth: int = 0) -> str:
        """Expands macro references of known macros in the specified C code.

        Args:
            code (str): C code in which the macro references should be expanded.
            exp_depth (int, optional): Macro expansion depth. Used internally to limit the expansion to 512 levels at maximum
                to avoid potential infinite loops or using too much memory. This parameter should not be changed by the user.
                Defaults to 0.

        Returns:
            str: C code with the expanded macro references.
        """
        exp_code = code
        if exp_depth == 0:
            exp_code = CodeFormatter.remove_line_escapes(exp_code)
        if exp_depth > 512:
            log.err("Macro expansion depth limit 512 exceeded (%l).", log.ErrSeverity.SEVERE)
            return exp_code

        for (macro_id, macro) in self.macros.items():
            macro_start_pos = self.__get_macro_ident_pos(exp_code, macro_id, bool(macro.args))
            while macro_start_pos >= 0 and (not CodeFormatter.is_in_comment(exp_code, macro_start_pos) and
                                            not CodeFormatter.is_in_string(exp_code, macro_start_pos)):
                log.msg(f"    {exp_depth * '    '}Expanding macro '{macro_id}'.", 2)
                macro_end_pos = macro_start_pos + len(macro_id)
                if macro.args:
                    arg_vals = []
                    (args_start_pos, args_end_pos) = CodeFormatter.get_enclosed_subst_pos(exp_code, macro_end_pos)
                    if args_start_pos >= 0:
                        macro_end_pos = args_end_pos + 1
                        arg_vals = self.__extract_macro_ref_args(exp_code[args_start_pos + 1: args_end_pos])
                    req_args_num = len(macro.args) - 1 if macro.args[-1] == "..." else len(macro.args)
                    if len(arg_vals) < req_args_num:
                        log.err(f"{macro_id} macro reference is missing some of its {len(macro.args)} required arguments (%l).",
                                log.ErrSeverity.CRITICAL)
                    # Create a list of fully expanded macro arguments.
                    fully_exp_arg_vals = []
                    for arg_val in arg_vals:
                        exp_arg_val = self.expand_macros(arg_val, exp_depth + 1)
                        fully_exp_arg_vals.append(exp_arg_val)
                    exp_macro_code = macro.expand_args(arg_vals, fully_exp_arg_vals)
                else:
                    exp_macro_code = macro.expand_args()
                # Recursively expand the expanded macro body.
                exp_macro_code = self.expand_macros(exp_macro_code, exp_depth + 1)
                exp_code = self.__insert_expanded_macro(exp_code, macro_start_pos, macro_end_pos, exp_macro_code)
                macro_start_pos = self.__get_macro_ident_pos(exp_code, macro_id, bool(macro.args))
        return exp_code

    # ----- END OF INTERFACE METHODS ----- #

    def __process_directives(self, code: str) -> bool:
        processed = False
        # Process conditional directives to correctly update the brach state stack and
        # detect elif/else for SEARCH branch state.
        for directive in self.__directives[DirectiveGroup.CONDITIONAL]:
            processed = directive.process(code)
            if processed:
                break
        if not processed and self.__cond_mngr.branch_active:
            # Process non-conditional directives in the active conditional branch.
            for directive in self.__directives[DirectiveGroup.STANDARD]:
                processed = directive.process(code)
                if processed:
                    break
        return processed

    def __process_include(self, parts: dict[str, str | None], _code: str) -> None:
        if parts["file"] is not None and parts["file"] not in self.exclude_macros_files:
            orig_log_file_name = log.proc_file_name
            self.process_files(parts["file"], global_output=False)
            log.proc_file_name = orig_log_file_name

    def __process_define(self, parts: dict[str, str | None], code: str) -> None:
        if parts["ident"] is not None:
            ident = parts["ident"]
            if ident not in self.exclude_macros_files:
                args_list = [arg.strip() for arg in parts["args"].split(",")] if parts["args"] is not None else []
                multiline_code = CodeFormatter.remove_line_escapes(code, True)
                # Find the starting position of the macro body, i.e., the last argument position or the end position of the macro ident.
                if args_list:
                    re_match = re.search(rf"{args_list[-1]}\s*\)", multiline_code, re.ASCII)
                else:
                    re_match = re.search(rf"{ident}[ \t]*", multiline_code, re.ASCII)
                if re_match is not None:
                    body = multiline_code[re_match.end():].rstrip()
                    if body.startswith("\n"):
                        body = body[1:]
                        body = dedent(body)
                    else:
                        body = body.lstrip()
                    # if macro has arguments, then insert it at the beginning of the macros dictionary, because if a const macro
                    # is an argument to the func-like macro, the func-like macro needs to be expanded first in the expand_macros method.
                    if args_list:
                        # if macro is already in a dict, then it needs to be deleted, because update function will not change its value.
                        if ident in self.macros:
                            del self.macros[ident]
                        new_macro_dict = {ident: Macro(ident, args_list, body)}
                        new_macro_dict.update(self.macros)
                        self.macros = new_macro_dict
                    else:
                        self.macros[ident] = Macro(ident, args_list, body)
                else:
                    log.err(f"Macro body not detected (%l):\n{code}", log.ErrSeverity.CRITICAL)
        else:
            log.err(f"#define with an unexpected formatting detected (%l):\n{code}", log.ErrSeverity.CRITICAL)

    def __process_undef(self, parts: dict[str, str | None], _code: str) -> None:
        if parts["ident"] is not None and parts["ident"] in self.macros:
            del self.macros[parts["ident"]]

    def __process_if(self, parts: dict[str, str | None], _code: str) -> None:
        is_true = self.is_true(parts["expr"]) if self.__cond_mngr.branch_active and parts["expr"] else False
        self.__cond_mngr.enter_if(is_true)

    def __process_elif(self, parts: dict[str, str | None], _code: str) -> None:
        is_true = self.is_true(parts["expr"]) if self.__cond_mngr.branch_search_active and parts["expr"] else False
        self.__cond_mngr.enter_elif(is_true)

    def __process_else(self, _parts: dict[str, str | None], _code: str) -> None:
        self.__cond_mngr.enter_elif(True)

    def __process_endif(self, _parts: dict[str, str | None], _code: str) -> None:
        self.__cond_mngr.exit_if()

    def __process_ifdef(self, parts: dict[str, str | None], _code: str) -> None:
        expr = parts["expr"].strip() if parts["expr"] else ""
        self.__cond_mngr.enter_if(expr in self.macros)

    def __process_ifndef(self, parts: dict[str, str | None], _code: str) -> None:
        expr = parts["expr"].strip() if parts["expr"] else ""
        self.__cond_mngr.enter_if(expr not in self.macros)

    def __preproc_eval_expr(self, code: str) -> str:
        out_code = self.__eval_defined(code)
        out_code = self.expand_macros(out_code)
        out_code = CodeFormatter.remove_line_escapes(out_code)
        out_code = CodeFormatter.remove_comments(out_code)
        out_code = CodeFormatter.remove_num_type_suffix(out_code)
        # Evaluate defined expressions again in case there are new ones comeing from expanded macros.
        out_code = self.__eval_defined(out_code)
        out_code = CodeFormatter.remove_empty_lines(out_code)
        return out_code

    def __eval_defined(self, code: str) -> str:
        def repl_defined(match: re.Match) -> str:
            ident = match.group("ident")
            return " 1" if ident is not None and ident in self.macros else " 0"

        return re.sub(r"(?:^|[ \t])defined[ \t]*\(?\s*(?P<ident>\w+)[ \t]*\)?",
                      repl_defined, code, count=0, flags=re.ASCII + re.MULTILINE)

    def __get_macro_ident_pos(self, code: str, macro_ident: str, has_args: bool = False) -> int:
        macro_id_pos = -1
        macro_re_ptrn_end = r"\s*\(" if has_args else r"(?:$|[^\w])"
        re_match_macro_id = re.search(rf"(?:^|[^\w])(?P<id>{macro_ident}){macro_re_ptrn_end}", code, re.ASCII + re.MULTILINE)
        if re_match_macro_id is not None:
            macro_id_pos = re_match_macro_id.start("id")
        return macro_id_pos

    def __extract_macro_ref_args(self, args_code: str) -> list[str]:
        args = []
        args_code = args_code.strip().replace("\n", "")
        temp_args = [arg for arg in args_code.split(",")]
        arg_idx = 0
        args.append(temp_args[0])
        for temp_arg in temp_args[1:]:
            # Check if the argument args[arg_idx] does not contain uneven number of parentheses or apostrophes, e.g. "value(1".
            # If yes, then the argument is incomplete and the next argument temp_arg needs to be added to it, e.g. "value(1, 2)".
            if ((args[arg_idx].count("\"") & 1) or (args[arg_idx].count("\'") & 1) or
                    (args[arg_idx].count("(") != args[arg_idx].count(")"))):
                args[arg_idx] = f"{args[arg_idx]}, {temp_arg}"
            else:
                args.append(temp_arg.strip())
                arg_idx += 1
        return args

    def __insert_expanded_macro(self, code: str, macro_ref_start_pos: int, macro_ref_end_pos: int, exp_macro_code: str) -> str:
        out_code = code[:macro_ref_start_pos]
        if "\n" in exp_macro_code:
            # Indent macro body lines 1 and more using the indentation of the code line where the macro is referenced.
            macro_insert_line = "" if out_code.endswith("\n") else out_code
            if "\n" in out_code and not out_code.endswith("\n"):
                macro_insert_line = out_code.splitlines()[-1]
            strip_insert_line = macro_insert_line.lstrip()
            # Get whitespace characters used for the indentation of the code line where the macro is referenced.
            indent_symbols = macro_insert_line[: -len(strip_insert_line)] if strip_insert_line else macro_insert_line
            # Add whitespace indentation characters before each macro body line that isn't empty, starting from the second line.
            exp_macro_code = "\n".join([f"{indent_symbols}{line}".rstrip() if idx > 0 else line
                                        for (idx, line) in enumerate(exp_macro_code.splitlines())])
        out_code = f"{out_code}{exp_macro_code}{code[macro_ref_end_pos:]}"
        return out_code


def run_console_app() -> None:
    argparser = argparse.ArgumentParser(description=CLI_DESCRIPTION, epilog=CLI_EPILOG,
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    argparser.add_argument("in_files", metavar="input_files", type=Path, nargs="+",
                           help="one or more input C source files to be processed into an output file")
    argparser.add_argument("out_file", metavar="output_file", type=Path,
                           help="output file generated from processed input files")
    argparser.add_argument("-i", "--incl_dirs", metavar="incl_dir", type=Path, nargs="+",
                           help="directories to search for included files")
    argparser.add_argument("-s", "--silent", metavar="file", type=Path, nargs="+",
                           help="additional files to be preprocessed first silently without generating an output file")
    argparser.add_argument("-x", "--exclude", metavar="macro_or_file", type=str, nargs="+",
                           help="excluded macros or files for which the #define and #include directives will not be processed")
    argparser.add_argument("-f", "--full_output", action="store_true",
                           help="enable full output, i.e., include directives, all comments and whitespaces in the preprocessor output")
    argparser.add_argument("-v", "--verbosity", metavar="level", type=int, choices=range(3), default=0,
                           help="set console log messages verbosity level 0-2 (0 = log OFF), does not affect error messages")
    argparser.add_argument("-V", "--version", action="version", version=f"{__module_name__} {__version__}")

    args = argparser.parse_args(CLI_DEBUG_ARGS_LIST)

    log.config(args.verbosity)
    neatcpp = NeatCpp()
    if args.incl_dirs is not None:
        neatcpp.add_include_dirs(*args.incl_dirs)
    if args.silent is not None:
        neatcpp.process_files(*args.silent, global_output=False)
    if args.exclude is not None:
        neatcpp.exclude_macros_files = args.exclude
    neatcpp.process_files(*args.in_files, global_output=True)
    neatcpp.save_output_to_file(args.out_file, args.full_output)


if __name__ == "__main__":
    run_console_app()
