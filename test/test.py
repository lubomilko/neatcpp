import sys
from pathlib import Path

CURR_DIR_PATH = str(Path(__file__).parent)

sys.path.append(str(Path(CURR_DIR_PATH, "..").resolve()))


from cpreproc import CPreprocessor


def remove_write_compare_file(out_file: Path, text: str, comp_file: Path) -> None:
    try:
        Path(out_file).unlink()
    except FileNotFoundError:
        pass
    with open(out_file, "w", encoding="utf-8") as file:
        file.write(text)
    out_str = ""
    exp_str = ""
    with open(out_file, "r", encoding="utf-8") as file:
        out_str = file.read()
    with open(comp_file, "r", encoding="utf-8") as file:
        exp_str = file.read()

    if out_str == exp_str:
        print(f"OK: Generated output file '{out_file.name}' matches "
              f"the expected output file '{comp_file.name}'.")
    else:
        print(f"ERROR: Generated output file '{out_file.name}' does not match the "
              f"expected output file '{comp_file.name}'.")


def main() -> None:
    cpp = CPreprocessor()
    cpp.process_file(f"{CURR_DIR_PATH}/src1.c")
    remove_write_compare_file(Path(CURR_DIR_PATH, "src1_out.c"), cpp.output, Path(CURR_DIR_PATH, "src1_exp.c"))

    cpp = CPreprocessor()
    cpp.add_include_dirs(f"{CURR_DIR_PATH}/incl_common")
    cpp.process_file(f"{CURR_DIR_PATH}/src2.c")
    remove_write_compare_file(Path(CURR_DIR_PATH, "src2_out.c"), cpp.output, Path(CURR_DIR_PATH, "src2_exp.c"))

    cpp = CPreprocessor()
    cpp.add_include_dirs(f"{CURR_DIR_PATH}/incl_hstgr", f"{CURR_DIR_PATH}/incl_common")
    cpp.process_file(f"{CURR_DIR_PATH}/src3.c")
    remove_write_compare_file(Path(CURR_DIR_PATH, "src3_out.c"), cpp.output, Path(CURR_DIR_PATH, "src3_exp.c"))

    cpp = CPreprocessor()
    cpp.process_file(f"{CURR_DIR_PATH}/src4.c")
    remove_write_compare_file(Path(CURR_DIR_PATH, "src4_out.c"), cpp.output, Path(CURR_DIR_PATH, "src4_exp.c"))


if __name__ == "__main__":
    main()
