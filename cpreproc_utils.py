import re
from pathlib import Path
from enum import IntEnum
from logger import log


class FileManager():
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


class Evaluator():
    @staticmethod
    def evaluate_expression(expression: str) -> any:
        # TODO: Add expansion of all macros.
        # TODO: Add evaluation of defined(bla) macros.

        expression = expression.replace("&&", " and ").replace("||", " or ").replace("/", "//")
        re.sub(r"!([^?==])", r" not \1", expression)

        try:
            # TODO: Make eval more safe by restricting certain commands or whole imports.
            output = eval(expression)
        except (SyntaxError, NameError, TypeError, ZeroDivisionError):
            output = False

        return output

    def test_expression(self, expression: str) -> bool:
        state = self.evaluate_expression(expression)

        if type(state) is str:
            return False

        return bool(state)


class ConditionManager():
    class BranchState(IntEnum):
        ACTIVE = 0  # if/elif/else branch code is active and if/elif/else condition is true.
        SEARCH = 1  # if/elif/else branch code is active and if condition is not true, so search for true elif/else condition.
        IGNORE = 2  # if/elif/else branch code is not active, i.e. the condition does not have to be evaluated anymore.

    def __init__(self) -> None:
        self.branch_state: self.BranchState = self.BranchState.ACTIVE
        self.branch_state_stack: list[self.BranchState] = []

    @property
    def branch_depth(self) -> int:
        return len(self.branch_state_stack)

    def enter_if(self, expression_flag: bool) -> None:
        self.branch_state_stack.append(self.branch_state)
        if self.branch_state == self.BranchState.ACTIVE:
            if not expression_flag:
                self.branch_state = self.BranchState.SEARCH
        else:
            self.branch_state = self.BranchState.IGNORE

    def enter_elif(self, expression_flag: bool) -> None:
        if self.branch_state == self.BranchState.SEARCH:
            if expression_flag:
                self.branch_state = self.BranchState.ACTIVE
        else:
            self.branch_state = self.BranchState.IGNORE

    def exit_if(self) -> None:
        if self.branch_depth > 0:
            self.branch_state = self.branch_state_stack.pop()
        else:
            log.err("Unexpected #endif detected.")


class TextProcessor():
    def __init__(self) -> None:
        pass

    @staticmethod
    def replace_tabs(code: str, tab_size: int = 4) -> str:
        out_code = ""
        for line in code.splitlines():
            tab_pos = line.find("\t")
            while tab_pos >= 0:
                line.replace("\t", f"{(tab_size - (tab_pos % tab_size)) * ' '}")
                tab_pos = line.find("\t")
            out_code = f"{out_code}\n{line}"
        return out_code
