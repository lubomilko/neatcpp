from pathlib import Path
import sys
import pytest


CURR_DIR_PATH = Path(__file__).parent

sys.path.append(str(Path(CURR_DIR_PATH, "../src").resolve()))


from pycpp import PyCpp             # noqa: E402
from pycpp import run_console_app   # noqa: E402


def compare_files(gen_file: Path, exp_file: Path) -> bool:
    files_match = False
    with open(gen_file, "r", encoding="utf-8") as file_gen, open(exp_file, "r", encoding="utf-8") as file_exp:
        if file_gen.read() == file_exp.read():
            files_match = True
        else:
            print(f"ERROR: File '{gen_file}' does not match the expected file '{exp_file}'.")
    return files_match


@pytest.fixture(scope="session")
def pycpp():
    pycpp = PyCpp()
    return pycpp


TEST_PARAMS = [
    ((),
     ["IGN_MACRO_OBJ", "IGN_MACRO_FUNC"],
     (),
     (Path(CURR_DIR_PATH, "c_files", "src1.c"),),
     Path(CURR_DIR_PATH, "c_files", "src1_out.c"),
     Path(CURR_DIR_PATH, "c_files", "src1_exp.c"),
     False),
    ((Path(CURR_DIR_PATH, "c_files", "incl"),),
     ["stdint.h"],
     (),
     (Path(CURR_DIR_PATH, "c_files", "src2.c"),),
     Path(CURR_DIR_PATH, "c_files", "src2_out.c"),
     Path(CURR_DIR_PATH, "c_files", "src2_exp.c"),
     True)]


@pytest.mark.parametrize("incl_dirs, excludes, files_silent, files_in, file_out, file_exp, full_output", TEST_PARAMS)
def test_module(pycpp: PyCpp, incl_dirs: tuple[Path], excludes: list[str], files_silent: tuple[Path],
                files_in: tuple[Path], file_out: Path, file_exp: Path,
                full_output: bool) -> None:
    pycpp.reset()
    # Set include dirs and process specified file.
    if incl_dirs:
        pycpp.add_include_dirs(*incl_dirs)
    if excludes:
        pycpp.exclude_macros_files = excludes
    pycpp.process_files(*files_silent, global_output=False)
    pycpp.process_files(*files_in, global_output=True)

    # Remove existing output file and save the newest one.
    file_out.unlink(missing_ok=True)
    pycpp.save_output_to_file(file_out, full_output)

    # Assert that the output file is the same as the expected file.
    assert compare_files(file_out, file_exp) is True


@pytest.mark.parametrize("incl_dirs, excludes, files_silent, files_in, file_out, file_exp, full_output", TEST_PARAMS)
def test_script(monkeypatch, incl_dirs: tuple[Path], excludes: list[str], files_silent: tuple[Path],
                files_in: tuple[Path], file_out: Path, file_exp: Path,
                full_output: bool) -> None:
    # Prepare list of command line arguments.
    args = [sys.argv[0]]    # This first argument must be the name of the executed file.
    for file in files_in:
        args.append(f"{file}")
    args.append(f"{file_out}")
    if incl_dirs:
        args.append("-i")
        for dir in incl_dirs:
            args.append(f"{dir}")
    if files_silent:
        args.append("-s")
        for file in files_silent:
            args.append(f"{file}")
    if excludes:
        args.append("-x")
        args.extend(excludes)
    if full_output:
        args.append("-f")

    print(f"Script arguments:\n{' '.join(args[1:])}")

    # Remove existing output file.
    file_out.unlink(missing_ok=True)

    # Set command line arguments to the app environment and run console app.
    monkeypatch.setattr(sys, 'argv', args)
    run_console_app()

    # Assert that the output file is the same as the expected file.
    assert compare_files(file_out, file_exp) is True
