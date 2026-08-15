# Store the current working directory and change it to the tool's root dir.
Push-Location -Path (Join-Path -Path $PSScriptRoot -ChildPath '..')

# Remove old build files.
foreach($BuildPath in ('dist'), ("build\*.egg-info"))
{
    if(Test-Path -Path $BuildPath)
    {
        Remove-Item -Path $BuildPath -Force -Recurse
    }
}

# Build new package distribution files.
python -m build

# Switch back to the original working directory.
Pop-Location
