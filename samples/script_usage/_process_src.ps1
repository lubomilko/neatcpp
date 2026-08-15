# Store the current working directory and move to the directory containing this script.
Push-Location -Path $PSScriptRoot

# Process src.c file into the processed_src.c with full output and verbosity set to the highest level 2.
& python "../../src/neatcpp" "c_files/src.c" "c_files/processed_src.c" -i "c_files/incl" -x "stdint.h" -f -v2

# Switch back to the original working directory.
Pop-Location
