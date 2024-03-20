from pathlib import Path
import sys


CURR_DIR_PATH = Path(__file__).parent

sys.path.append(str(Path(CURR_DIR_PATH, "../../src").resolve()))


from pycpp import PyCpp     # noqa: E402


SAMPLE_CODE_1 = """
#define SUM(A, B)   A + B

SUM(11, 22)
"""

SAMPLE_CODE_2 = """
#define IGNORE_MACRO(X)     #X
#define SQR(A)      A * A
#define A 5

#ifdef A
    #define A_SQR   SQR(A)
#endif

A_SQR /* Outputs 5 * 5 */

IGNORE_MACRO(abc)
"""

# Create the preprocessor object.
pycpp = PyCpp()

# Process C code defined in a SAMPLE_CODE_1 string and save the processed output into the variable.
# The processed code is also stored in the internal global preprocessor output.
local_output = pycpp.process_code(SAMPLE_CODE_1)

print(local_output)
# Prints:
# 11 + 22

# Add macro identifier IGNORE_MACRO to the excluded macros. The macro will not be processed.
pycpp.exclude_macros_files.append("IGNORE_MACRO")

# Process C code defined in a SAMPLE_CODE_2 string and save the full processed output into the variable.
# The full output means that everything from the original code (including preprocessor directives) is included in the output.
# The processed code is not added the internal global preprocessor output.
local_output = pycpp.process_code(SAMPLE_CODE_2, full_local_output=True, global_output=False)

print(local_output)     # Notice the non-expanded macro IGNORE_MACRO that was excluded from processing.
# Prints:
# #define IGNORE_MACRO(X)     #X
# #define SQR(A)      A * A
# #define A 5
#
# #ifdef A
#     #define A_SQR   SQR(A)
# #endif
#
# 5 * 5 /* Outputs 5 * 5 */
#
# IGNORE_MACRO(abc)

# Print global output (note that SAMPLE_CODE_2 output was not added to the global output).
print(pycpp.output)
# Prints:
# 11 + 22

# Print full global output (note that SAMPLE_CODE_2 output was not added to the global output).
print(pycpp.output_full)
# Prints:
# #define SUM(A, B)   A + B
#
# 11 + 22

print(pycpp.expand_macros("A + A == SUM(3, 7)"))
# Prints:
# 5 + 5 == 3 + 7

print(pycpp.evaluate("A_SQR"))
# Prints:
# 25

print(pycpp.is_true("SUM(1, 2) >= 3"))
# Prints:
# True

# Reset global preprocessor output.
pycpp.reset_output()

# Add include directory to search for included files.
pycpp.add_include_dirs(Path(CURR_DIR_PATH, "c_files", "incl"))
# Process C code defined in files. Local output corresponding to the processed file code is returned but ignored.
pycpp.process_files(Path(CURR_DIR_PATH, "c_files", "src1.c"))
pycpp.process_files(Path(CURR_DIR_PATH, "c_files", "src2.c"))

# Save output from both processed input files into the output file.
pycpp.save_output_to_file(Path(CURR_DIR_PATH, "c_files", "processed_src12.c"))
