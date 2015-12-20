@echo off&color a
chcp 1250
cls
pushd "%~dp0"
title TELEWIZJADA UPDATER
fltmc >nul 2>&1 || (
	echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
	echo UAC.ShellExecute "%~fs0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
	"%temp%\getadmin.vbs"
	del /f /q "%temp%\getadmin.vbs"
	exit /b
)
REG QUERY "HKU\S-1-5-19" >NUL 2>&1 && (
pushd "%~dp0"
cls
GOTO RUN
) || (
echo.&echo.&echo.
echo Uruchom ten skrypt jako administrator...
echo.&echo.&echo.
pause
exit
)

:RUN
set agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2595.0 Safari/537.36"
set cookies_dir=cookies
set strm_dir=strm
set m3u_dir=m3u
set logo_tv=https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/logo_tv
set logo_radio=https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/logo_radio
set images=https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/images
set cookie=%cookies_dir%\%%C.txt
set pls="%%B/playlist.m3u8"
set link=
pushd "%~dp0"
if exist %m3u_dir%\telewizjada.m3u del /F /Q %m3u_dir%\telewizjada.m3u
echo #EXTM3U > %m3u_dir%\telewizjada.m3u
cls

:DOWNLOAD
:: %%A -> Nazwa    %%B -> adres kanalu    %%C -> nazwa pliku dla cookie oraz logo
FOR /F "tokens=1,2,3 delims=," %%A IN (linki.txt) DO (
set pls="%%B/playlist.m3u8"
if exist %pls% del /F /Q %pls%
echo.
echo %%A && set /p=""<nul
wget_lite.exe -q --tries=2 --timeout=3 --show-progress --user-agent=%agent% --load-cookies=%cookie% %pls%
::PING -n 1 127.0.0.1>nul
if exist "%strm_dir%\%%C.strm" del /F /Q "%strm_dir%\%%C.strm"
set /p="%%B/"<nul >"%strm_dir%\%%C.strm"
FIND /i "chunklist" < playlist.m3u8 >>"%strm_dir%\%%C.strm"

del /F /Q *m3u8*
)
echo.
echo CZEKAM 15s PRZED KOLEJN¥ AKTUALIZACJ¥ LINKÓW...
echo.
echo JE¯ELI TO CZYTASZ, TO ZNACZY, ¯E KODI JEST URUCHOMIONY
echo (program zostanie zakoñczony po wy³¹czeniu KODI.EXE)
echo.
tasklist /fi "imagename eq kodi.exe" | find /i "kodi.exe" > nul
if not errorlevel 1 (echo kodi run & PING -n 1 127.0.0.1>nul) else (
  exit
)
TIMEOUT /T 14 /NOBREAK
::PING -n 15 127.0.0.1>nul
:CLEAR_TEMP
pushd "%~dp0"
start /low /min update.exe
exit