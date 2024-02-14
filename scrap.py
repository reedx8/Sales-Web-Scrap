# Call all platforms from this main file
from PyQt5 import QtWidgets, uic#, QtCore
from revel import run_revel
from doordash import run_doordash
from uber import run_uber
from grubhub import run_grubhub

app = QtWidgets.QApplication([])
dlg = uic.loadUi("Program.ui")
# dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground)

# dlg.OutputConsole.addItem("Scraps live sales from 4 platforms")

# dlg.RunAllButton.setFocus()
# dlg.RunAllButton.setAutoDefault(True)


def exec_all():
    run_revel()
    run_doordash()
    run_uber()
    run_grubhub()

dlg.RunAllButton.clicked.connect(exec_all)
dlg.RevelButton.clicked.connect(run_revel)
dlg.DoordashButton.clicked.connect(run_doordash)
dlg.UberButton.clicked.connect(run_uber)
dlg.GrubhubButton.clicked.connect(run_grubhub)

dlg.show()
app.exec()