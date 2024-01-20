from pathlib import Path
import os
from shutil import rmtree

if __name__ == "__main__":
    root_path = Path(__file__).parent
    os.chdir(root_path)
    os.system(
        "pyinstaller --clean --onefile --name server-vroom-legend "
        "serverHTTP/serverHTTP.py"
    )
    rmtree("build", ignore_errors=True)
    exe_folder = root_path / Path("dist/server-vroom-legend.exe")
    print(f"Built in {exe_folder}")
