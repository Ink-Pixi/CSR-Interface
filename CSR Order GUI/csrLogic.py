from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QAction, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLabel, 
                             QListWidgetItem, QScrollArea, QGroupBox)
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QFont
from PyQt5.QtCore import QSize, Qt
from queries import mysql_db


class CSRWidgets(QWidget):
    def __init__(self):
        super(CSRWidgets, self).__init__()    
    
    def createSaleButtons(self):
        btnLayout = QGridLayout()
        
        buttons = {}

        onSale = mysql_db.saleButtons(self)

        k = 0
        j = 0
        for i in range(len(onSale)):
            t = onSale[i]

            # keep a reference to the buttons
            buttons[(i)] = QToolButton(self)
            buttons[(i)].setIcon(QIcon("//wampserver/" + str(t[2])))
            buttons[(i)].setIconSize(QSize(180, 180))
            buttons[(i)].setAutoRaise(True)
            buttons[(i)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            buttons[(i)].setStyleSheet("background-color: rgb(255, 255, 255);")
            buttons[(i)].setFont(QFont("Helvetica",12,QFont.Bold))
            buttons[(i)].setObjectName(str(t[1]))
            buttons[(i)].setText(str(t[1]) + '\n' + str(t[0]))
            buttons[(i)].clicked.connect(self.btnSale_Click)

            # add to the layout
            btnLayout.addWidget(buttons[(i)], j, k)   
            
            if k == 3:
                j += 1
                k = 0
            else:
                k += 1  
                
            btnLayout.setObjectName("salePage")    

        return btnLayout
    
    def createActions(self):

        self.quitAct = QAction(QIcon('icon/exit.png'), "&Quit", self, shortcut="Ctrl+Q", statusTip="Quit the application", 
                               triggered=self.close)

        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)  
        self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, shortcut=Qt.Key_Return, statusTip="Find a design.",
                                 triggered=self.btnSearch_Click)
        self.homeAct = QAction(QIcon('icon/home-icon.png'), '&Home', self, shortcut="Ctrl+H", statusTip="Return to home screen.", 
                               triggered=self.btnHome_Click)
        self.undoAct = QAction(QIcon('icon/undo.png'), '&Undo', self, shortcut=QKeySequence.Undo, 
                               statusTip="This will undo actions added to order", triggered=self.btnUndo_Click)
        self.enterAct = QAction(self, shortcut=Qt.Key_Enter, triggered=self.btnSearch_Click)
        
    def addItem(self, design):
        print(design)
        
    def loadDesignItem(self, sku_code):
        self.availableItems.clear()
        des = mysql_db.designInfo(self, sku_code)
        
        vBox = QVBoxLayout()
        
        if not des:
            lblOpps = QLabel("We could put a .png or something here, something better than text, to let the CSR's know that " + \
                             "they searched an empty string or that the design they were looking for does not exist or that " + \
                             "they mistyped what they were looking for.", self)
            vBox.addWidget(lblOpps)
            CSRWidgets.changeCentralWidget(self, vBox)
        print(des)        

        currentInfo = {}
        for i in des:
            CSRWidgets.item = QListWidgetItem()
            CSRWidgets.item.setText(str(i[5]))
            
            currentInfo[i[5]] = (str(i[5]),str(i[8]),str(i[3]))
            self.availableItems.addItem(CSRWidgets.item)
                
        print(currentInfo)
        pix = QLabel()
        pix.setPixmap(QPixmap("//wampserver/data/store/" + sku_code + "-zoom-box.jpg"))
        
        btnTest = QPushButton("Back")
        btnTest.clicked.connect(self.btnHome_Click)
        
        vBox.addWidget(pix)
        vBox.addWidget(btnTest)
        
        CSRWidgets.changeCentralWidget(self, vBox)
        
    def undo(self):
        print("this will \"undo\" items added to the order.")
        self.searchBar.clear()
        
    def changeCentralWidget(self, widgetLayout):
       
        mainWidget = QWidget()
        mainWidget.setLayout(widgetLayout)
        if str(widgetLayout.objectName()) == "salePage":
            mainWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        scrollWidget = QScrollArea()
        scrollWidget.setWidgetResizable(True)
        scrollWidget.setWidget(mainWidget)
        
        self.setCentralWidget(scrollWidget)