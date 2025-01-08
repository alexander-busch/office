@echo off

rem Close OneDrive
taskkill /IM OneDrive.exe /T /F

rem Delete files in folders as recommended on 
cd C:\Users\%username%\AppData\Local\Microsoft\OneDrive\setup\logs
del UserTelemetryCache.otc
del UserTelemetryCache.otc.session

rem Reset OneDrive
%localappdata%\Microsoft\OneDrive\onedrive.exe /reset

rem Remove all content in
set destination=C:\Users\%username%\AppData\Local\Microsoft\Office\Spw
echo %destination%
del /q %destination% \*
rem for /d %%x in %destination% %\*) do @rd /s /q ^"%%x^"

rem Remove all content in
set destination=C:\Users\%username%\AppData\Local\Microsoft\Office\16.0\OfficeFileCache
echo %destination%
del /q %destination% \*

rem this is not correct as it tries to delete much more than only the specified folder 

rem del /q /S %destination% \*

rem Restart OneDrive
%localappdata%/Microsoft/OneDrive/onedrive.exe