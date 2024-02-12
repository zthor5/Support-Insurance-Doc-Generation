REM This batch file runs a python script that creates templates.
DEL Output-Goes-Here\*.pdf
DEL Output-Goes-Here\*.txt
SET PATH=%PATH%;C:\Python27;C:\Python27\Scripts
IF EXIST "Insert-csvFile\input.csv" (
    python runner.py
) else ( 
    REM ===========================================================================================
    REM == READ HERE --> Please Insert a csv file (input.csv) into the "Insert-csvFile" Folder! ==
    REM ==========================================================================================
    PAUSE
)