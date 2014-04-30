from PyQt5.QtCore import Qt
#from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QApplication, QDockWidget, QListWidget, QMainWindow, QMessageBox, QLineEdit, QDesktopWidget, QTreeWidget)
from csrLogic import CSRWidgets

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setUpMenus()
       
        CSRWidgets.changeCentralWidget(self, CSRWidgets.createDesignButtons(self, 'default')) #Sets central widget on init.
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
        self.searchBar.setMaximumWidth(150)
        self.searchToolBar.addWidget(self.searchBar)
        
        self.searchToolBar.addSeparator()
        self.searchToolBar.addAction(self.undoAct)
        self.searchToolBar.addAction(self.enterAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Available Garments Types", self)
        #dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.availableItems = QListWidget(dock)
        self.availableItems.setMinimumWidth(350)
        self.availableItems.setMaximumWidth(350)
        #self.availableItems.addItems(("stuff"))
        #self.availableItems.itemClicked.connect(self.itemClicked_Click)
        self.availableItems.itemClicked.connect(self.itemClicked_Click)
        dock.setWidget(self.availableItems)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        self.dock = QDockWidget("Available Garment Sizes", self)
        self.orderItem = QTreeWidget(dock)
        #self.orderItem.setMinimumWidth(350)
        #self.orderItem.setMaximumWidth(350)
        #self.orderItem.insertText(("more stuff"))
        self.dock.setWidget(self.orderItem)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.viewMenu.addAction(self.dock.toggleViewAction())
        
        #Create a tree widget for use when the t-shirt is clicked.
        self.treeDock = QDockWidget("Order Items", self)
        self.garmentTree = QTreeWidget(self.treeDock)
        self.garmentTree.hide()
        
    def btnSale_Click(self):
        btnName = self.sender()
        sku_code = str(btnName.objectName())
        CSRWidgets.loadDesignItem(self, sku_code)
        
    def btnHome_Click(self):
        CSRWidgets.changeCentralWidget(self, CSRWidgets.createDesignButtons(self,'default'))
        self.availableItems.clear()
        #self.orderItem.clear()
        
    def btnSearch_Click(self):
        self.availableItems.clear()
        #self.orderItem.clear()
        searchTerm = self.searchBar.text()
        CSRWidgets.changeCentralWidget(self, CSRWidgets.createDesignButtons(self,searchTerm))

    def btnUndo_Click(self):
        CSRWidgets.undo(self)

    def itemClicked_Click(self):
        button = self.sender()
        txtItem = button.uniqueId
        CSRWidgets.loadGarmentInfo(self,self.currentInfo[txtItem][2],self.currentInfo[txtItem][1],self.currentInfo[txtItem][0])
        
    def showOrder(self):
        btn = self.sender()
        txtName = btn.objectName()
        print(txtName)
        print(self.grpBox[txtName])
        self.grpBox[txtName].show()
        
       
    def hideOrder(self):
        btn = self.sender()
        txtName = btn.objectName()
        print(txtName)
        self.grpBox[txtName].hide()
        
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
