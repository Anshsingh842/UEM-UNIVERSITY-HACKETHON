@echo off
title Jan Sahayak - Stop
set "FOUND=0"
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":5000 " ^| findstr LISTENING') do (
  taskkill /PID %%p /F >nul 2>nul
  set "FOUND=1"
)
if "%FOUND%"=="1" (
  echo  Jan Sahayak band ho gaya.
) else (
  echo  Jan Sahayak chal hi nahi raha tha.
)
timeout /t 3 >nul
