# Introduction

**Pycpp** (**Py**thon **C** **p**re**p**rocessor) is a C code preprocessor written in Python. The preprocessor is not
intended to create source files for the compiler. It is aimed at the creation of C source files with correctly
expanded macros for the purposes of static analysis or code coverage analysis.

The pycpp produces a code with formatting very close to the original code, i.e., the line endings, intendantion and
comments are preserved, even in the expanded macro bodies. It is also possible to keep the original preprocessor
directives.

# Usage

## Pycpp as a Python module

The code below shows the basic usage of pycpp as a Python module. See the *samples\module_usage* directory for the
executable example listed below together with another slightly more advanced sample script.

``` python
# Import preprocessor class PyCpp
from pycpp import PyCpp


SAMPLE_CODE = """
#define CUBE(X)     (X) * (X) * (X)
#define A           5
#define B           3

a = CUBE(A);
"""

# Create the preprocessor object.
pycpp = PyCpp()

# Process C code defined in a SAMPLE_CODE string.
pycpp.process_code(SAMPLE_CODE)

# Print full global output. The full output means that everything from the original code
# (including preprocessor directives) is included in the output.
print(pycpp.output_full)
# Prints:
# #define CUBE(X)     (X) * (X) * (X)
# #define A           5
# #define B           3
#
# a = (5) * (5) * (5);

# Print standard preprocessed output without the processed directives and comments not related to the remaining code.
print(pycpp.output)
# Prints:
# a = (5) * (5) * (5);

print(pycpp.expand_macros("b = CUBE(B + 1);"))
# Prints:
# b = (3 + 1) * (3 + 1) * (3 + 1);

print(pycpp.evaluate("CUBE(2 + 2)"))
# Prints:
# 64

print(pycpp.is_true("CUBE(A - B) < CUBE(A + B)"))
# Prints:
# True

# Reset internal preprocessor output.
pycpp.reset_output()

# Add include directory to search for included files.
pycpp.add_include_dirs("path/to/incl/dir")

# Process C code defined in file.
pycpp.process_files("path/to/src.c")

# Save preprocessor output to the output file.
pycpp.save_output_to_file("path/to/src_processed.c")
```

## Pycpp as a standalone script

C source files can be processed by calling the pycpp from the commmand line with the arguments in a following format:

```text
python pycpp.py in_src1.c [in_src2.c ...] out_src.c [-s silent_in_src1 [silent_in_src2 ...]] [-i incl_dir1 [incl_dir2 ...]] [-f] [-v 0-2] [-V] [-h]
```

Positional arguments:

- `in_src1.c [in_src2.c ...]` - Input source files to be processed.
- `out_src.c` - Output source file with processed code from all specified input files.

Optional arguments:

- `-s silent_in_src1 [silent_in_src2 ...]` - Input source files processed silently , i.e., without generated
  output, before processing the main input files.
- `-i incl_dir1 [incl_dir2 ...]` - Included directories to search for the input files or for the included files
  defined by the `#include` statements in the input sources.
- `-f` - Option to enable full output, i.e., to include directives, all comments and whitespaces in the
  preprocessor output
- `-v 0-2` - Set console log verbosity level (0 = logging OFF with errors still shown).
- `-V` - Show program name and version.
- `-h` - Show help message and exit.

Example of a call to process a single file with full output and verbosity at the maximum level 2:

```powershell
python "src/pycpp.py" "samples/script_usage/c_files/src.c" "samples/script_usage/c_files/processed_src.c" -i "samples/script_usage/c_files/incl" -f -v2
```

See the example in the *samples\script_usage* directory for more details.
