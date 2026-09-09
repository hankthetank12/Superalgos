@echo off
REM Sweden Retail Brokers - push the latest dashboard build to its Kit app.
REM
REM Kit serves a FROZEN copy and never pulls, so every rebuild has to be pushed to it.
REM The rebuild itself happens in the cloud session (see ..\RUNBOOK.md) and lands on the
REM GitHub branch; this script pulls that branch and republishes the file to Kit through
REM the kit skill in Claude Code. Run it by hand after a refresh, or register it with
REM Task Scheduler (weekdays, after the 13:07 UTC / 09:07 ET cloud run) via
REM   wscript.exe //B C:\Users\hstauber\tools\run-hidden.vbs "<this file>"
REM
REM Edit the three paths below once.
setlocal
set REPO=C:\Users\hstauber\Superalgos
set BRANCH=claude/sweden-brokers-market-share-1kmz2n
set HUB=%OneDrive%\Documents\Dashboards
set LOG=%~dp0refresh-kit.log
set KIT_APP=REPLACE_WITH_THE_KIT_APP_SLUG_AFTER_THE_FIRST_PUBLISH

echo [%date% %time%] start >> "%LOG%"

REM 1. Pull the latest build. A clone must already exist at %REPO% on %BRANCH%.
git -C "%REPO%" fetch origin %BRANCH% >> "%LOG%" 2>&1 || goto :fail
git -C "%REPO%" checkout -q %BRANCH% >> "%LOG%" 2>&1 || goto :fail
git -C "%REPO%" pull --ff-only origin %BRANCH% >> "%LOG%" 2>&1 || goto :fail
if not exist "%REPO%\sweden-brokers\dashboard.html" goto :fail

REM 2. Copy into the shared Dashboards hub so the hub card and Kit carry the same build.
if exist "%HUB%" copy /Y "%REPO%\sweden-brokers\dashboard.html" "%HUB%\Sweden Retail Brokers.html" >> "%LOG%" 2>&1

REM 3. Republish to Kit. The kit skill (~\.claude\skills\kit\SKILL.md) does the push; this is
REM    the same plain-English instruction you would type interactively, run headless.
claude -p "use kit to publish %REPO%\sweden-brokers\dashboard.html as a new version of the existing Kit app %KIT_APP% (Sweden Retail Brokers). Serve the file as-is. Print the app link when done." >> "%LOG%" 2>&1 || goto :fail

echo [%date% %time%] ok >> "%LOG%"
endlocal
exit /b 0

:fail
echo [%date% %time%] FAILED - see above >> "%LOG%"
endlocal
exit /b 1
