import re
from pathlib import Path
from typing import Generator
from logger import log


class FileIO():
    def __init__(self) -> None:
        self.incl_dir_paths: list[Path] = [Path("")]

    def add_include_dir(self, *dir_paths: str) -> None:
        for dir_path in dir_paths:
            incl_dir_path = Path(dir_path).resolve()

            if incl_dir_path.is_file():
                incl_dir_path = incl_dir_path.parent()

            if incl_dir_path.is_dir():
                if incl_dir_path not in self.incl_dir_paths:
                    self.incl_dir_paths.append(incl_dir_path)
            else:
                log.err(f"Include dir path '{dir_path}' not found.")

    def read_include_file(self, file_path: str) -> str:
        for incl_dir_path in self.incl_dir_paths:
            incl_file_path = Path(incl_dir_path, Path(file_path))
            if incl_file_path.is_file():
                with open(incl_file_path, "r", encoding="utf-8") as file:
                    file_code = file.read()
                break
        else:
            log.err(f"Include file path '{file_path}' not found.")
            file_code = ""

        return file_code


class CodeFormatter():
    RE_PTRN_MLINE_CMNT = re.compile(r"/\*.*?\*/", re.ASCII + re.DOTALL)
    RE_PTRN_SLINE_CMNT = re.compile(r"//[^\n]*", re.ASCII)

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
    def remove_line_continuations(code: str, keep_newlines: bool = False) -> str:
        out_code = ""
        for line in code.splitlines():
            if line.rstrip().endswith("\\"):
                line = line[: -1].rstrip()
                if keep_newlines:
                    out_code = f"{out_code}{line}\n"
                else:
                    line = line.lstrip()
                    out_code = f"{out_code}{line} "
            else:
                out_code = f"{out_code}{line}\n"
        return out_code

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


class CodeSection():
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.line_idx: int = 0
        self.has_escaped_lines: bool = False
        self.has_multiline_comment: bool = False

    @property
    def code(self) -> str:
        return "\n".join(self.lines)

    @code.setter
    def code(self, code: str) -> None:
        self.lines = code.splitlines()
        self.line_idx = 0

    def get_next_section(self) -> Generator["CodeSection", None, None]:
        code_lines_num = len(self.lines)
        while self.line_idx < code_lines_num:
            out = CodeSection()
            line = self.lines[self.line_idx].rstrip()
            out.lines.append(line)
            self.line_idx += 1
            # Detect and extract continuous line split to lines ending with "\".
            if line.endswith("\\"):
                while self.line_idx < code_lines_num:
                    line = self.lines[self.line_idx].rstrip()
                    out.lines.append(line)
                    self.line_idx += 1
                    if not line.endswith("\\"):
                        break
                out.has_escaped_lines = True
            # Detect and extract multiline comment.
            if "/*" in line and "*/" not in line:
                while self.line_idx < code_lines_num:
                    line = self.lines[self.line_idx].rstrip()
                    out.lines.append(line)
                    self.line_idx += 1
                    if "*/" in line:
                        break
                else:
                    log.err("Unterminated comment detected.")
                out.has_multiline_comment = True
            yield out

    def append_section(self, new_section: "CodeSection") -> None:
        self.lines.extend(new_section.lines)


class Evaluator():
    @staticmethod
    def evaluate(expression: str) -> any:
        # Expression must already be preprocessed, i.e., lines joined, comments removed, macros expanded.
        expression = expression.replace("&&", " and ").replace("||", " or ").replace("/", "//")
        re.sub(r"!([^?==])", r" not \1", expression)

        try:
            # TODO: Make eval more safe by restricting certain commands or whole imports.
            output = eval(expression)
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            output = False

        return output

    def is_true(self, expression: str) -> bool:
        state = self.evaluate(expression)

        if type(state) is str:
            return False

        return bool(state)
