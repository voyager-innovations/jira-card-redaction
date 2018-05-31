searchpan
    - Outputs a list of suspected images with PAN to a text file (results.txt)

Installation:
    Prerequisite:
        - Python 3.5.x is installed

    1. Create a 'searchpan' folder to contain all files
    2. Create a python virtual environment using this command:
        python3 -m venv env
    3. Activate the virtual environment using this command:
        . env/bin/activate
    4. Install required libraries using this command:
        pip3 install -r requirements.txt

Usage:
    searchpan.py [-h] [-l] [-d]

    optional arguments:
      -h, --help     show this help message and exit
      -l, --less     print less details on the screen
      -d, --dir      root directory to start traversing. Defaults to current working directory.

