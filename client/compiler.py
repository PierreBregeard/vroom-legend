from pathlib import Path
import os
from shutil import rmtree

if __name__ == "__main__":
    root_path = Path(__file__).parent
    os.chdir(root_path)
    os.system("pyinstaller --clean --onefile --windowed --name vroom-legend --add-data "
              "src\\ressources;src\\ressources src\\main.py")
    rmtree("build")
    exe_folder = root_path / Path("dist\\vroom-legend.exe")
    print(f"Game built in {exe_folder}")
