import re
from pathlib import Path
from .logger import log


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
    RE_PTRN_LINE_CONT = re.compile(r"[ \t]*\\[ \t]*\n", re.ASCII)

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
