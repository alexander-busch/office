rem Create folder structure for a new task
rem alexander.busch@alumni.ntnu.no, 27.11.2019
@echo off
set taskpath="C:\Users\Tasks\"
set taskname=2020.185_xxx
set /p taskname=Enter task name
set taskpath="%taskpath:"=%%taskname%"

echo %taskpath%
mkdir %taskpath%
cd %taskpath%

mkdir "00_Archive"
mkdir "01_Customer"
mkdir "01_Customer\CAD"
mkdir "02_Data"
mkdir "02_Data\CAD"
mkdir "03_Sim"
mkdir "03_Sim\scripts"
mkdir "03_Sim\post"
mkdir "04_Doc"
mkdir "04_Doc\figures"
mkdir "04_Doc\movies"


