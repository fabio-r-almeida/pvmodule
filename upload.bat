set /p COUNTER=<1_current_version.txt


@echo off
    setlocal enableextensions disabledelayedexpansion

    set "search=%COUNTER%"
    set /A COUNTER=COUNTER+1
    set "replace=%COUNTER%"

    set "textFile=1_SETUP_TEMPLATE.txt"

    for /f "delims=" %%i in ('type "%textFile%" ^& break ^> "%textFile%" ') do (
        set "line=%%i"
        setlocal enabledelayedexpansion
        >>"%textFile%" echo(!line:%search%=%replace%!
        endlocal
    )
for /f "tokens=1-4 delims=/ " %%i in ("%date%") do (
     set month=%%j
     set year=%%k
     )
set datestr=__version__ = '%year%.%month%.

@echo off

    set "textFile=1_VERSION.txt"

    for /f "delims=" %%i in ('type "%textFile%" ^& break ^> "%textFile%" ') do (
        set "line=%%i"
        setlocal enabledelayedexpansion
        >>"%textFile%" echo(%datestr%%replace%'!
        endlocal
    )

<NUL set /p=%COUNTER%> 1_current_version.txt
copy 1_VERSION.txt pvmodule_version.py
copy 1_SETUP_TEMPLATE.txt setup.py

@RD /S /Q "./build"
@RD /S /Q "./dist"
@RD /S /Q "./pvmodule.egg-info"
python setup.py sdist bdist_wheel
twine upload dist/* -u Fabio_R_Almeida
git add -A
git commit -m "Automatic Push"
git pull origin main
git push -u origin main 

