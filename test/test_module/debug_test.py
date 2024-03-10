import sys
from pathlib import Path

CURR_DIR_PATH = Path(__file__).parent

sys.path.append(str(Path(CURR_DIR_PATH, "../../src").resolve()))


from pycpp import PyCpp     # noqa: E402


def main() -> None:
    in_file_path = Path(CURR_DIR_PATH, "test_srcs", "src2.c")
    out_file_path = Path(in_file_path.parent, f"{in_file_path.stem}_out.{in_file_path.suffix}")
    out_file_path.unlink(out_file_path)

    cpp = PyCpp()
    cpp.add_include_dirs(Path(CURR_DIR_PATH, "incl_common"))
    cpp.process_file(str(in_file_path))
    cpp.save_output_to_file(str(out_file_path))


if __name__ == "__main__":
    main()
