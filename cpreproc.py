import re
from enum import IntEnum
from typing import Generator
from textwrap import dedent
from typing import Callable
from pathlib import Path


__all__ = ["CPreprocessor"]


class CodeFormatter():
    RE_PTRN_MLINE_CMNT = re.compile(r"/\*.*?\*/", re.ASCII + re.DOTALL)
    RE_PTRN_SLINE_CMNT = re.compile(r"//[^\n]*", re.ASCII)
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

    def add_include_dir(self, *dir_paths: str) -> None:
        for dir_path in dir_paths:
            incl_dir_path = Path(dir_path).resolve()

            if incl_dir_path.is_file():
                incl_dir_path = incl_dir_path.parent()

            if incl_dir_path.is_dir():
                if incl_dir_path not in self.incl_dir_paths:
                    self.incl_dir_paths.append(incl_dir_path)
            else:
                print(f"ERROR: Include dir path '{dir_path}' not found.")

    def read_include_file(self, file_path: str) -> str:
        for incl_dir_path in self.incl_dir_paths:
            incl_file_path = Path(incl_dir_path, Path(file_path))
            if incl_file_path.is_file():
                with open(incl_file_path, "r", encoding="utf-8") as file:
                    file_code = file.read()
                break
        else:
            print(f"ERROR: Include file path '{file_path}' not found.")
            file_code = ""

        return file_code


class ConditionManager():
    class BranchState(IntEnum):
        ACTIVE = 0  # if/elif/else branch code is enabled and if/elif/else condition is true (active).
        SEARCH = 1  # if/elif/else branch code is enabled and if condition is not true, so search for true elif/else condition.
        IGNORE = 2  # if/elif/else branch code is not enabled, i.e. the condition does not have to be evaluated anymore.

    def __init__(self) -> None:
        self.branch_state: self.BranchState = self.BranchState.ACTIVE
        self.branch_state_stack: list[self.BranchState] = []

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
            print("ERROR: Unexpected #endif detected.")


class CodeType(IntEnum):
    CODE = 0
    DIRECTIVE = 1
    COMMENT = 2
    SPACE = 3


class PreprocInput():
    def get_next_code_part(self, code: str) -> Generator[tuple[CodeType, str], None, None]:
        in_lines = code.splitlines()
        line_idx = 0
        code_lines_num = len(in_lines)
        while line_idx < code_lines_num:
            out_lines = []
            in_line = in_lines[line_idx].rstrip()
            out_lines.append(in_line)
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
                    print("ERROR: Unterminated comment detected.")
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


class Directive():
    def __init__(self, re_ptrn: re.Pattern = None, handler: Callable[[dict[str, str | None], str], None] = None) -> None:
        self.re_ptrn: re.Pattern = re_ptrn
        self.handler: Callable[[dict[str, str | None], str], None] = handler

    def process(self, code: str) -> bool:
        processed = False
        joined_code = CodeFormatter.remove_line_escapes(code)
        re_match = self.re_ptrn.match(joined_code)
        if re_match:
            self.handler(re_match.groupdict(), code)
            processed = True
        return processed


class Macro():
    def __init__(self, identifier: str = "", args: list[str] = [], body: str = "") -> None:
        self.identifier: str = identifier
        self.args: list[str] = args
        self.body: str = body

    def expand_args(self, arg_vals: list[str] = [], fully_exp_arg_vals: list[str] = []) -> str:
        exp_code = self.body
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
                # If argument value is specified, then use it. Otherwise use empty string (not enough parameters given in macro reference).
                arg_val = arg_vals[arg_idx] if arg_idx < len(arg_vals) else ""
                fully_exp_arg_val = fully_exp_arg_vals[arg_idx] if arg_idx < len(fully_exp_arg_vals) else ""
            # Perform concatenatenation of macro arguments specified by the ## operator.
            exp_code = re.sub(rf"[\s\\]*##[\s\\]*{arg_name}", rf"{arg_val}", exp_code, 0, re.ASCII + re.MULTILINE)
            exp_code = re.sub(rf"{arg_name}[\s\\]*##[\s\\]*", rf"{arg_val}", exp_code, 0, re.ASCII + re.MULTILINE)
            # Perform stringification specified by the # operator.
            exp_code = re.sub(rf"(^|[^#])#\s*{arg_name}($|[^\w])", rf'\g<1>"{arg_val}"\g<2>', exp_code, 0, re.ASCII + re.MULTILINE)
            # Replace the macro argument in macro body with the fully expanded argument value.
            exp_code = re.sub(rf"(^|[^\w]){arg_name}($|[^\w])", rf"\g<1>{fully_exp_arg_val}\g<2>", exp_code, 0, re.ASCII + re.MULTILINE)
        # Perform remaining concatenatenations specified by the ## operator by removing the operator and its surrounding spaces.
        exp_code = re.sub(r"[\s\\]*##[\s\\]*", "", exp_code, 0, re.ASCII + re.MULTILINE)
        # Perform an lstrip in case some of the expanded arguments are empty and generate a whitespace at the beginning of the macro body.
        return exp_code.lstrip()


class CPreprocessor():
    def __init__(self) -> None:
        self.__file_io: FileIO = FileIO()
        self.__output: PreprocOutput = PreprocOutput()
        self.__cond_mngr: ConditionManager = ConditionManager()
        self.__directives: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#[ \t]*define[ \t]+(?P<ident>\w+)(?:\((?P<args>[^\)]*)\))?", re.ASCII), self.__process_define),
            Directive(re.compile(r"^[ \t]*#[ \t]*undef[ \t]+(?P<ident>\w+)", re.ASCII), self.__process_undef),
            Directive(re.compile(r"^[ \t]*#[ \t]*include[ \t]+(?:\"|<)(?P<file>[^\">]+)(?:\"|>)", re.ASCII), self.__process_include)
        )
        self.__directives_conditional: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#[ \t]*if[ \t]+(?P<expr>.*)", re.ASCII), self.__process_if),
            Directive(re.compile(r"^[ \t]*#[ \t]*elif[ \t]+(?P<expr>.*)", re.ASCII), self.__process_elif),
            Directive(re.compile(r"^[ \t]*#[ \t]*else(?:\s|$)", re.ASCII), self.__process_else),
            Directive(re.compile(r"^[ \t]*#[ \t]*endif(?:\s|$)", re.ASCII), self.__process_endif),
            Directive(re.compile(r"^[ \t]*#[ \t]*ifdef[ \t]+(?P<expr>.*)", re.ASCII), self.__process_ifdef),
            Directive(re.compile(r"^[ \t]*#[ \t]*ifndef[ \t]+(?P<expr>.*)", re.ASCII), self.__process_ifndef)
        )
        self.macros: dict[Macro] = {}

    @property
    def output(self) -> str:
        return self.__output.code

    @property
    def output_full(self) -> str:
        return self.__output.code_all

    def reset(self) -> None:
        self.__file_io.reset()
        self.__output.reset()
        self.__cond_mngr.reset()
        self.macros = {}

    def add_include_dirs(self, *dir_paths: str) -> None:
        self.__file_io.add_include_dir(*dir_paths)

    def process_file(self, file_path: str, generate_output: bool = True) -> None:
        file_code = self.__file_io.read_include_file(file_path)
        if file_code:
            self.process_code(file_code, generate_output)

    def process_code(self, code: str, generate_output: bool = True) -> None:
        original_branch_depth = self.__cond_mngr.branch_depth
        code = CodeFormatter.replace_tabs(code)
        # code = CodeFormatter.remove_comments(code, replace_with_newlines=True)
        # code = CodeFormatter.remove_line_escapes(code, True)
        input = PreprocInput()
        for (code_type, code_part) in input.get_next_code_part(code):
            if code_type == CodeType.DIRECTIVE:
                self.__process_directives(code_part)
            else:
                if self.__cond_mngr.branch_active:
                    if code_type == CodeType.CODE:
                        code_part = self.expand_macros(code_part)
            if generate_output:
                self.__output.add_code_part(code_part, code_type)

        if self.__cond_mngr.branch_depth != original_branch_depth:
            print("ERROR: Unexpected #if detected.")

    def evaluate(self, expr_code: str) -> any:
        expr_code = self.__preproc_eval_expr(expr_code)
        # Expression must already be preprocessed, i.e., lines joined, comments removed, macros expanded.
        expr_code = expr_code.replace("&&", " and ").replace("||", " or ").replace("/", "//")
        re.sub(r"!([^?==])", r" not \1", expr_code)
        try:
            # TODO: Make eval more safe by restricting certain commands or whole imports.
            output = eval(expr_code)
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            output = False
        return output

    def is_true(self, expr_code: str) -> bool:
        expr_code = self.__preproc_eval_expr(expr_code)
        state = self.evaluate(expr_code)
        if type(state) is str:
            return False
        return bool(state)

    def expand_macros(self, code: str, exp_depth: int = 0) -> str:
        exp_code = code
        if exp_depth == 0:
            exp_code = CodeFormatter.remove_line_escapes(exp_code)
        if exp_depth > 4096:
            print("ERROR: Macro expansion depth limit 4096 exceeded.")
            return exp_code

        for (macro_id, macro) in self.macros.items():
            macro_start_pos = self.__get_macro_ident_pos(exp_code, macro_id, macro.args)
            while macro_start_pos >= 0 and (not CodeFormatter.is_in_comment(exp_code, macro_start_pos) and
                                            not CodeFormatter.is_in_string(exp_code, macro_start_pos)):
                macro_end_pos = macro_start_pos + len(macro_id)
                if macro.args:
                    arg_vals = []
                    (args_start_pos, args_end_pos) = CodeFormatter.get_enclosed_subst_pos(exp_code, macro_end_pos)
                    if args_start_pos >= 0:
                        macro_end_pos = args_end_pos + 1
                        arg_vals = self.__extract_macro_ref_args(exp_code[args_start_pos + 1: args_end_pos])
                    if len(arg_vals) < len(macro.args):
                        print(f"ERROR: {macro_id} macro reference is missing some of its {len(macro.args)} arguments.")
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
                macro_start_pos = self.__get_macro_ident_pos(exp_code, macro_id, macro.args)
        return exp_code

    def __process_directives(self, code: str) -> bool:
        processed = False
        # Process conditional directives to correctly update the brach state stack and
        # detect elif/else for SEARCH branch state.
        for directive in self.__directives_conditional:
            processed = directive.process(code)
            if processed:
                break
        if not processed and self.__cond_mngr.branch_active:
            # Process non-conditional directives in the active conditional branch.
            for directive in self.__directives:
                processed = directive.process(code)
                if processed:
                    break
        return processed

    def __process_include(self, parts: dict[str, str | None], code: str) -> None:
        if parts["file"] is not None:
            self.process_file(parts["file"], False)

    def __process_define(self, parts: dict[str, str | None], code: str) -> None:
        if parts["ident"] is not None:
            ident = parts["ident"]
            args_list = [arg.strip() for arg in parts["args"].split(",")] if parts["args"] is not None else []

            multiline_code = CodeFormatter.remove_line_escapes(code, True)
            # Find the starting position of the macro body, i.e., the last argument position or the end position of the macro identifier.
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
                self.macros[ident] = Macro(ident, args_list, body)
            else:
                print(f"ERROR: Macro body not detected:\n{code}")
        else:
            print(f"ERROR: #define with an unexpected formatting detected:\n{code}")

    def __process_undef(self, parts: dict[str, str | None], code: str) -> None:
        if parts["ident"] is not None and parts["ident"] in self.macros:
            del self.macros[parts["ident"]]

    def __process_if(self, parts: dict[str, str | None], code: str) -> None:
        is_true = self.is_true(parts["expr"]) if self.__cond_mngr.branch_active else False
        self.__cond_mngr.enter_if(is_true)

    def __process_elif(self, parts: dict[str, str | None], code: str) -> None:
        is_true = self.is_true(parts["expr"]) if self.__cond_mngr.branch_search_active else False
        self.__cond_mngr.enter_elif(is_true)

    def __process_else(self, parts: dict[str, str | None], code: str) -> None:
        self.__cond_mngr.enter_elif(True)

    def __process_endif(self, parts: dict[str, str | None], code: str) -> None:
        self.__cond_mngr.exit_if()

    def __process_ifdef(self, parts: dict[str, str | None], code: str) -> None:
        self.__cond_mngr.enter_if(parts["expr"] in self.macros)

    def __process_ifndef(self, parts: dict[str, str | None], code: str) -> None:
        self.__cond_mngr.enter_if(parts["expr"] not in self.macros)

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
                      repl_defined, code, 0, re.ASCII + re.MULTILINE)

    def __get_macro_ident_pos(self, code: str, macro_ident: str, has_args: bool = False) -> int:
        macro_id_pos = -1
        macro_re_ptrn_end = r"\s*\(" if has_args else r"(?:$|[^\w])"
        re_match_macro_id = re.search(rf"(?:^|[^\w])(?P<id>{macro_ident}){macro_re_ptrn_end}", code, re.ASCII + re.MULTILINE)
        if re_match_macro_id is not None:
            macro_id_pos = re_match_macro_id.start("id")
        return macro_id_pos

    def __extract_macro_ref_args(self, args_code: str) -> list[str]:
        args = []
        if args_code:
            args_code = args_code.strip().replace("\n", "")
            temp_args = [arg for arg in args_code.split(",")]
            arg_idx = 0
            args.append(temp_args[0])
            for temp_arg in temp_args[1:]:
                if ((args[arg_idx].count("\"") & 1) or (args[arg_idx].count("\'") & 1) or
                        (args[arg_idx].count("(") != args[arg_idx].count(")"))):
                    args[arg_idx] += temp_arg
                else:
                    args.append(temp_arg.strip())
                    arg_idx += 1
        return args

    def __insert_expanded_macro(self, code: str, macro_ref_start_pos: int, macro_ref_end_pos: int, exp_macro_code: str) -> str:
        out_code = code[:macro_ref_start_pos]
        if "\n" in exp_macro_code:
            # Indent macro body lines 1 and more using the indentation of the code line where the macro is referenced.
            macro_insert_line = out_code.splitlines()[-1] if "\n" in out_code else out_code
            strip_insert_line = macro_insert_line.lstrip()
            # Get whitespace characters used for the indentation of the code line where the macro is referenced.
            indent_symbols = macro_insert_line[: -len(strip_insert_line)] if strip_insert_line else macro_insert_line
            # Add whitespace indentation characters before each macro body line that isn't empty, starting from the second line.
            exp_macro_code = "\n".join([f"{indent_symbols}{line}".rstrip() if idx > 0 else line
                                        for (idx, line) in enumerate(exp_macro_code.splitlines())])
        out_code = f"{out_code}{exp_macro_code}{code[macro_ref_end_pos:]}"
        return out_code


def main() -> None:
    pass


if __name__ == "__main__":
    main()
