# Sales Web Scrap (Ava)

Scraps live sales data from 4 different web platforms and sends data to a spreadsheet.

Spreadsheet: https://docs.google.com/spreadsheets/d/1deyIpmet1Fa9bRqAI9IbRpMC60Z1NmM3Jt6cOFOwZe0/edit#gid=0

## To run

1. Clone the repo
2. Install:
    - Chrome browser
    - Python 3+: https://www.python.org/downloads/
        - If asked/prompted:
            - Add python.exe to PATH
            - Use admin priviliges
    - git: https://git-scm.com/downloads
    - pip: Comes packaged with python when downloaded from python.org
3. Open terminal/command prompt to run the following commands in a virtual environment:

    1. Virtual Environment how-to: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments
        - Note: The `.venv` folder is already included in the `.gitignore` file
    2. Run the following command to install all required packages: `pip3 install -r requirements.txt`
        - _Note_: Use `pip3` or `pip` depending on your setup
        - Requirements outlined (Fallback only. Ignore if install command above worked):
            - PyQt5: `pip3 install PyQt5`
                - Qt Designer (optional): try `pip3 install pyqt5-tools`. If doesnt work, download Qt directly from qt.io (Qt comes with Qt Designer).
            - Selenium: `pip3 install selenium`
            - Load-dotenv: `pip3 install python-dotenv`
            - pygsheets: `pip3 install https://github.com/nithinmurali/pygsheets/archive/staging.zip`
            - pandas: `pip3 install pandas`
            - webdriver-manager: `pip3 install webdriver-manager` (_needed for windows users_)
            - fake-useragent: `pip3 install fake-useragent`
            - See "Installation Docs" section for more info

4. Add the following files to project folder (message repo owner):
    - `.env` file
        - **Windows users only**: Create a new Notepad file, add credentials to file, _file -> save_, save as type: All Files, and name it _'.env'_ (no quotes).
    - `google_api_cred.json` file
5. Edit `sheet.py` with your own path to `google_api_cred.json`
6. Finally, run program with: `python3 scrap.py`
    - Use `python3`, `python`, or `py` depending on your installation setup of python
    - Refrain from closing terminal or resizing browser window while program is running.

_Note_: Do the following to get around Grubhub's login security check:

    1. Clear all history in the browser the script is running
    2. Close the Live Sales app
    3. Sign out of Grubhub anywhere else
    4. Now rerun the app

## Installation Docs

-   Selenium: https://selenium-python.readthedocs.io/installation.html
-   Load-dotenv: https://github.com/theskumar/python-dotenv
-   pygsheets: https://github.com/nithinmurali/pygsheets
-   pandas: https://pandas.pydata.org/docs/getting_started/install.html
-   webdriver-manager: https://pypi.org/project/webdriver-manager/
-   PyQt5: https://doc.qt.io/qtforpython-5/
-   fake-useragent: https://pypi.org/project/fake-useragent/
