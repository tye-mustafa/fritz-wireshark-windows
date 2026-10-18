@echo off
setlocal
py -3 "%~dp0fritzcap.py" %*
exit /b %errorlevel%
