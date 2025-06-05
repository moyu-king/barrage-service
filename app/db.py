from peewee import SqliteDatabase
from app.constant import db_path
from app.constant import project_root
import subprocess
import os
import sys

db = SqliteDatabase(db_path)


__all__ = ['db']

if __name__ == "__main__":
    dir_name = 'models'
    dir_path = os.path.join(project_root, 'app', 'models')

    for file in os.listdir(dir_path):
        full_path = os.path.join(dir_path, file)
        module = file.replace('.py', '')

        if os.path.isfile(full_path) and file.endswith('.py'):
            subprocess.run([sys.executable, '-m', f'app.{dir_name}.{module}'])
