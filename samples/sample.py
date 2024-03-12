from pathlib import Path
import sys


CURR_DIR_PATH = Path(__file__).parent

sys.path.append(str(Path(CURR_DIR_PATH, "../src").resolve()))


from pycpp import PyCpp     # noqa: E402


def main() -> None:
    cpp = PyCpp()
    cpp.process_files(Path(CURR_DIR_PATH, "sample_src.c"))
    cpp.save_output_to_file(Path(CURR_DIR_PATH, "sample_src_out.c"))


if __name__ == "__main__":
    main()
