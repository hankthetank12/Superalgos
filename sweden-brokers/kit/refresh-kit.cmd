@echo off
REM Sweden Retail Brokers - push the latest dashboard build to its Kit app.
REM
REM Kit serves a FROZEN copy and never pulls, so every rebuild has to be pushed to it.
REM The rebuild itself happens in the cloud session (see ..\RUNBOOK.md): it lands on the GitHub
REM branch and is uploaded to the SharePoint Dashboards hub as "Sweden Retail Brokers.html".
REM This script pulls the branch, refreshes the synced hub copy and republishes to Kit.
REM Run it by hand after a refresh, or register it with Task Scheduler (weekdays, after the
REM 13:07 UTC / 09:07 ET cloud run) via
REM   wscript.exe //B C:\Users\hstauber\tools\run-hidden.vbs "<this file>"
REM
REM Edit the paths and KIT_APP below once.
setlocal
set REPO=C:\Users\hstauber\Superalgos
set BRANCH=claude/sweden-brokers-market-share-1kmz2n
REM HUB = the OneDrive-synced copy of JBCM\Shared Documents\NewCo\HS\Dashboards
REM       (the folder that holds index.html, kit-publish.ps1 and kit-apps.json).
set HUB=%OneDrive%\Documents\Dashboards
set LOG=%~dp0refresh-kit.log
set KIT_APP=REPLACE_WITH_THE_KIT_APP_SLUG_AFTER_THE_FIRST_PUBLISH

echo [%date% %time%] start >> "%LOG%"

REM 1. Pull the latest build. A clone must already exist at %REPO% on %BRANCH%.
git -C "%REPO%" fetch origin %BRANCH% >> "%LOG%" 2>&1 || goto :fail
git -C "%REPO%" checkout -q %BRANCH% >> "%LOG%" 2>&1 || goto :fail
git -C "%REPO%" pull --ff-only origin %BRANCH% >> "%LOG%" 2>&1 || goto :fail
if not exist "%REPO%\sweden-brokers\hub\Sweden Retail Brokers.html" goto :fail

REM 2. Refresh the hub copy (the cloud run already uploads it to SharePoint; this covers the
REM    case where the synced folder lags).
if exist "%HUB%" copy /Y "%REPO%\sweden-brokers\hub\Sweden Retail Brokers.html" "%HUB%\Sweden Retail Brokers.html" >> "%LOG%" 2>&1

REM 3. Republish to Kit. Preferred: the hub's own publisher, which PUTs the page to
REM    https://nnj2-seal7742.walleyetrading.net/kit/v1/apps/%KIT_APP% and updates kit-apps.json.
REM    Check its parameter block once and put the right call here, e.g.
REM      powershell -NoProfile -ExecutionPolicy Bypass -File "%HUB%\kit-publish.ps1" "Sweden Retail Brokers.html" >> "%LOG%" 2>&1 || goto :fail
REM    Fallback (used until then): the kit skill in Claude Code, run headless.
claude -p "use kit to publish %REPO%\sweden-brokers\hub\Sweden Retail Brokers.html as a new version of the existing Kit app %KIT_APP% (Sweden Retail Brokers). Serve the file as-is. Print the app link when done." >> "%LOG%" 2>&1 || goto :fail

echo [%date% %time%] ok >> "%LOG%"
endlocal
exit /b 0

:fail
echo [%date% %time%] FAILED - see above >> "%LOG%"
endlocal
exit /b 1
