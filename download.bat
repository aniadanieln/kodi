@echo off&color a&mode con: cols=132 lines=20
chcp 1250
cls
pushd "%~dp0"
title Aktualizacja STREAM?W
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
set logo_tv=https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/logo_tv
set logo_radio=https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/logo_radio
set images=https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/images
set cookie=%cookies_dir%\%%C.txt
set pls="%%B/playlist.m3u8"
set link=
pushd "%~dp0"
cls
:CLEAR_ALL
pushd "%~dp0"
::del /F /Q %strm_dir%\*
del /F /Q *m3u8*
del /F /Q log.txt
cls

:DOWNLOAD
::echo %time:~0,-3%
:: %%A -> Nazwa    %%B -> adres kanalu    %%C -> nazwa pliku dla cookie oraz logo
FOR /F "tokens=1,2,3 delims=," %%A IN (linki.txt) DO (
set pls="%%B/playlist.m3u8"
echo %%A
if exist %strm_dir%\%%C.strm del /F /Q %strm_dir%\%%C.strm
wget_lite.exe -nv --append-output=log.txt --show-progress --waitretry=2 --user-agent=%agent% --load-cookies=%cookie% %pls%
echo #EXTINF:0 thumb=%logo_tv%\%%C.png,%%A >%strm_dir%\%%C.strm
set /p="%%B/"<nul >>%strm_dir%\%%C.strm
FIND /i "chunklist" < playlist.m3u8 >>%strm_dir%\%%C.strm
del /F /Q *m3u8*
echo.
)

:CLEAR_TEMP
pushd "%~dp0"
TIMEOUT /T 5 /NOBREAK
"C:\Program Files\Git\git-bash.exe" "sh script.sh"
TIMEOUT /T 20 /NOBREAK
cls
goto run

exit