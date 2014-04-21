from PyQt5.QtCore import Qt
#from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QApplication, QDockWidget, QListWidget, QMainWindow, QMessageBox, QLineEdit, QDesktopWidget, QTextEdit)
from csrLogic import CSRWidgets

class MainWindow(QMainWindow):
    '''Doc - __init__ Constructor'''
    def __init__(self):
        self.supervar = None
        super(MainWindow, self).__init__()
        
        self.setUpMenus()
       
        CSRWidgets.changeCentralWidget(self, CSRWidgets.createSaleButtons(self)) #Sets central widget on init.
        self.setWindowTitle("CSR Proving Ground")
        
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
        self.searchToolBar.addAction(self.enterAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Something", self)
        #dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.availableItems = QListWidget(dock)
        self.availableItems.setMinimumWidth(250)
        #self.availableItems.addItems(("stuff"))
        #self.availableItems.itemClicked.connect(self.itemClicked_Click)
        self.availableItems.currentTextChanged.connect(self.itemClicked_Click)
        dock.setWidget(self.availableItems)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget("Something Else", self)
        self.orderItem = QListWidget(dock)
        self.orderItem.setMinimumWidth(250)
        #self.orderItem.insertText(("more stuff"))
        dock.setWidget(self.orderItem)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        
    def btnSale_Click(self):
        btnName = self.sender()
        sku_code = str(btnName.objectName())
        CSRWidgets.loadDesignItem(self, sku_code)
        
    def btnHome_Click(self):
        CSRWidgets.changeCentralWidget(self, CSRWidgets.createSaleButtons(self))
        
    def btnSearch_Click(self):
        sku_code = self.searchBar.text()
        CSRWidgets.loadDesignItem(self, sku_code)

    def btnUndo_Click(self):
        CSRWidgets.undo(self)

    def itemClicked_Click(self, wtf):
        print(wtf)
        self.orderItem.addItem(wtf)
        #CSRWidgets.addItem(self, )
        
if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
