import re
from enum import IntEnum
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
        self.__dir_proc: DirectiveProcessor = DirectiveProcessor()
        self.output: CodeSection = CodeSection()

    def add_include_dirs(self, *dir_paths: str) -> None:
        self.__file_io.add_include_dir(dir_paths)

    def process_file(self, file_path: str) -> None:
        file_code = self.__file_io.read_include_file(file_path)
        self.parse_code(file_code)

    def process_code(self, code: str) -> None:
        original_branch_depth = self.__dir_proc.cond_mngr.branch_depth
        code_sect = CodeSection()
        code = CodeFormatter.replace_tabs(code)
        # code = CodeFormatter.remove_comments(code, replace_with_newlines=True)
        # code = CodeFormatter.remove_line_escapes(code, True)
        code_sect.code = code
        for subsect in code_sect.get_next_section():
            if not self.__dir_proc.process_directives(subsect):
                if self.__dir_proc.cond_mngr.branch_active:
                    # TODO: Expand macros.
                    if len(subsect.lines) > 1:
                        print(f"{subsect.code}\n\n")
                    self.output.append_section(subsect)

        if self.__dir_proc.cond_mngr.branch_depth != original_branch_depth:
            log.err("Unexpected #if detected.")


class Directive():
    def __init__(self, re_ptrn: re.Pattern = None, handler: callable[[CodeSection], None] = None) -> None:
        self.re_ptrn: re.Pattern = re_ptrn
        self.handler: callable[[CodeSection], None] = handler

    def process(self, code_section: CodeSection) -> bool:
        processed = False
        re_match = self.re_ptrn.match(code_section.lines[0])
        if re_match:
            code_section.lines[0] = code_section.lines[0][re_match.end():].lstrip()
            self.handler(code_section)
            processed = True
        return processed


class Macro():
    def __init__(self, identifier: str = "", args: list[str] = [], body: str = "") -> None:
        self.identifier: str = identifier
        self.args: list[str] = args
        self.body: str = body

    def expand_args(self, *args: str) -> str:
        exp_code = self.body
        for (arg_idx, arg_name) in enumerate(self.args):
            # If argument value is specified, then use it. Otherwise use empty string.
            arg_val = args[arg_idx] if arg_idx < len(args) else ""
            # Replace all macro arguments in macro body with argument values.
            exp_code = re.sub(rf"([^\w]){arg_name}([^\w])", rf"\g<1>{arg_val}\g<2>", exp_code, 0, re.ASCII + re.MULTILINE)
        # Remove all string concatenations "##" .
        exp_code = re.sub(r"([\s\\]*##[\s\\]*)", "", exp_code, 0, re.ASCII + re.MULTILINE)
        return exp_code


class DirectiveProcessor():
    def __init__(self, parent_cpp: CPreprocessor) -> None:
        self.cpp: CPreprocessor = parent_cpp
        self.cond_mngr: ConditionManager = ConditionManager()
        self.eval: Evaluator = Evaluator()
        self.directives: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#\s*define", re.ASCII + re.DOTALL), self.process_define)
        )
        self.directives_conditional: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#\s*if", re.ASCII + re.DOTALL), self.process_if)
        )

    def process_directives(self, code_section: CodeSection) -> bool:
        processed = False
        if code_section.lines[0].lstrip().startswith("#"):
            if self.cond_mngr.branch_search_active:
                # Process only conditional directives to correctly update the brach state stack and
                # detect elif/else for SEARCH branch state.
                for directive in self.directives_conditional:
                    processed = directive.process(code_section)
                    if processed:
                        break
            elif self.cond_mngr.branch_active:
                # if "#define" in code_section.lines[0]:
                #    print(f"Define detected:\n{code_section.code}\n\n")
                # print(f"Directive detected:\n{code_section.code}\n\n")
                # TODO: parse non-conditional directives
                pass
            # TODO: Add evaluation of defined(bla) macros.
        return processed

    def process_define(self, expr_section: CodeSection) -> None:
        ident_args_code = CodeFormatter.remove_comments(expr_section.code)
        ident_args_code = CodeFormatter.remove_line_escapes(ident_args_code)
        # TODO: Extract macro identifier, arguments and body.

    def process_if(self, expr_section: CodeSection) -> None:
        expr = self.preprocess_conditional_expr(expr_section)
        # TODO: Evaluate defined(...) to 1 / 0.
        is_true = self.eval.is_true(expr)
        self.cond_mngr.enter_if(is_true)

    def preprocess_conditional_expr(self, expr_section: CodeSection) -> str:
        pass
        # if, elif, ifdef, ifndef
        # TODO: Remove comments.
        # TODO: Expand macros (remove comments after each expansion because macro bodies can contain comments).
        # TODO: Join escaped lines.
