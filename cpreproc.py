from cpreproc_utils import FileManager, TextProcessor, ConditionManager
from logger import log


class CPreprocessor():
    def __init__(self) -> None:
        self.txt_proc: TextProcessor = TextProcessor()
        self.file_mngr: FileManager = FileManager()
        self.cond_mngr: ConditionManager = ConditionManager()

    def include_file(self, file_path: str) -> None:
        file_code = self.file_mngr.read_include_file(file_path)
        self.include_code(file_code)

    def include_code(self, code: str) -> None:
        original_branch_depth = self.cond_mngr.branch_depth

        code_lines = code.splitlines()
        lines_num = len(code_lines)
        line_idx = 0
        while line_idx < lines_num:
            # TODO: Do initial code parsing, i.e., remove comments, optionally join lines, etc.
            line_idx += 1

        if self.cond_mngr.branch_depth != original_branch_depth:
            log.err("Unexpected #if detected.")
