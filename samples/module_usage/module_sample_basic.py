# pylint: disable=missing-module-docstring, missing-function-docstring

from pathlib import Path
import sys


CURR_DIR_PATH = Path(__file__).parent

sys.path.append(str(Path(CURR_DIR_PATH, "../../src").resolve()))

# pylint: disable=wrong-import-position
from neatcpp import NeatCpp     # noqa: E402


SAMPLE_CODE = """
#define CUBE(X)     (X) * (X) * (X)
#define A           5
#define B           3

a = CUBE(A);
"""

# Create the preprocessor object.
neatcpp = NeatCpp()

# Process C code defined in a SAMPLE_CODE string.
neatcpp.process_code(SAMPLE_CODE)

# Print full global output. The full output means that everything from the original code
# (including preprocessor directives) is included in the output.
print(neatcpp.output_full)
# Prints:
# #define CUBE(X)     (X) * (X) * (X)
# #define A           5
# #define B           3
#
# a = (5) * (5) * (5);

# Print standard preprocessed output without the processed directives and comments not related to
# the remaining code.
print(neatcpp.output)
# Prints:
# a = (5) * (5) * (5);

print(neatcpp.expand_macros("b = CUBE(B + 1);"))
# Prints:
# b = (3 + 1) * (3 + 1) * (3 + 1);

print(neatcpp.evaluate("CUBE(2 + 2)"))
# Prints:
# 64

print(neatcpp.is_true("CUBE(A - B) < CUBE(A + B)"))
# Prints:
# True

# Reset internal preprocessor output.
neatcpp.reset_output()

# Add include directory to search for included files.
neatcpp.add_include_dirs(Path(CURR_DIR_PATH, "c_files", "incl"))

# Process C code defined in file.
neatcpp.process_files(Path(CURR_DIR_PATH, "c_files", "src1.c"))

# Save preprocessor output to the output file.
neatcpp.save_output_to_file(Path(CURR_DIR_PATH, "c_files", "processed_src1.c"))
