from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
#from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QApplication, QDockWidget, QListWidget, QMainWindow, QMessageBox, QTextEdit, QFrame, QGridLayout, QToolButton)
import queries
from csrLogic import CSRWidgets
#change 1
#change 1 to branch_2

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.createButtons()
        self.setUpMenus()
            
        self.setWindowTitle("CSR proving ground")
        
    def setUpMenus(self):
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        
    def createButtons(self):
        frmDesign = QFrame()
        frmDesign.setStyleSheet("background-color: rgb(255, 255, 255);")
        frmDesign.setLayout(CSRWidgets.createSaleButtons(self))
           
        self.textEdit = QTextEdit()
        self.setCentralWidget(frmDesign)

    def about(self):
        QMessageBox.about(self, "sup, dog.")


    def createMenus(self):
        
        CSRWidgets.createActions(self)
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.quitAct)

        self.editToolBar = self.addToolBar("Edit")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Something", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.addItems(("stuff"))
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Something Else", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.addItems(("more stuff"))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        
    def btnSaleClick(self):
        btnName = self.sender()
        design = str(btnName.objectName())
        CSRWidgets.loadDesignItem(self, design)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
