:: Store the current working dir and switch to the directory where this bat file is located, because all paths below are relative to this dir.
:: %~dp0 contains the dir path of this bat file.
@pushd %~dp0

:: Run preprocessor as a script, read specified files and generate corresponding processed files.
python ../../cpreproc.py ^
comp_interpolation/static_analysis/interpolation_def_in.h comp_interpolation/static_analysis/interpolation_def.h ^
comp_interpolation/static_analysis/interpolation_def_in.c comp_interpolation/static_analysis/interpolation_def.c ^
-i comp_interpolation/dep comp_interpolation/dep/comp_util_type comp_interpolation/dep/src_common comp_interpolation/src ^
-f

:: Switch back to the original current working directory.
@popd
