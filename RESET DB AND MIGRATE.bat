
REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Change to the Django project directory
cd django-autorecruiting-app

REM Clear the database
python manage.py migrate autorecruiting zero
REM Specify the directory path

cd autorecruiting/migrations
del /Q *
REM add __init__.py
break>__init__.py
cd ../..
del db.sqlite3

REM Pause the script to see the output

python.exe manage.py makemigrations
python manage.py makemigrations autorecruiting
python manage.py migrate
python manage.py migrate autorecruiting
pause
REM Deactivate the virtual environment
deactivate
