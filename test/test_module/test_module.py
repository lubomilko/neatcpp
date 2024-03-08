import pytest
import sys
from pathlib import Path

CURR_DIR_PATH = Path(__file__).parent

sys.path.append(str(Path(CURR_DIR_PATH, "../..").resolve()))


from cpreproc import CPreprocessor


TEST_PROCESS_FILE_PARAMS = [
    (Path(CURR_DIR_PATH, "test_srcs", "src1.c"),
     Path(CURR_DIR_PATH, "test_srcs", "src1_exp.c"),
     ()),

    (Path(CURR_DIR_PATH, "test_srcs", "src2.c"),
     Path(CURR_DIR_PATH, "test_srcs", "src2_exp.c"),
     (Path(CURR_DIR_PATH, "incl_common"),)),

    (Path(CURR_DIR_PATH, "test_srcs", "src3.c"),
     Path(CURR_DIR_PATH, "test_srcs", "src3_exp.c"),
     (Path(CURR_DIR_PATH, "incl_common"), Path(CURR_DIR_PATH, "incl_hstgr"))),

    (Path(CURR_DIR_PATH, "test_srcs", "src4.c"),
     Path(CURR_DIR_PATH, "test_srcs", "src4_exp.c"),
     ())]


@pytest.mark.parametrize("in_file, exp_out_file, incl_dirs", TEST_PROCESS_FILE_PARAMS)
def test_process_file(in_file: Path, exp_out_file: Path, incl_dirs: tuple[Path]) -> None:
    cpp = CPreprocessor()
    if incl_dirs:
        cpp.add_include_dirs(*incl_dirs)
    cpp.process_file(f"{in_file}")
    proc_output = cpp.output

    # Save processed output into *_out file for debugging purposes.
    with open(Path(in_file.parent, f"{in_file.stem}_out.{in_file.suffix}"), "w", encoding="utf-8") as file:
        file.write(proc_output)

    # Read file containing the expected processed output.
    exp_output = ""
    with open(exp_out_file, "r", encoding="utf-8") as file:
        exp_output = file.read()

    # Assert that the processed output is going to be the same as the expected output.
    assert proc_output == exp_output
