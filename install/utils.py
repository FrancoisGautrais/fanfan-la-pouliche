from pathlib import Path


def package_data(dir, relative_to=None):
    array =  []
    relative_to=Path(relative_to or Path(__file__).parent)
    stack = [Path(dir)]
    while stack:
        for path in stack.pop(0).iterdir():
            if path.is_file():
                array.append(str(path.resolve().relative_to(relative_to)))
            else:
                stack.append(path)
    return array