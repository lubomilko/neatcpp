import re
from enum import IntEnum
from textwrap import dedent
from typing import Callable
from cpreproc_utils import FileIO, CodeFormatter, CodeSection, Evaluator
from logger import log


class ConditionManager():
    class BranchState(IntEnum):
        ACTIVE = 0  # if/elif/else branch code is enabled and if/elif/else condition is true (active).
        SEARCH = 1  # if/elif/else branch code is enabled and if condition is not true, so search for true elif/else condition.
        IGNORE = 2  # if/elif/else branch code is not enabled, i.e. the condition does not have to be evaluated anymore.

    def __init__(self) -> None:
        self.branch_state: self.BranchState = self.BranchState.ACTIVE
        self.branch_state_stack: list[self.BranchState] = []

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
            log.err("Unexpected #endif detected.")


class CPreprocessor():
    def __init__(self) -> None:
        self.__file_io: FileIO = FileIO()
        self.__dir_proc: DirectiveProcessor = DirectiveProcessor(self)
        self.out_code: str = ""

    def add_include_dirs(self, *dir_paths: str) -> None:
        self.__file_io.add_include_dir(dir_paths)

    def process_file(self, file_path: str) -> None:
        file_code = self.__file_io.read_include_file(file_path)
        self.process_code(file_code)

    def process_code(self, code: str) -> None:
        original_branch_depth = self.__dir_proc.cond_mngr.branch_depth
        code_sect = CodeSection()
        code = CodeFormatter.replace_tabs(code)
        # code = CodeFormatter.remove_comments(code, replace_with_newlines=True)
        # code = CodeFormatter.remove_line_escapes(code, True)
        code_sect.code = code
        for subsect in code_sect.get_next_section():
            if not self.__dir_proc.process_directives(subsect.code):
                if self.__dir_proc.cond_mngr.branch_active:
                    self.out_code = f"{self.out_code}{self.expand_macros(subsect.code)}\n"

        if self.__dir_proc.cond_mngr.branch_depth != original_branch_depth:
            log.err("Unexpected #if detected.")

    def expand_macros(self, code: str) -> str:
        return self.__dir_proc.expand_macros(code)


class Directive():
    def __init__(self, re_ptrn: re.Pattern = None, handler: Callable[[str], None] = None) -> None:
        self.re_ptrn: re.Pattern = re_ptrn
        self.handler: Callable[[str], None] = handler

    def process(self, code: str) -> bool:
        processed = False
        code_lines = code.splitlines()
        re_match = self.re_ptrn.match(code_lines[0])
        if re_match:
            code_lines[0] = code_lines[0][re_match.end():].lstrip()
            self.handler("\n".join(code_lines))
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
        return exp_code


class DirectiveProcessor():
    def __init__(self, parent_cpp: CPreprocessor) -> None:
        self.cpp: CPreprocessor = parent_cpp
        self.cond_mngr: ConditionManager = ConditionManager()
        self.eval: Evaluator = Evaluator()
        self.macros: dict[Macro] = {}
        self.directives: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#\s*define", re.ASCII + re.MULTILINE), self.process_define),
        )
        self.directives_conditional: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#\s*if", re.ASCII + re.MULTILINE), self.process_if),
        )

    def process_directives(self, code: str) -> bool:
        processed = False
        if code and code.splitlines()[0].lstrip().startswith("#"):
            if self.cond_mngr.branch_search_active:
                # Process only conditional directives to correctly update the brach state stack and
                # detect elif/else for SEARCH branch state.
                for directive in self.directives_conditional:
                    processed = directive.process(code)
                    if processed:
                        break
                if self.cond_mngr.branch_active and not processed:
                    # Process non-conditional directives in the active conditional branch.
                    for directive in self.directives:
                        processed = directive.process(code)
                        if processed:
                            break
        return processed

    def expand_macros(self, code: str, exp_depth: int = 0) -> str:
        exp_code = code
        if exp_depth == 0:
            exp_code = CodeFormatter.remove_line_escapes(exp_code)
        if exp_depth > 4096:
            log.err("Macro expansion depth limit 4096 exceeded.")
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
                        arg_vals = self.__extract_macro_ref_args(exp_code[args_start_pos + 1:args_end_pos])
                    if len(arg_vals) < len(macro.args):
                        log.err(f"{macro_id} macro reference is missing some of its {len(macro.args)} arguments.")
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
                exp_code = exp_code[:macro_start_pos] + exp_macro_code + exp_code[macro_end_pos:]
                macro_start_pos = self.__get_macro_ident_pos(exp_code, macro_id, macro.args)
        return exp_code

    def process_define(self, expr_code: str) -> None:
        macro_code = CodeFormatter.remove_line_escapes(expr_code, True)
        re_match = re.match(r"\s*(?P<ident>\w+)(?:\((?P<args>[^\)]*)\))?", macro_code, re.ASCII + re.MULTILINE)
        if re_match is not None:
            ident = re_match.group("ident")
            args = [arg.strip() for arg in re_match.group("args").split(",")] if re_match.group("args") else []
            body = macro_code[re_match.end():].rstrip()
            if body.startswith("\n"):
                body = body[1:]
                body = dedent(body)
            else:
                body = body.lstrip()
            self.macros[ident] = Macro(ident, args, body)
        else:
            log.err(f"#define with an unexpected formatting detected:\n{expr_code}")

    def process_if(self, expr_code: str) -> None:
        expr = self.__preprocess_conditional_expr(expr_code)
        is_true = self.eval.is_true(expr)
        self.cond_mngr.enter_if(is_true)

    def __preprocess_conditional_expr(self, expr_code: str) -> str:
        pass
        # if, elif, ifdef, ifndef
        # TODO: Expand macros (remove comments after each expansion because macro bodies can contain comments).
        # TODO: Evaluate defined(...) to 1 / 0.
        # TODO: Remove comments.
        # TODO: Join escaped lines.

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
