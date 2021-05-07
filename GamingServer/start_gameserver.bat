@ECHO ON
ECHO Start gameserver and udp receiver...

start cmd /c vJoyClient.exe
start cmd /c
"python.exe" "main.py"
pause
