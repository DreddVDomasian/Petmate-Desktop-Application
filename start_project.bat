@echo off

:: Start Django Backend

start cmd /k "cd venv\Scripts && call activate && cd ..\.. && cd Desktop_Application && cd Backend && python manage.py runserver"


:: Start PyQt Desktop App
start cmd /k "cd venv\Scripts && call activate && cd ..\.. && cd Desktop_Application && cd Frontend && python app.py"

:: Start React Frontend
start cmd /k "cd web-applications && npm run dev"
