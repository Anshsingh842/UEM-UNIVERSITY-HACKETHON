@echo off
title Jan Sahayak - Start
cd /d "%~dp0"
echo.
echo  Jan Sahayak shuru ho raha hai...
echo.

rem --- Agar pehle se chal raha hai to bas browser kholo ---
netstat -ano | findstr ":5000 " | findstr LISTENING >nul
if %errorlevel%==0 goto open

rem --- Python dhundo ---
set "PY="
where py >nul 2>nul
if %errorlevel%==0 set "PY=py -3"
if not defined PY (
  where python >nul 2>nul
  if %errorlevel%==0 set "PY=python"
)
if not defined PY goto nopython
%PY% --version >nul 2>nul
if errorlevel 1 goto nopython

rem --- Pehli baar: venv banao aur Flask install karo ---
if not exist ".venv\Scripts\python.exe" (
  echo  Pehli baar setup ho raha hai, 1-2 minute lagenge...
  %PY% -m venv .venv
  if errorlevel 1 goto fail
)
if not exist ".venv\installed.flag" (
  ".venv\Scripts\python.exe" -m pip install -q -r requirements.txt
  if errorlevel 1 goto nointernet
  echo ok> ".venv\installed.flag"
)

rem --- Server chalao (chhoti minimized window mein) ---
start "Jan Sahayak Server" /min ".venv\Scripts\python.exe" app.py

rem --- Server ready hone ka intezaar (max 20 second) ---
for /l %%i in (1,1,20) do (
  netstat -ano | findstr ":5000 " | findstr LISTENING >nul
  if not errorlevel 1 goto open
  timeout /t 1 >nul
)
goto fail

:open
start "" http://127.0.0.1:5000
echo  Browser khul gaya hai. Band karne ke liye STOP.bat par double click karo.
timeout /t 4 >nul
exit /b 0

:nopython
echo  Python nahi mila.
echo  python.org se Python install karo. Install karte waqt "Add Python to PATH" tick karna.
echo  Phir START.bat dobara chalao.
pause
exit /b 1

:nointernet
echo  Flask install nahi ho paya. Internet chalu karke dobara try karo.
pause
exit /b 1

:fail
echo  Kuch gadbad hui. Server shuru nahi hua.
echo  Ek baar STOP.bat chalao aur phir START.bat dobara chalao.
pause
exit /b 1
