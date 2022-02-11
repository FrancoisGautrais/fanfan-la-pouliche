import os
from pathlib import Path
from install import common


dir = os.getcwd()
os.chdir(Path(__file__).parent)

for path in os.environ.get("PATH", "").split(":"):
    path = Path(path)
    if (path / "npm").exists():
        common.NPM_PATH=path / "npm"
        break

if not common.NPM_PATH:
    print("npm n'est pas installé et requis")
    exit(-1)

print("installation des dépendances NPM")
os.system("npm install")
os.chdir(dir)