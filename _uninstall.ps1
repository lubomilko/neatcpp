# Store the current working directory and change it to the root dir of this script.
Push-Location -Path $PSScriptRoot

# Get the package name from the first directory within the '.\src' subdirectory.
$pkgName = Get-ChildItem -Path 'src' -Directory | Select-Object -First 1 -ExpandProperty Name
# Uninstall the package.
python -m pip uninstall --disable-pip-version-check --yes $pkgName

# Switch back to the original working directory.
Pop-Location
