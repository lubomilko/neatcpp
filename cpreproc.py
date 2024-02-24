from enum import IntEnum
from cpreproc_utils import FileIO, CodeFormatter, CodeSection
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
        return bool(self.branch_state == self.BranchState.SEARCH)

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
        self.__cond_mngr: ConditionManager = ConditionManager()
        self.__formatter: CodeFormatter = CodeFormatter()
        self.output: CodeSection = CodeSection()

    def include_file(self, file_path: str) -> None:
        file_code = self.__file_io.read_include_file(file_path)
        self.parse_code(file_code)

    def include_code(self, code: str) -> None:
        self.parse_code(code)

    def parse_code(self, code: str) -> None:
        original_branch_depth = self.__cond_mngr.branch_depth
        code_sect = CodeSection()
        code = self.__formatter.replace_tabs(code)
        # code = self.__formatter.remove_comments(code, replace_with_newlines=True)
        # code = self.__formatter.remove_line_continuations(code, True)
        code_sect.code = code
        for subsect in code_sect.get_next_section():
            if not self.parse_directives(subsect):
                if self.__cond_mngr.branch_active:
                    # TODO: Expand macros.
                    self.output.append_section(subsect)

        if self.__cond_mngr.branch_depth != original_branch_depth:
            log.err("Unexpected #if detected.")

    def parse_directives(self, code_section: CodeSection) -> bool:
        directive_detected = False
        if code_section.lines[0].lstrip().startswith("#"):
            if self.__cond_mngr.branch_active:
                # if "#define" in code_section.lines[0]:
                #    print(f"Define detected:\n{code_section.code}\n\n")
                # print(f"Directive detected:\n{code_section.code}\n\n")
                # TODO: parse non-conditional directives
                pass
            if self.__cond_mngr.branch_active or self.__cond_mngr.branch_search_active:
                # TODO: Parse only conditional directives to correctly update the brach state stack and
                # detect elif/else for SEARCH branch state.
                pass
            # TODO: Add evaluation of defined(bla) macros.
        return directive_detected
