import os, sys
from pathlib import Path
from install import common


os.system(f"bash update_jsx one_shot")
os.chdir("src/fflp")
os.system("python manage.py migrate")
os.system("python manage.py runserver")