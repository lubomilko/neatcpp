@ECHO OFF
REM Store the current working dir and switch to the directory where this bat file is located,
REM because all paths below are relative to this dir. %~dp0 contains the dir path of this bat file.
@pushd %~dp0

REM Execute tests.
python -m pytest test.py -s -v

REM Switch back to the original current working directory.
@popd
