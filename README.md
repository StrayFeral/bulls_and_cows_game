# BULLS AND COWS GAME
Command-line and PyQt implementation of the classic "Bulls and Cows" game (yes, that same old game we all played in high-school with pen and paper).


## COMMAND-LINE VERSION
Taken directly as is from my python_exercises repository, but I still 
left it there too to keep the commit history.  
This version passed black, mypy and flake8.

### INSTALLATION AND RUNNING
#### LINUX: Debian, Ubuntu, Mint or any other Debian derivative
1. Download the latest DEB package from here
[https://github.com/StrayFeral/bulls_and_cows_game/tree/main/linux_packages/debian/DEBPACKAGES](https://github.com/StrayFeral/bulls_and_cows_game/tree/main/linux_packages/debian/DEBPACKAGES)

2. Install. You could use apt or any package manager of your choice  
`apt install ./bulls-and-cows-game_1.0-1_all.deb`

#### RUN THE GAME

`bulls_and_cows_game`

The .deb package installs a man page as well. Not that anyone needs it, but it's there.

#### INSTALLATION FROM SOURCE
If you already installed the DEB package, you don't need this.

You only need to download file `bulls_and_cows_game.py`.  
The rest of the code is not needed for the command-line version.

#### RUN THE GAME FROM SOURCE
`./bulls_and_cows_game.py`


## QT VERSION (version with a GUI)
Requires PyQt6. This version was created using the Qt Designer 6.4.3.

For this reason, this version passed no black, mypy nor flake8, as 
in general the PyQt convention totally breaks the general Python 
styleguide conventions.

### INSTALLATION
#### LINUX: Debian, Ubuntu, Mint or any other Debian derivative
DEB package is not yet available - will be available after April 2024.

#### INSTALLATION FROM SOURCE
1. Download the code. If you don't have git, just download it as a .zip  
`git clone https://github.com/StrayFeral/bulls_and_cows_game.git`

2. Execute  
`source venv/bin/activate
python -m pip install -r requirements.txt`

Now just run  
`./bulls_and_cows_game_qt.py`
