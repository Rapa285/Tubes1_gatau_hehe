@echo off
start cmd /k "python main.py --logic CBG --email=mfauzan.az23@email.com --name=ojan --password=123456 --team etimo"
start cmd /k "python main.py --logic lwd --email=mfauzan.az23@email.com --name=ojandua --password=123456 --team etimo"

@REM wait till 65 seconds
timeout /t 65

@REM then start again the run-bots.bat
start run-bots.bat

@REM then close the current cmd
exit
```