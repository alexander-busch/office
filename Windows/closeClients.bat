@echo off

rem Close OneDrive
taskkill /IM OneDrive.exe /T /F

rem close Synology Drive
taskkill /IM cloud-drive-ui.exe /T /F

rem close Skype for Business
taskkill /IM lync.exe /T /F

rem close Teams
taskkill /IM Teams.exe /T /F

rem Dropbox
taskkill /IM Dropbox.exe /T /F

rem Close iCloud
taskkill /IM iCloudDrive.exe /T /F
taskkill /IM iCloudPhotos.exe /T /F
taskkill /IM AppleIEDAV.exe /T /F
taskkill /IM ApplePhotoStreams.exe /T /F
taskkill /IM iCloudServices.exe /T /F