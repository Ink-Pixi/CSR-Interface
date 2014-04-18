from PyQt5.QtCore import Qt
#from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QApplication, QDockWidget, QListWidget, QMainWindow, QMessageBox, QTextEdit, QFrame, QLineEdit, QDesktopWidget,
                             QScrollArea, QWidget)
from csrLogic import CSRWidgets

class MainWindow(QMainWindow):
    def __init__(self):
        self.supervar = None
        super(MainWindow, self).__init__()
        
        self.createButtons()
        self.setUpMenus()
       
        self.setCentralWidget(self.scrollWidget)
        self.setWindowTitle("CSR proving ground")
        
        #Sizes and orients the App in the center of the screen.
        self.resize(1500, 900)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def setUpMenus(self):
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        
    def createButtons(self):
        mainWidget = QWidget()
        mainWidget.setLayout(CSRWidgets.createSaleButtons(self))
        mainWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setWidget(mainWidget)
        
        #self.mainFrame = QFrame()
        #self.mainFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        #self.mainFrame.setLayout(CSRWidgets.createSaleButtons(self))

    def about(self):
        QMessageBox.about(self, "sup?", "nothin, sup with you?")

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
        self.homeToolBar = self.addToolBar("Home")
        self.homeToolBar.addAction(self.homeAct)
        self.homeToolBar.addAction(self.quitAct)

        self.searchToolBar = self.addToolBar("Search")
        self.searchToolBar.addAction(self.searchAct)
        
        self.searchBar = QLineEdit()
        self.searchBar.setMaximumWidth(100)
        self.searchToolBar.addWidget(self.searchBar)
        
        self.searchToolBar.addSeparator()
        self.searchToolBar.addAction(self.undoAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Something", self)
        #dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.customerList = QListWidget(dock)
        self.customerList.setMinimumWidth(250)
        #self.customerList.addItems(("stuff"))
        self.customerList.itemClicked.connect(CSRWidgets.printSomething)
        dock.setWidget(self.customerList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Something Else", self)
        self.paragraphsList = QListWidget(dock)
        self.paragraphsList.setMinimumWidth(250)
        self.paragraphsList.addItems(("more stuff"))
        dock.setWidget(self.paragraphsList)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        
    def btnSaleClick(self):
        btnName = self.sender()
        sku_code = str(btnName.objectName())
        CSRWidgets.loadDesignItem(self,sku_code)
        CSRWidgets.onHide(self)
        
    def btnShow_Click(self):
        CSRWidgets.onShow(self)
        
    def btnSearch_Click(self):
        sku_code = self.searchBar.text()
        if self.mainFrame:
            CSRWidgets.onHide(self)
        CSRWidgets.loadDesignItem(self, sku_code)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
