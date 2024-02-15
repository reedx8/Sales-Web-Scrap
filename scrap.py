# Call all platforms from this main file
from PyQt5 import QtWidgets, uic 
from revel import run_revel
from doordash import run_doordash
from uber import run_uber
from grubhub import run_grubhub
from threading import *

app = QtWidgets.QApplication([])
dlg = uic.loadUi("Program.ui")

def exec_all():
    dlg.OutputConsole.addItem("Scraping now...")
    run_revel()
    dlg.OutputConsole.addItem("Revel done...")
    run_doordash()
    dlg.OutputConsole.addItem("Doordash done...")
    run_uber()
    dlg.OutputConsole.addItem("Uber done...")
    run_grubhub()
    dlg.OutputConsole.addItem("Grubhub done...")
    dlg.OutputConsole.clear()
    dlg.OutputConsole.addItem("Opening spreadsheet...")
    # TODO: open browser to spreadsheet...
    
def webscrap_all_thread():
    webscrapThread = Thread(target=exec_all)
    webscrapThread.start()

def webscrap_revel_thread():
    webscrapThread = Thread(target=run_revel)
    webscrapThread.start()

def webscrap_doordash_thread():
    webscrapThread = Thread(target=run_doordash)
    webscrapThread.start()

def webscrap_uber_thread():
    webscrapThread = Thread(target=run_uber)
    webscrapThread.start()

def webscrap_grubhub_thread():
    webscrapThread = Thread(target=run_grubhub)
    webscrapThread.start()

dlg.RunAllButton.clicked.connect(webscrap_all_thread)
dlg.RevelButton.clicked.connect(webscrap_revel_thread)
dlg.DoordashButton.clicked.connect(webscrap_doordash_thread)
dlg.UberButton.clicked.connect(webscrap_uber_thread)
dlg.GrubhubButton.clicked.connect(webscrap_grubhub_thread)


dlg.show()
app.exec()