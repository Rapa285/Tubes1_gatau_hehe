@echo off
start cmd /k "python main.py --logic CBG --email=test@email.com --name=stima --password=123456 --team etimo"
start cmd /k "python main.py --logic lwd --email=test1@email.com --name=stima1 --password=123456 --team etimo"
start cmd /k "python main.py --logic CBG --email=test2@email.com --name=stima2 --password=123456 --team etimo"
start cmd /k "python main.py --logic lwd --email=test3@email.com --name=stima3 --password=123456 --team etimo"

@REM wait till 65 seconds
timeout /t 65

@REM then start again the run-bots.bat
start run-bots.bat

@REM then close the current cmd
exit
```