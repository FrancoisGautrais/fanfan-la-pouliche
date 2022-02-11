import os, sys
from pathlib import Path
import os
from pathlib import Path


dir = os.getcwd()
os.chdir(Path(__file__).parent)

NPM_PATH=None
for path in os.environ.get("PATH", "").split(":"):
    path = Path(path)
    if (path / "npm").exists():
        NPM_PATH=path / "npm"
        break

if not NPM_PATH:
    print("npm n'est pas installé et requis")
    exit(-1)

print("installation des dépendances NPM")
os.system("npm install")
os.chdir(dir)

os.system(f"bash update_jsx one_shot")
os.chdir("src/fflp")
os.system("python manage.py migrate")
os.system("python manage.py runserver")