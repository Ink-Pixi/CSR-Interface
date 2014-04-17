from PyQt5.QtWidgets import QWidget, QGridLayout, QToolButton, QAction, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence
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
            buttons[(i)].setIconSize(QSize(120, 120))
            buttons[(i)].setAutoRaise(True)
            buttons[(i)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            buttons[(i)].setStyleSheet("background-color: rgb(255, 255, 255);")
            #buttons[(i)].setFont(QFont("Helvetica",10,QFont.Bold))
            buttons[(i)].setObjectName(str(t[1]))
            buttons[(i)].setText(str(t[1]) + '\n' + str(t[0]))
            buttons[(i)].clicked.connect(self.btnSaleClick)

            # add to the layout
            btnLayout.addWidget(buttons[(i)], j, k)   
            
            if k == 3:
                j += 1
                k = 0
            else:
                k += 1        
        
        return btnLayout        
    
    def createActions(self):

        self.quitAct = QAction(QIcon('icon/exit.png'), "&Quit", self, shortcut="Ctrl+Q", statusTip="Quit the application", 
                               triggered=self.close)

        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)  
        self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, shortcut=Qt.Key_Return, statusTip="Find a design.",
                                 triggered=self.btnSearch_Click)
        self.homeAct = QAction(QIcon('icon/home-icon.png'), '&Home', self, shortcut="Ctrl+H", statusTip="Return to home screen.", 
                               triggered=self.btnShow_Click)
        self.undoAct = QAction(QIcon('icon/undo.png'), '&Undo', self, shortcut=QKeySequence.Undo, 
                               statusTip="This will undo actions added to order", triggered=CSRWidgets.undo)
        
    def loadDesignItem(self, sku_code):
        des = mysql_db.designInfo(self, sku_code)
        print(des)        
        
        vBox = QVBoxLayout()
        pix = QLabel()
        pix.setPixmap(QPixmap("//wampserver/data/store/" + sku_code + "-zoom-box.jpg"))
        
        btnTest = QPushButton("Back")
        btnTest.clicked.connect(self.btnShow_Click)
        
        vBox.addWidget(pix)
        vBox.addWidget(btnTest)
        
        self.frmTest = QFrame()
        self.frmTest.setLayout(vBox)
        self.setCentralWidget(self.frmTest)
        
    def onShow(self):
        if not self.mainFrame:
            self.createButtons()
            self.setCentralWidget(self.mainFrame)

    def onHide(self):
        if self.mainFrame:
            self.mainFrame.deleteLater()
            self.mainFrame = None
            
    def undo(self):
        print("this will \"undo\" items added to the order.")
            

            
