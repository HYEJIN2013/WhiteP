from django.db import connection
from django.core.management import call_command

cursor = connection.cursor()
cursor.execute("DROP SCHEMA public CASCADE;")
cursor.execute("CREATE SCHEMA public;")
call_command('migrate')
