# Call all platforms from this main file
import os
import sys
from PyQt5 import QtWidgets, uic 
from revel import run_revel
from doordash import run_doordash
from uber import run_uber
from grubhub import run_grubhub
from threading import Thread
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for development and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


app = QtWidgets.QApplication([])
dlg = uic.loadUi(resource_path(os.path.join("assets", "Program.ui")))


class Settings:
    isHeadlessEnabled = False
    # other settings to add...

settings = Settings()

dlg.statusbar.showMessage("Ready...", 10000)
dlg.OutputConsole.addItem("Welcome to the Live Sales App")
dlg.OutputConsole.addItem("Press any button below to begin")

def output_to_app(platformName, sales):
    platformName = platformName.lower()

    if platformName == "revel":
        dlg.OutputConsole.addItem("REVEL")
    elif platformName == "doordash":
        dlg.OutputConsole.addItem("DOORDASH")
    elif platformName == "uber":
        dlg.OutputConsole.addItem("UBER EATS")
    elif platformName == 'grubhub':
        dlg.OutputConsole.addItem("GRUBHUB")
    else:
        print("ERROR: Need to pass platform name")
        exit()

    dlg.OutputConsole.addItem("----------------")

    for location, amount in sales.items():
        outputString = str(location) + ": $" + str(amount)
        dlg.OutputConsole.addItem(outputString)

def exec_all():
    exec_revel()
    # revelSales = run_revel()
    # output_to_app("revel", revelSales)

    exec_doordash()
    # doordashSales = run_doordash()
    # output_to_app("doordash", doordashSales)
    
    exec_uber()
    # uberSales = run_uber()
    # output_to_app("uber", uberSales)

    exec_grubhub()
    # grubhubSales = run_grubhub()
    # output_to_app("grubhub", grubhubSales)

    # dlg.OutputConsole.clear()

    # dlg.OutputConsole.addItem("Opening spreadsheet...")
    # TODO: open browser to spreadsheet...
    
# exec_<platformName>() wrapper functions allow us to catch return value (threads dont handle return)
def exec_revel():
    # dlg.OutputConsole.addItem("Scraping Revel...")
    revelSales = run_revel()
    dlg.OutputConsole.clear()
    if revelSales == 1:
        dlg.OutputConsole.addItem("Revel: Login failed")
    else:
        output_to_app("revel", revelSales)

def exec_doordash():
    doordashSales = run_doordash()
    dlg.OutputConsole.clear()
    if doordashSales == 1:
        dlg.OutputConsole.addItem("Doordash: Login failed")
    elif doordashSales == 2:
        dlg.OutputConsole.addItem("Doordash: Blocked by 2SV")
    elif doordashSales == 3:
        dlg.OutputConsole.addItem("Doordash: Couldn't find an element on page or network error")
    else:
        output_to_app("doordash", doordashSales)

def exec_uber():
    uberSales = run_uber()
    dlg.OutputConsole.clear()
    if uberSales == 1:
        dlg.OutputConsole.addItem("Uber: Login failed")
    else:
        output_to_app("uber", uberSales)

def exec_grubhub():
    grubhubSales = run_grubhub()
    dlg.OutputConsole.clear()
    if grubhubSales == 1:
        dlg.OutputConsole.addItem("Grubhub: Login failed")
    elif grubhubSales == 2:
        dlg.OutputConsole.addItem("Grubhub: Blocked by login security check")
        dlg.OutputConsole.addItem("Tip - Mimic human input to get around check:")
        dlg.OutputConsole.addItem("Click on input fields, check remember me, and")
        dlg.OutputConsole.addItem("manually click sign in button to avoid. Press and hold button.")
        dlg.OutputConsole.addItem("(May need to do the above twice)")
    else:
        output_to_app("grubhub", grubhubSales)

def webscrap_all_thread():
    dlg.OutputConsole.clear()
    dlg.OutputConsole.addItem("Scraping now...")
    webscrapThread = Thread(target=exec_all)
    webscrapThread.start()
    # webscrapThread.join()

def webscrap_revel_thread():
    dlg.OutputConsole.clear()
    dlg.OutputConsole.addItem("Scraping Revel...")
    # webscrapThread = Thread(target=run_revel)
    webscrapThread = Thread(target=exec_revel)
    webscrapThread.start()
    # webscrapThread.join()

def webscrap_doordash_thread():
    dlg.OutputConsole.clear()
    dlg.OutputConsole.addItem("Scraping DoorDash...")
    webscrapThread = Thread(target=exec_doordash)
    webscrapThread.start()

def webscrap_uber_thread():
    dlg.OutputConsole.clear()
    dlg.OutputConsole.addItem("Scraping Uber Eats...")
    webscrapThread = Thread(target=exec_uber)
    webscrapThread.start()

def webscrap_grubhub_thread():
    dlg.OutputConsole.clear()
    dlg.OutputConsole.addItem("Scraping Grubhub...")
    webscrapThread = Thread(target=exec_grubhub)
    webscrapThread.start()

def open_github():
    dlg.statusbar.showMessage("Opening github repo to project...", 5000)
    options = ChromeOptions()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get("https://github.com/reedx8/Sales-Web-Scrap")
    # driver.quit()

def updateHeadlessBtn():
    settings.isHeadlessEnabled = dlg.HeadlessRadioBtn.isChecked()

dlg.RunAllButton.clicked.connect(webscrap_all_thread)
dlg.RevelButton.clicked.connect(webscrap_revel_thread)
dlg.DoordashButton.clicked.connect(webscrap_doordash_thread)
dlg.UberButton.clicked.connect(webscrap_uber_thread)
dlg.GrubhubButton.clicked.connect(webscrap_grubhub_thread)
dlg.GithubButton.clicked.connect(open_github)
dlg.HeadlessRadioBtn.clicked.connect(updateHeadlessBtn)





dlg.show()
app.exec()