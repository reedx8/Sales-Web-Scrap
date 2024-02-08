# Sales Web Scrap (Ava)

Scraps live sales data from 4 different web platforms and sends data to a spreadsheet.

Spreadsheet: https://docs.google.com/spreadsheets/d/1deyIpmet1Fa9bRqAI9IbRpMC60Z1NmM3Jt6cOFOwZe0/edit#gid=0

## To run

1. Clone the repo
2. Install:
    - Chrome browser (Latest updated version)
    - Python 3: https://www.python.org/downloads/
        - Add python.exe to PATH
        - Use admin priviliges
    - git: https://git-scm.com/downloads
    - pip: Comes packaged with python when downloaded from python.org
3. Open terminal (mac) or command prompt (windows) to install the following in a virtual environment:
    1. Virtual Environment how-to: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments
        - Note: The `.venv` folder is already included in the `.gitignore` file
    2. Selenium (4.16): `pip3 install selenium`
        - _Note_: Use `pip3` or `pip` depending on your setup
    3. Load-dotenv: `pip3 install python-dotenv`
    4. pygsheets: `pip3 install https://github.com/nithinmurali/pygsheets/archive/staging.zip`
    5. pandas: `pip3 install pandas`
    6. webdriver-manager: `pip3 install webdriver-manager` (_needed for windows users only_)
    7. See "Installation Docs" section for more info
4. Add the following files to project folder (message repo owner):
    - `.env` file
        - **Windows users only**: Create a new Notepad file, add credentials to file, _file -> save_, save as type: All Files, and name it _'.env'_ (no quotes).
    - `google_api_cred.json` file
5. Edit `sheet.py` with your own path to `google_api_cred.json`
6. Run the following in terminal:
    - `python3 scrap.py <PATH_OPTION>`
        - _Note_: Use `python3`, `python`, or `py` depending on your installation setup of python
    - Path option = The path option defined in `sheet.py`
    - _Note_: Refrain from closing terminal or resizing browser window while programs are running.

## Installation Docs

-   Selenium: https://selenium-python.readthedocs.io/installation.html
-   Load-dotenv: https://github.com/theskumar/python-dotenv
-   pygsheets: https://github.com/nithinmurali/pygsheets
-   pandas: https://pandas.pydata.org/docs/getting_started/install.html
-   webdriver-manager: https://pypi.org/project/webdriver-manager/
