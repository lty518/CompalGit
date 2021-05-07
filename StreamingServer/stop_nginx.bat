@ECHO OFF
ECHO Stopping Nginx server....
nginx.exe -s stop
taskkill /f /im nginx.exe