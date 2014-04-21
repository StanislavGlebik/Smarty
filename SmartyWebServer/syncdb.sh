rm SmartyDatabase
python manage.py syncdb
DJANGO_SETTINGS_MODULE=SmartyWebServer.settings python filldb.py
