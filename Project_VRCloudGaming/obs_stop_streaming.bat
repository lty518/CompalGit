::taskkill /f /im obs64.exe

tasklist /FI "IMAGENAME eq obs64.exe" /FO CSV > search1.log 

FOR /F %%A IN (search1.log) DO IF %%~zA EQU 1 GOTO end 

taskkill /F /FI "IMAGENAME eq obs64.exe"

:end 

del search.log 