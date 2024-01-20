from pathlib import Path
import os
from shutil import rmtree

if __name__ == "__main__":
    root_path = Path(__file__).parent
    os.chdir(root_path)
    os.system(
        "pyinstaller --clean --onefile --windowed --name vroom-legend "
        "--icon src/ressources/Ico/ico.ico "
        "--add-data src/ressources/Maps/dependencies;ressources/Maps/dependencies "
        "--add-data src/ressources/Sprites/dependencies;ressources/Sprites/dependencies "
        "--add-data src/ressources/BackgroundMenu;ressources/BackgroundMenu "
        "--add-data src/ressources/Buttons;ressources/Buttons "
        "--add-data src/ressources/Font;ressources/Font "
        "--add-data src/ressources/Sounds;ressources/Sounds "
        "--add-data src/ressources/Ico;ressources/Ico "
        "src/main.py"
    )
    rmtree("build", ignore_errors=True)
    exe_folder = root_path / Path("dist/vroom-legend.exe")
    print(f"Game built in {exe_folder}")
