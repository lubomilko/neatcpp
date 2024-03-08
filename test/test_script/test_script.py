import sys
from pathlib import Path

CURR_DIR_PATH = Path(__file__).parent

sys.path.append(str(Path(CURR_DIR_PATH, "../..").resolve()))

from cpreproc import CPreprocessor


def main() -> None:
    cpp = CPreprocessor()
    cpp.add_include_dirs(
        str(Path(CURR_DIR_PATH, "comp_interpolation", "dep")),
        str(Path(CURR_DIR_PATH, "comp_interpolation", "dep", "comp_util_type")),
        str(Path(CURR_DIR_PATH, "comp_interpolation", "dep", "src_common")),
        str(Path(CURR_DIR_PATH, "comp_interpolation", "src")))

    cpp.process_file(str(Path(CURR_DIR_PATH, "comp_interpolation", "static_analysis", "interpolation_def_in.h")))
    with open(Path(CURR_DIR_PATH, "comp_interpolation", "static_analysis", "interpolation_def.h"), "w", encoding="utf-8") as file:
        file.write(cpp.output_full)
    cpp.reset_output()

    cpp.process_file(str(Path(CURR_DIR_PATH, "comp_interpolation", "static_analysis", "interpolation_def_in.c")))
    with open(Path(CURR_DIR_PATH, "comp_interpolation", "static_analysis", "interpolation_def.c"), "w", encoding="utf-8") as file:
        file.write(cpp.output_full)


if __name__ == "__main__":
    main()
