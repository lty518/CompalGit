tasklist /FI "IMAGENAME eq vrmonitor.exe" /FO CSV > search.log 

FOR /F %%A IN (search.log) DO IF %%~zA EQU 1 GOTO end 

taskkill /F /FI "IMAGENAME eq vrmonitor.exe"


:end 

del search.log 