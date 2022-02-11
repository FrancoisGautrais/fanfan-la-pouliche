import os, sys
from pathlib import Path
from install import common


if __name__ != "__main__":
    dir = os.getcwd()
    os.chdir(Path(__file__).parent)
    os.system(f"{sys.executable} {sys.argv[0]}")
    os.chdir(dir)
else: #reload libraries
    os.system(f"bash update_jsx one_shot")
    os.chdir("src/fflp")
    os.system("python manage.py migrate")
    os.system("python manage.py runserver")