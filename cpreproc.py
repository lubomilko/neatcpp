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
                    self.expand_macros(subsect.code)
                    if len(subsect.lines) > 1:
                        print(f"{subsect.code}\n\n")
                    self.output.append_section(subsect)

        if self.__dir_proc.cond_mngr.branch_depth != original_branch_depth:
            log.err("Unexpected #if detected.")

    def expand_macros(self, code: str) -> str:
        return self.__dir_proc.expand_macros(code)


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
            # Perform stringifications specified by the # operator.
            exp_code = re.sub(rf"(\s+)#\s*{arg_name}([^\w])", rf"\g<1>\"{arg_val}\"\g<2>", exp_code, 0, re.ASCII + re.MULTILINE)
            # Replace all macro arguments in macro body with argument values.
            exp_code = re.sub(rf"([^\w]){arg_name}([^\w])", rf"\g<1>{arg_val}\g<2>", exp_code, 0, re.ASCII + re.MULTILINE)
        # Perform concatenatenations specified by the ## operator by removing the operator and its surrounding spaces.
        exp_code = re.sub(r"([\s\\]*##[\s\\]*)", "", exp_code, 0, re.ASCII + re.MULTILINE)
        return exp_code


class DirectiveProcessor():
    def __init__(self, parent_cpp: CPreprocessor) -> None:
        self.cpp: CPreprocessor = parent_cpp
        self.cond_mngr: ConditionManager = ConditionManager()
        self.eval: Evaluator = Evaluator()
        self.macros: dict[Macro] = {}
        self.directives: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#\s*define", re.ASCII + re.MULTILINE), self.process_define)
        )
        self.directives_conditional: tuple[Directive] = (
            Directive(re.compile(r"^[ \t]*#\s*if", re.ASCII + re.MULTILINE), self.process_if)
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
                if self.cond_mngr.branch_active and not processed:
                    # Process non-conditional directives in the active conditional branch.
                    for directive in self.directives:
                        processed = directive.process(code_section)
                        if processed:
                            break
        return processed

    def expand_macros(self, code: str, exp_depth: int = 0) -> None:
        if exp_depth == 0:
            code = CodeFormatter.remove_line_escapes(code)
        if exp_depth > 4096:
            log.err("Macro expansion depth limit 4096 exceeded.")

        for (macro_ident, macro) in self.macros.items():
            macro_id_pos = code.find(macro_ident)
            while macro_id_pos >= 0 and (not CodeFormatter.is_in_comment(code, macro_id_pos) and
                                         not CodeFormatter.is_in_string(code, macro_id_pos)):
                if macro.args:
                    
                else:

                macro_id_pos = code.find(macro_ident)

    def process_define(self, expr_section: CodeSection) -> None:
        macro_code = CodeFormatter.remove_line_escapes(expr_section.code, True)
        re_match = re.match(r"\s*(?P<ident>\w+)(?P<args>\([^\)]*\))?", macro_code, re.ASCII + re.MULTILINE)
        if re_match is not None:
            ident = re_match.group("ident")
            args = [arg.strip() for arg in re_match.group("args").split(",")]
            body = macro_code[re_match.end():].lstrip()
            self.macros[ident] = Macro(ident, args, body)
        else:
            log.err(f"#define with an unexpected formatting detected:\n{expr_section.lines[0]}...")

    def process_if(self, expr_section: CodeSection) -> None:
        expr = self.preprocess_conditional_expr(expr_section)
        is_true = self.eval.is_true(expr)
        self.cond_mngr.enter_if(is_true)

    def preprocess_conditional_expr(self, expr_section: CodeSection) -> str:
        pass
        # if, elif, ifdef, ifndef
        # TODO: Expand macros (remove comments after each expansion because macro bodies can contain comments).
            # TODO: Evaluate defined(...) to 1 / 0.
        # TODO: Remove comments.
        # TODO: Join escaped lines.
