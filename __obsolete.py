class CommentReplaceOption(IntEnum):
    KEEP_ALL = 0
    KEEP_1SPACE = 1
    KEEP_SPACES_NEWLINES = 2
    REPL_NEWLINES = 3


@dataclass
class CodeFormatConfig:
    join_cont_lines: bool = False
    repl_tabs: bool = True
    tab_size: int = 4
    repl_cmtns: CommentReplaceOption = CommentReplaceOption.REPL_NEWLINES


def preformat_code(self, code: str, config: CodeFormatConfig) -> str:
    if config.repl_tabs:
        code = self.replace_tabs(code, config.tab_size)
    if config.join_cont_lines:
        code = self.remove_line_continuations(code)
    if config.repl_cmtns == config.CommentReplaceOption.KEEP_1SPACE:
        code = self.remove_comments(code)
    elif config.repl_cmtns == config.CommentReplaceOption.KEEP_SPACES_NEWLINES:
        code = self.remove_comments(code, replace_with_spaces=True)
    elif config.repl_cmtns == config.CommentReplaceOption.REPL_NEWLINES:
        code = self.remove_comments(code, replace_with_newlines=True)


    @staticmethod
    def replace_comments_with_tags(code: str, tag_multiline_comment: str, tag_singleline_comment: str) -> list[str]:

        out_code = code
        out_code = CodeFormatter.RE_PTRN_MLINE_CMNT.sub(__repl_mline_cmnt, out_code)
        out_code = CodeFormatter.RE_PTRN_SLINE_CMNT.sub(__repl_sline_cmnt, out_code)
        
        return out_code