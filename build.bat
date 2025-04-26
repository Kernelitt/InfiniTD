@echo off
REM Компилируем файлы levelmaker.py и menu.py с помощью PyInstaller
pyinstaller --onefile --noconsole levelmaker.py
pyinstaller --onefile --noconsole menu.py

REM Копируем папки music и levels в папку dist
xcopy /E /I music dist\music
xcopy /E /I levels dist\levels

REM Копируем файл config.ini в папку dist
copy config.ini dist\config.ini

REM Переименовываем menu.exe в InfiniTD.exe
rename dist\menu.exe InfiniTD.exe

REM Удаляем .spec файлы
del *.spec

REM Переименовываем папку dist в InfiniTD
ren dist InfiniTD

REM Упаковываем папку InfiniTD в ZIP-архив
powershell -command "Compress-Archive -Path InfiniTD -DestinationPath InfiniTD.zip"

echo Compilation Completed!
pause