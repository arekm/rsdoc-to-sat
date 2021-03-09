REM Batch script to convert all .rsdoc files into .sat inside the same directory as python and rsdoc file(s)

@echo off
for %%f in (*.rsdoc) do (
	if "%%~xf"==".rsdoc" python rsdoc_to_sat.py %%f
)
