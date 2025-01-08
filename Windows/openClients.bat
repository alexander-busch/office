@echo off

rem Start Skype for Business
start lync.exe

rem Start Teams
cd "C:\Users\u376949\AppData\Local\Microsoft\Teams\current"
start Teams.exe

rem Start OneDrive
cd "C:\Users\u376949\AppData\Local\Microsoft\OneDrive"
start OneDrive.exe

rem Start Synology Drive
cd "C:\Program Files (x86)\Synology\SynologyDrive\bin\"
start launcher.exe

rem Dropbox
cd "C:\Program Files (x86)\Dropbox\Client"
start dropbox.exe

rem Start Synology Drive
cd "C:\Program Files (x86)\Common Files\Apple\Internet Services\"
start iCloud.exe
start iCloudDrive.exe
start iCloudPhotos.exe
start AppleIEDAV.exe

cd "C:\Users\u376949"