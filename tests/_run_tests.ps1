# Store the current working directory and move to the directory containing this script.
Push-Location -Path $PSScriptRoot

# Execute tests. -s: disable all stdout/stderr capturing, -v: verbose
& python -m pytest test.py -s -v

# Switch back to the original working directory.
Pop-Location
