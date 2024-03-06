import sys
from pathlib import Path

CURR_DIR_PATH = str(Path(__file__).parent)

sys.path.append(str(Path(CURR_DIR_PATH, "..").resolve()))


from cpreproc.cpreproc import CPreprocessor


def compare_output(generated_file: Path, expected_file: Path) -> None:
    gen_str = ""
    exp_str = ""
    with open(generated_file, "r", encoding="utf-8") as file:
        gen_str = file.read()
    with open(expected_file, "r", encoding="utf-8") as file:
        exp_str = file.read()

    if gen_str == exp_str:
        print(f"OK: Generated output file '{generated_file.name}' matches "
              f"the expected output file '{expected_file.name}'.")
    else:
        print(f"ERROR: Generated output file '{generated_file.name}' does not match the "
              f"expected output file '{expected_file.name}'.")
    

def main() -> None:
    cpp = CPreprocessor()
    cpp.process_file(f"{CURR_DIR_PATH}/src1.c")
    with open(f"{CURR_DIR_PATH}/src1_out.c", "w", encoding="utf-8") as file:
        file.write(cpp.output)
    compare_output(Path(CURR_DIR_PATH, "src1_out.c"), Path(CURR_DIR_PATH, "src1_exp.c"))

    cpp = CPreprocessor()
    cpp.process_file(f"{CURR_DIR_PATH}/src2.c")
    with open(f"{CURR_DIR_PATH}/src2_out.c", "w", encoding="utf-8") as file:
        file.write(cpp.output)
    compare_output(Path(CURR_DIR_PATH, "src2_out.c"), Path(CURR_DIR_PATH, "src2_exp.c"))

    cpp = CPreprocessor()
    cpp.process_file(f"{CURR_DIR_PATH}/src3.c")
    with open(f"{CURR_DIR_PATH}/src3_out.c", "w", encoding="utf-8") as file:
        file.write(cpp.output)
    compare_output(Path(CURR_DIR_PATH, "src3_out.c"), Path(CURR_DIR_PATH, "src3_exp.c"))


if __name__ == "__main__":
    main()
