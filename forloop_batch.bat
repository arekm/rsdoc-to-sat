Rem for /r %%i in (*) do echo %%i

REM @echo off
REM for %%f in (*.rsdoc) do (
    REM if "%%~xf"==".rsdoc" echo %%f
REM )




@echo off
for %%f in (*.rsdoc) do (
	if "%%~xf"==".rsdoc" python rsdoc_to_sat.py %%f
)
