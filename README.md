# Sales Web Scrap (Ava)
Scraps live sales data from 4 different web platforms and sends data to a spreadsheet.

Spreadsheet: https://docs.google.com/spreadsheets/d/1deyIpmet1Fa9bRqAI9IbRpMC60Z1NmM3Jt6cOFOwZe0/edit#gid=0

## To run:
1. Clone the repo
2. Install the following (see "Installation Docs" section for more):
    - Chrome browser
    - python 3.9: https://www.python.org/downloads/
    - pip: Comes packaged with python when downloaded from python.org
    - Selenium: `pip3 install selenium`
    - Load-dotenv: `pip3 install python-dotenv`
    - pygsheets: `pip3 install https://github.com/nithinmurali/pygsheets/archive/staging.zip`
    - pandas: `pip3 install pandas`
3. Message repo owner for the following files and add to project's root folder:
    - `.env` file
    -  `google_api_cred.json` file
4. Edit `sheet.py` with your own path to `google_api_cred.json`
5. Run each of the following in terminal:
    - `python3 revel.py <path_option>`
    - `python3 doordash.py <path_option>`
    - Path option = The path option defined in `sheet.py`
    - Note: Refrain from closing terminal or resizing browser window while programs are running.

## Installation Docs
- Selenium:  https://selenium-python.readthedocs.io/installation.html
- Load-dotenv: https://github.com/theskumar/python-dotenv 
- pygsheets: https://github.com/nithinmurali/pygsheets
- pandas: https://pandas.pydata.org/docs/getting_started/install.html


