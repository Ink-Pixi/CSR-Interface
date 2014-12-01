import sys
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import (QApplication, QDockWidget, QListWidget, QMainWindow, QMessageBox, QLineEdit, QDesktopWidget, QTreeWidget, QTableWidgetItem, QGridLayout, QToolButton, QAction,
                             QTreeWidgetItemIterator, QPushButton, QLabel, QListWidgetItem, QHBoxLayout, QFrame, QTableWidget, QVBoxLayout, QWidget, QScrollArea, QTreeWidgetItem, QInputDialog,
                             QDialog, QTextEdit, QRadioButton)
from PyQt5.QtGui import QFont, QIcon, QKeySequence, QPixmap, QColor, QPalette
import mysql.connector
import pyodbc

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.gt = GarmentTree()

        self.createMenus()
        self.createToolbars()
        self.createStatusBar()
        self.createDockWindows()
       
        self.changeCentralWidget(self.createDesignButtons('default')) #Sets central widget on init.
        self.setWindowTitle("CSR Proving Ground")
        
        self.resize(1500, 900)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
         
    def about(self):
        QMessageBox.about(self, "C3PO", "His high exaltedness, the Great Jabba the Hutt, has decreed that you are to be terminated immediately.")

    def createMenus(self):
        self.createActions()
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")

        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createToolbars(self):
        self.homeToolBar = self.addToolBar("Home")
        self.homeToolBar.addAction(self.homeAct)
        self.homeToolBar.addAction(self.quitAct)

        self.searchToolBar = self.addToolBar("Search")
        self.searchToolBar.addAction(self.searchAct)
        
        self.searchBar = QLineEdit()
        self.searchBar.setMaximumWidth(150)
        self.searchBar.returnPressed.connect(self.btnSearch_Click)
        self.searchToolBar.addWidget(self.searchBar)
        
        self.searchToolBar.addSeparator()
        self.searchToolBar.addAction(self.undoAct)
        
        self.searchToolBar.addSeparator()
        
        btnNameChange = QPushButton('Add Name', self)
        btnNameChange.clicked.connect(self.btnNameChange_Click)
        
        self.lblVar1 = QLabel()
        self.lblVar1.setFont(QFont('Veranda', 14, QFont.Bold))
        #self.lblVar1.setMargin(10)
        self.lblVar1.setStyleSheet('padding-left:10px')
        
        self.lblTxtVar1 = QLabel()
        self.lblTxtVar1.setFont(QFont('Veranda', 14, QFont.Bold))
        #self.lblTxtVar1.setMargin(0)
        self.lblTxtVar1.setStyleSheet('padding-left:1px')
        
        self.lblVar2 = QLabel()
        self.lblVar2.setFont(QFont('Veranda', 14, QFont.Bold))
        self.lblVar2.setMargin(10)  
        
        self.lblTxtVar2 = QLabel()
        self.lblTxtVar2.setFont(QFont('Veranda', 14, QFont.Bold))
        self.lblTxtVar2.setMargin(0)              
        
        self.lblSkuName = QLabel()
        self.lblSkuName.setFont(QFont('Veranda', 14, QFont.Bold))
        self.lblSkuName.setMargin(10)
        
        self.searchToolBar.addWidget(btnNameChange)
        self.searchToolBar.addWidget(self.lblVar1)
        self.searchToolBar.addWidget(self.lblTxtVar1)
        self.searchToolBar.addWidget(self.lblVar2)
        self.searchToolBar.addWidget(self.lblTxtVar2)
        self.searchToolBar.addWidget(self.lblSkuName)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        dock = QDockWidget("Available Garments Types", self)
        #dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.availableItems = QListWidget(dock)
        self.availableItems.setMinimumWidth(350)
        self.availableItems.setMaximumWidth(350)
        #self.availableItems.addItems(("stuff"))
        self.availableItems.itemClicked.connect(self.itemClicked_Click)
        dock.setWidget(self.availableItems)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        dock.hide()

        self.dock = QDockWidget("Available Garment Sizes", self)
        self.orderItem = QTreeWidget(dock)
        #self.orderItem.setMinimumWidth(350)
        #self.orderItem.setMaximumWidth(350)
        #self.orderItem.insertText(("more stuff"))
        self.dock.setWidget(self.orderItem)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.viewMenu.addAction(self.dock.toggleViewAction())
        self.dock.hide()
        #Create a tree widget for use when the t-shirt is clicked.

   
        self.gt.treeDock.hide()
        
    def btnSale_Click(self):
        btnName = self.sender()
        sku_code = str(btnName.objectName())
        self.loadDesignItem(sku_code)
        
    def btnNameChange_Click(self):
        self.gt.changeCustName()
        
    def btnHome_Click(self):
        self.changeCentralWidget(self.createDesignButtons('default'))
        self.availableItems.clear()
        itSku = QTreeWidgetItemIterator(self.gt.garmentTree) 
#################################################################################           
        while itSku.value():
            if itSku.value().parent() != None:   
                itSku.value().setExpanded(False)
            itSku += 1
#################################################################################
        
    def btnSearch_Click(self):
        self.availableItems.clear()
        #self.orderItem.clear()
        searchTerm = self.searchBar.text()
        self.changeCentralWidget(self.createDesignButtons(searchTerm))

    def btnUndo_Click(self):
        self.undo()

    def itemClicked_Click(self):
        button = self.sender()
        txtItem = button.uniqueId
        self.gt.loadGarmentInfo(self.currentInfo[txtItem][2], self.currentInfo[txtItem][1], self.currentInfo[txtItem][0])
        #self.garmName.setExpanded(False)

    def createDesignButtons(self, qryId):
        btnLayout = QGridLayout()       
        buttons = {}
        if qryId == 'default':
            qryResult = mysql_db.sale_buttons(self)
        else:
            qryResult = mysql_db.search_designs(self,qryId)
            
        k = 0
        j = 0
        for i in range(len(qryResult)):
            t = qryResult[i]

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
                
            btnLayout.setObjectName("designPage")    

        return btnLayout
    
    def createActions(self):

        self.quitAct = QAction(QIcon('icon/exit.png'), "&Quit", self, shortcut="Ctrl+Q", statusTip="Quit the application", 
                               triggered=self.close)

        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)  
        self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, shortcut=Qt.Key_Enter, statusTip="Find a design.",
                                 triggered=self.btnSearch_Click)
        self.homeAct = QAction(QIcon('icon/home-icon.png'), '&Home', self, shortcut="Ctrl+H", statusTip="Return to home screen.", 
                               triggered=self.btnHome_Click)
        self.undoAct = QAction(QIcon('icon/undo.png'), '&Undo', self, shortcut=QKeySequence.Undo, 
                               statusTip="This will undo actions added to order", triggered=self.btnUndo_Click)
        
    def loadDesignItem(self, sku_code):
        self.lblSkuName.setText(sku_code)
        des = mysql_db.design_info(self, sku_code)
        
        #self.vBox = QVBoxLayout()
        self.winGrid = QGridLayout()
        
        if not des:
            lblOpps = QLabel("""We could put a .png or something here, something better than text, to let the CSR's know that 
                             they searched an empty string or that the design they were looking for does not exist or that 
                             they mistyped what they were looking for.""", self)
            self.grid.addWidget(lblOpps)
            self.changeCentralWidget(self, self.vBox)

        self.currentInfo = {}
        for i in des:
            self.item = QListWidgetItem()
            self.item.setText(str(i[7]))         
            self.currentInfo[i[7]] = (str(i[7]),str(i[8]),str(i[3]),str(i[9]),str(i[10]),str(i[11]),str(i[1]))
        smImage = self.currentInfo['T-Shirts'][3]

        hBox = QHBoxLayout()
        
        pix = QLabel()
        smImg = QPixmap("//wampserver/"+ smImage)
        myScaledPixmap = smImg.scaled(125,125, Qt.KeepAspectRatio)
        pix.setPixmap(myScaledPixmap)

        hBox.addWidget(pix)
       
        icons = {}
        for i in des:
            icons[(i)] = QToolButton(self)
            icons[(i)].setIcon(QIcon("//wampserver/" + str(i[10])))
            icons[(i)].setIconSize(QSize(44, 44))
            icons[(i)].setAutoRaise(True)
            icons[(i)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            #icons[(i)].setStyleSheet("background-color: rgb(255, 255, 255);")
            icons[(i)].setFont(QFont("Helvetica",8))
            #icons[(i)].setObjectName(str(i[7]))
            icons[(i)].setText(str(i[7]) + '\n' + str(i[3]))
            icons[(i)].uniqueId = str(i[7])
            icons[(i)].clicked.connect(self.itemClicked_Click)
            hBox.addWidget(icons[(i)])
        
        hBox.addStretch(1)
        
        hFrame = QFrame()
        hFrame.setLayout(hBox)
        hFrame.setMaximumHeight(200)
        hFrame.setStyleSheet("background-color: rgb(255, 255, 255);") 
        
        #Create table to hold and display details of order order as they are selected from the tree. 
        self.tblOrderDetails = QTableWidget(7, 0)
        self.tblOrderDetails.hide()
        #self.tblOrderDetails.setMaximumHeight(250)

        
        self.winGrid.addWidget(hFrame, 0, 0, 2, 2)
        #self.vBox.addWidget(hFrame)
        #self.vBox.addWidget(self.tblOrderDetails)
        self.winGrid.addWidget(self.tblOrderDetails, 2, 0, 1, 1)
        #self.winGrid.addWidget(self.totalBox, 2, 1, 1, 1)       
        #self.vBox.addStretch(1)

        self.changeCentralWidget(self.winGrid)
        
        self.gt.updateOrderDetails()
        self.gt.getCustomerName(sku_code)      
        
    def totalBox(self):
        lblTest = QLabel("test")
        lblSomething = QLabel("something else")
        
        totBox = QVBoxLayout()
        totBox.addWidget(lblTest)
        totBox.addWidget(lblSomething)
        totBox.addStretch()
        
        tFrame = QFrame()
        tFrame.setLayout(totBox)
        tFrame.setMinimumWidth(350)
        
        return tFrame
               
    def undo(self):
        print("this will \"undo\" items added to the order.")
        self.searchBar.clear()
  
    def changeCentralWidget(self, widgetLayout):
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(widgetLayout)
        #self.mainWidget.setMinimumSize(900, 800)
        if str(widgetLayout.objectName()) == "designPage":
            self.mainWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setWidget(self.mainWidget)
        self.scrollWidget.setAlignment(Qt.AlignTop)
        
        self.setCentralWidget(self.scrollWidget)
        
####################################################################################################################################################        
###### class for garment tree ######################################################################################################################        
####################################################################################################################################################
        
class GarmentTree(QTreeWidget):
    var1 = ""
    var2 = ""
        
    def __init__(self):
        super(GarmentTree, self).__init__()    
        
        self.treeDock = QDockWidget("Order Items", self)
        self.garmentTree = QTreeWidget(self.treeDock)
        self.garmentTree.setObjectName('garmentTree')
        self.garmentTree.itemClicked.connect(self.sumQuantity)
        self.garmentTree.itemClicked.connect(self.updateNameDesign)
        self.garmentTree.setMaximumWidth(490)
        self.garmentTree.setMinimumWidth(490)        
   
    def loadGarmentInfo(self,sku_code,garment_type,garment_name):

        #print(garment_type)
        #Query the database to get all garments available for this particular SKU.      
        garm = mysql_db.garment_info(self, sku_code, garment_type)
        columnList = ["Design", "Size","Price", "Qty","", ""]
        
        #Set tree header/title stuff
        self.garmentTree.setHeaderLabels(columnList)
        self.garmentTree.setColumnCount(6)
        self.garmentTree.header().resizeSection(0, 280)
        self.garmentTree.header().resizeSection(1, 75)
        self.garmentTree.header().resizeSection(2, 45)
        self.garmentTree.header().resizeSection(3, 30)
        self.garmentTree.header().resizeSection(4, 30)
        self.garmentTree.header().resizeSection(5, 30)
        
        
        #If there are no nodes in this tree yet, create the first one
        if self.garmentTree.topLevelItemCount() == 0:
            #print("NEW PARENT NODE")
            self.lblTotal = {}
            nm = QTreeWidgetItem(self.garmentTree)
            nm.setText(0, self.orderVars)
            nm.setBackground(0, QColor(180,180,180,127))
            nm.setBackground(1, QColor(180,180,180,127))
            nm.setBackground(2, QColor(180,180,180,127))
            nm.setBackground(3, QColor(180,180,180,127))
            nm.setBackground(4, QColor(180,180,180,127))
            nm.setBackground(5, QColor(180,180,180,127))
            nm.setFont(0, QFont("Helvetica",16,QFont.Bold))
            
            sku = QTreeWidgetItem(nm)
            sku.setText(0, sku_code)
            sku.setBackground(0, QColor(180,180,180,127))
            sku.setBackground(1, QColor(180,180,180,127))
            sku.setBackground(2, QColor(180,180,180,127))
            sku.setBackground(3, QColor(180,180,180,127))
            sku.setBackground(4, QColor(180,180,180,127))
            sku.setBackground(5, QColor(180,180,180,127))
            sku.setFont(0, QFont("Helvetica",12,QFont.Bold))
            
            #If the garment name does not exist we want to create a node for it. 
            garmName = QTreeWidgetItem(sku)
            garmName.setText(0, garment_name)
            garmName.setText(3, "")
            garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
            garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
            garmName.setBackground(0, QColor(230,230,230,127))
            garmName.setBackground(1, QColor(230,230,230,127))
            garmName.setBackground(2, QColor(230,230,230,127))
            garmName.setBackground(3, QColor(230,230,230,127))
            garmName.setBackground(4, QColor(230,230,230,127))
            garmName.setBackground(5, QColor(230,230,230,127))
            
            removeName = QToolButton(self)
            removeName.setIcon(QIcon("Icon/close-widget.png"))
            removeName.setIconSize(QSize(14,14))
            removeName.setAutoRaise(True)
            removeName.clicked.connect(self.remove_widget)
            
            removeSku = QToolButton(self)
            removeSku.setIcon(QIcon("icon/close-widget.png"))
            removeSku.setIconSize(QSize(14, 14))
            removeSku.setAutoRaise(True)
            removeSku.clicked.connect(self.remove_widget)
            
            removeGarment = QToolButton(self)
            removeGarment.setIcon(QIcon("icon/close-widget.png"))
            removeGarment.setIconSize(QSize(14, 14))
            removeGarment.setAutoRaise(True)
            removeGarment.clicked.connect(self.remove_widget)
            
            editName = QToolButton(self)
            editName.setIcon(QIcon("icon/undo.png"))
            editName.setIconSize(QSize(14, 14))
            editName.setAutoRaise(True)
            editName.clicked.connect(self.editTreeName)
            
            editSku = QToolButton(self)
            editSku.setIcon(QIcon("icon/undo.png"))
            editSku.setIconSize(QSize(14, 14))
            editSku.setAutoRaise(True)
            editSku.clicked.connect(self.editTreeSku)            

            self.lblTotal[str(sku_code + garment_name)] = QLabel()
            self.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
            self.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
            
            self.garmentTree.setItemWidget(nm, 4, removeName)
            self.garmentTree.setItemWidget(sku, 4, removeSku)
            self.garmentTree.setItemWidget(garmName, 4, removeGarment)              
            self.garmentTree.setItemWidget(garmName, 3, self.lblTotal[str(sku_code + garment_name)])
            self.garmentTree.setItemWidget(nm, 5, editName)
            self.garmentTree.setItemWidget(sku, 5, editSku)
            
            self.le = {}
            #Create all the garment types for the first node
            for i in garm:
                kiddo = QTreeWidgetItem(garmName)
                kiddo.setText(0, i[1])
                kiddo.setText(2, str(i[3]))
                kiddo.setText(1, i[2])
                kiddo.setText(3,"")
                kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                kiddo.setText(4,"-")
                
                nm.setExpanded(True)
                sku.setExpanded(True)
                garmName.setExpanded(True)
                kiddo.setExpanded(True)
                
        #If items already exist in the tree, do stuff depending on what sku/garment was clicked.
        else:          
            name_match = 0
            sku_match = 0       
            itSku = QTreeWidgetItemIterator(self.garmentTree) 

            #iterate through all tree items and see if anything matches the SKU we selected.           
            while itSku.value():
                if itSku.value().text(0) == self.orderVars:
                    name_match = 1
                    #print("NAME MATCHED!!!")
                #If the SKU we selected exists somewhere in the tree, set variable to indicate that.
                if itSku.value().text(0) == sku_code and itSku.value().parent().text(0) == self.orderVars:
                    sku_match = 1
                    #print("SKU MATCHED!!!")
                #Collapse all non-parent nodes so we can selectively open the nodes we are currently working on below.
                if itSku.value().parent() != None:   
                    itSku.value().setExpanded(False)
                itSku += 1

            if name_match == 1:
                #print("NAME MATCHED!!!!!!!!")
                #if the SKU we've selected already exists in the tree, check to see if the garment we've selected exists also   
                if sku_match == 1:
                    #print("SKU MATCHED!!!")
                    garm_match = 0
                    #print("already", sku_code)
                    #Create an iterator to iterate through all the elements in the tree.
                    itGarment = QTreeWidgetItemIterator(self.garmentTree)
                    #Open up iterator
                    while itGarment.value():
                        #If BOTH the SKU and garment already exist in the tree, just expand it while collapsing all other items.
                        if itGarment.value().text(0) == garment_name and itGarment.value().parent().text(0) == sku_code and itGarment.value().parent().parent().text(0) == self.orderVars:
                            #itGarment.value().parent().setExpanded(True)
                            #itGarment.value().setExpanded(True)
                            garm_match = 1
                            itGarment.value().parent().parent().setExpanded(True)
                            itGarment.value().parent().setExpanded(True)
                            itGarment.value().setExpanded(True)
                            
                        itGarment += 1
    
    
                    #If the selected garment does NOT exist in the tree for this SKU, create it.
                    if garm_match == 0:
                        #create tree iterator
                        itSizes = QTreeWidgetItemIterator(self.garmentTree)
                        while itSizes.value():
                            #When the iterator hits the correct SKU, create the new garment node that doesn't exist yet.                         
                            if itSizes.value().text(0) == sku_code and itSizes.value().parent().text(0) == self.orderVars:
                                #If the garment name does not exist we want to create a node for it. 
                                garmName = QTreeWidgetItem(itSizes.value())
                                garmName.setText(0, garment_name)
                                garmName.setText(3, "")
                                garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
                                garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
                                
                                
                                garmName.setBackground(0, QColor(230,230,230,127))
                                garmName.setBackground(1, QColor(230,230,230,127))
                                garmName.setBackground(2, QColor(230,230,230,127))
                                garmName.setBackground(3, QColor(230,230,230,127))
                                garmName.setBackground(4, QColor(230,230,230,127))
                                garmName.setBackground(5, QColor(230,230,230,127))
                                
                                removeGarment = QToolButton(self)
                                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                                removeGarment.setIconSize(QSize(14, 14))
                                removeGarment.setAutoRaise(True)
                                removeGarment.clicked.connect(self.remove_widget)
                                
                                self.lblTotal[str(sku_code + garment_name)] = QLabel(self.garmentTree)
                                self.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                                self.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                                
                                self.garmentTree.setItemWidget(garmName, 4, removeGarment)
                                self.garmentTree.setItemWidget(garmName, 3, self.lblTotal[str(sku_code + garment_name)])
                                #Create all the garment types for the node
                                #self.le = {}
                                for i in garm:
                                    kiddo = QTreeWidgetItem(garmName)
                                    kiddo.setText(0, i[1])
                                    kiddo.setText(2, str(i[3]))
                                    kiddo.setText(1, i[2])
                                    kiddo.setText(3,"")
                                    kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                                    kiddo.setText(4,"-")
                                    itSizes.value().setExpanded(True)
                                    garmName.setExpanded(True)
                                    kiddo.setExpanded(True)
                            itSizes += 1       
     
     
                                           
                    
                #If the SKU does NOT exist in the tree yet, but others already do, create this particular SKU.
                else:
                    #print("SAME NAME, DIFFERENT SKU!!!!! SKU = " + sku_code + " -- Name = " + self.orderVars)                       
                            
                    iterNewSku =  QTreeWidgetItemIterator(self.garmentTree) 
                    
                    while iterNewSku.value():
                        
                        if iterNewSku.value().childCount() > 0:
                            if iterNewSku.value().text(0) == self.orderVars:
                                                  
                                sku = QTreeWidgetItem(iterNewSku.value())     
                                sku.setText(0, sku_code)
                                sku.setBackground(0, QColor(180,180,180,127))
                                sku.setBackground(1, QColor(180,180,180,127))
                                sku.setBackground(2, QColor(180,180,180,127))
                                sku.setBackground(3, QColor(180,180,180,127))
                                sku.setBackground(4, QColor(180,180,180,127))
                                sku.setBackground(5, QColor(180,180,180,127))
                                sku.setFont(0, QFont("Helvetica",12,QFont.Bold) )
                                
                                garmName = QTreeWidgetItem(sku)
                                garmName.setText(0, garment_name)
                                garmName.setText(3, "")
                                garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
                                garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
                                garmName.setBackground(0, QColor(230,230,230,127))
                                garmName.setBackground(1, QColor(230,230,230,127))
                                garmName.setBackground(2, QColor(230,230,230,127))
                                garmName.setBackground(3, QColor(230,230,230,127))
                                garmName.setBackground(4, QColor(230,230,230,127))
                                garmName.setBackground(5, QColor(230,230,230,127)) 

                                removeSku = QToolButton(self)
                                removeSku.setIcon(QIcon("icon/close-widget.png"))
                                removeSku.setIconSize(QSize(14, 14))
                                removeSku.setAutoRaise(True)
                                removeSku.clicked.connect(self.remove_widget)
                                
                                removeGarment = QToolButton(self)
                                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                                removeGarment.setIconSize(QSize(14, 14))
                                removeGarment.setAutoRaise(True)
                                removeGarment.clicked.connect(self.remove_widget)
                                
                                editSku = QToolButton(self)
                                editSku.setIcon(QIcon("icon/undo.png"))
                                editSku.setIconSize(QSize(14, 14))
                                editSku.setAutoRaise(True)
                                editSku.clicked.connect(self.editTreeSku)                                
                                
                                self.lblTotal[str(sku_code + garment_name)] = QLabel(self.garmentTree)
                                self.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                                self.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                                
                                self.garmentTree.setItemWidget(sku, 4, removeSku)
                                self.garmentTree.setItemWidget(sku, 5, editSku)
                                self.garmentTree.setItemWidget(garmName, 4, removeGarment)  
                                self.garmentTree.setItemWidget(garmName, 3, self.lblTotal[str(sku_code + garment_name)])
                                #self.le = {}
                                #Create all the garment types for the first node
                                for i in garm:
                                    kiddo = QTreeWidgetItem(garmName)
                                    kiddo.setText(0, i[1])
                                    kiddo.setText(2, str(i[3]))
                                    kiddo.setText(1, i[2])
                                    kiddo.setText(3,"")
                                    kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold))
                                    kiddo.setText(4,"-")
                                    #nm.setExpanded(True)
                                    sku.setExpanded(True)
                                    garmName.setExpanded(True)
                                    kiddo.setExpanded(True)
                            
                        iterNewSku += 1

                        
            else:
                #print("NEW NAME")

                self.lblTotal = {}
                nm = QTreeWidgetItem(self.garmentTree)
                nm.setText(0, self.orderVars)
                nm.setBackground(0, QColor(180,180,180,127))
                nm.setBackground(1, QColor(180,180,180,127))
                nm.setBackground(2, QColor(180,180,180,127))
                nm.setBackground(3, QColor(180,180,180,127))
                nm.setBackground(4, QColor(180,180,180,127))
                nm.setBackground(5, QColor(180,180,180,127))
                nm.setFont(0, QFont("Helvetica",16,QFont.Bold))
                
                sku = QTreeWidgetItem(nm)
                sku.setText(0, sku_code)
                sku.setBackground(0, QColor(180,180,180,127))
                sku.setBackground(1, QColor(180,180,180,127))
                sku.setBackground(2, QColor(180,180,180,127))
                sku.setBackground(3, QColor(180,180,180,127))
                sku.setBackground(4, QColor(180,180,180,127))
                sku.setBackground(5, QColor(180,180,180,127))
                sku.setFont(0, QFont("Helvetica",12,QFont.Bold))
                
                
                #If the garment name does not exist we want to create a node for it. 
                garmName = QTreeWidgetItem(sku)
                garmName.setText(0, garment_name)
                garmName.setText(3, "")
                garmName.setFont(0,QFont("Helvetica",10,QFont.Bold))
                garmName.setFont(3,QFont("Helvetica",10,QFont.Bold))
                garmName.setBackground(0, QColor(230,230,230,127))
                garmName.setBackground(1, QColor(230,230,230,127))
                garmName.setBackground(2, QColor(230,230,230,127))
                garmName.setBackground(3, QColor(230,230,230,127))
                garmName.setBackground(4, QColor(230,230,230,127))
                garmName.setBackground(5, QColor(230,230,230,127))
                
                removeName = QToolButton(self)
                removeName.setIcon(QIcon("Icon/close-widget.png"))
                removeName.setIconSize(QSize(14,14))
                removeName.setAutoRaise(True)
                removeName.clicked.connect(self.remove_widget)                
                
                removeSku = QToolButton(self)
                removeSku.setIcon(QIcon("icon/close-widget.png"))
                removeSku.setIconSize(QSize(14, 14))
                removeSku.setAutoRaise(True)
                removeSku.clicked.connect(self.remove_widget)
                
                removeGarment = QToolButton(self)
                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                removeGarment.setIconSize(QSize(14, 14))
                removeGarment.setAutoRaise(True)
                removeGarment.clicked.connect(self.remove_widget)
                
                editName = QToolButton(self)
                editName.setIcon(QIcon("icon/undo.png"))
                editName.setIconSize(QSize(14, 14))
                editName.setAutoRaise(True)
                editName.clicked.connect(self.editTreeName)
                
                editSku = QToolButton(self)
                editSku.setIcon(QIcon("icon/undo.png"))
                editSku.setIconSize(QSize(14, 14))
                editSku.setAutoRaise(True)
                editSku.clicked.connect(self.editTreeSku)                            
    
                self.lblTotal[str(sku_code + garment_name)] = QLabel()
                self.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                self.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                
                self.garmentTree.setItemWidget(nm, 4, removeName)
                self.garmentTree.setItemWidget(sku, 4, removeSku)
                self.garmentTree.setItemWidget(nm, 5, editName)
                self.garmentTree.setItemWidget(sku, 5, editSku)
                self.garmentTree.setItemWidget(garmName, 4, removeGarment)              
                self.garmentTree.setItemWidget(garmName, 3, self.lblTotal[str(sku_code + garment_name)])
                self.le = {}
                #Create all the garment types for the first node
                for i in garm:
                    kiddo = QTreeWidgetItem(garmName)
                    kiddo.setText(0, i[1])
                    kiddo.setText(2, str(i[3]))
                    kiddo.setText(1, i[2])
                    kiddo.setText(3,"")
                    kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                    kiddo.setText(4,"-")
                    
                    nm.setExpanded(True)
                    sku.setExpanded(True)
                    garmName.setExpanded(True)
                    kiddo.setExpanded(True)
                    #print(le.objectName())
                
                
        self.treeDock.show()
        mainWin.viewMenu.addAction(self.treeDock.toggleViewAction())        
        
        self.treeDock.setWidget(self.garmentTree)
        mainWin.addDockWidget(Qt.RightDockWidgetArea, self.treeDock)
        
    def editTreeSku(self):
        #EditTreeSku.editTreeSku(self)
        btn = self.sender()
        btn.setFocus()
                
        selItems = self.garmentTree.selectedItems()
        
        ets = EditTreeSku()
        ets.editTreeSku(selItems)
        ets.show()
        mainWin.setEnabled(False)
                
    def editTreeName(self):
        #If a customer wants to change is name during ordering.
        
        #Grabs the item that was clicked in the tree and set focus to it to be double sure we get the correct values
        btn = self.sender()
        btn.setFocus()
        
        #loop through the items in the row selected in the tree and grab the information we need.
        for item in self.garmentTree.selectedItems():
            name = item.text(0)
            sku = item.child(0).text(0)
            
            #go get the type of variables that go on the shirt.
            self.var1 = mysql_db.get_first_var(self, sku)
            self.var2 = mysql_db.get_second_var(self, sku)
            
            #Get the name the customer wants to change to.
            inVar1, ok = QInputDialog.getText(self, "Enter "+self.var1, "Please enter "+self.var1+":")
            if ok and inVar1:
                newName = inVar1
                #set the tree to the new name.
                item.setText(0, newName)
                #reset the order variables for the order.
                self.orderVars = newName
                #if the name had a second variable we need to get that too.
                if name.find('::', 0, len(name)) > 0:
                    #ask for the second variable.
                    inVar2, ok = QInputDialog.getText(self, "Enter "+self.var2, "Please enter "+self.var2+":")
                    if ok and inVar2:
                        #reset the order variables with the second variable.
                        self.orderVars = newName + ' :: ' + inVar2
                        #reset the name in the tree.
                        item.setText(0, self.orderVars)

    def remove_widget(self):
        btn = self.sender()
        btn.setFocus()
        root = self.garmentTree.invisibleRootItem()
       
        for item in self.garmentTree.selectedItems():
            (item.parent() or root).removeChild(item)        
            
        self.updateOrderDetails()
        
    def sumQuantity(self, item, column):
        if item.text(column) and item.childCount() == 0 and item.parent() != None:
            #If this row has no Quantity yet, set it to zero.
            if item.text(3) == "":
                newNum = 0
            else:
                newNum = int(item.text(3))
            if item.parent().text(3) == "":
                newSum = 0
            else:
                newSum = int(item.parent().text(3))
                                               
            #If user clicks on the "-" sign in column 4, subtract 1
            if column == 4:
                if newNum > 0:
                    newNum = newNum - 1
                    if newSum > 0:                    
                        newSum = newSum - 1
                    
            #else if the user clicks anywhere BUT column 4, add number   
            else:
                newNum = newNum + 1                  
                newSum = newSum + 1

            #prepare the numbers for output    
            if newNum == 0:
                newNum = ""
            else:
                newNum = str(newNum)
                
            if newSum == 0:
                newSum = ""
            else:
                newSum = str(newSum)
            #Output    
            item.parent().setText(3,newSum)
            item.setText(3,newNum)
                      
    def updateOrderDetails(self):
        # If there is already a garment tree we want to clear out the old lists we do this to catch in an error
        # in case this function get's called before there is a tree build or grown, ha ha.
        if self.garmentTree:
            lstItems = []
            # Open a iterator to iterate through the tree (again) and build a list of lists of items in the tree to be added to the table.
            itOrders = QTreeWidgetItemIterator(self.garmentTree)
            while itOrders.value():
                if itOrders.value() != None:
                    # Below makes sure that there are values for both the price and the quantity.
                    if itOrders.value().text(3) != "" and itOrders.value().text(2) != "":
                        # This makes sure that we are at the correct level in the tree so we do try to add what shouldn't be added
                        if itOrders.value().parent().parent().parent() != None:
                            txtItems = []
                            txtItems = [itOrders.value().parent().parent().parent().text(0), itOrders.value().parent().parent().text(0), 
                                        itOrders.value().parent().text(0), itOrders.value().text(0), itOrders.value().text(1), 
                                        str(format(float(itOrders.value().text(2)) * float(itOrders.value().text(3)), '.2f')), 
                                        itOrders.value().text(3)]
                            lstItems.append(txtItems)
                itOrders += 1
            # A check to make sure the iterator picked up items from the list.
            if len(lstItems) > 0:
                # Build the table to hold the information from the tree.
                mainWin.tblOrderDetails.setRowCount(len(lstItems))
                mainWin.tblOrderDetails.setColumnCount(7)
                mainWin.tblOrderDetails.setAlternatingRowColors(True)
                lstHeader = ["Name", "Design", "Category", "Type", "Size", "Price", "Qty" ]     
                mainWin.tblOrderDetails.setHorizontalHeaderLabels(lstHeader)
                #self.tblOrderDetails.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
                mainWin.tblOrderDetails.setWordWrap(False)
                # Another check to make sure the list is there and has data, then we go through it and add data to the table.
                if lstItems:
                    for i, row in enumerate(lstItems):
                        for j, col in enumerate(row):
                            item = QTableWidgetItem(col)
                            item.setFlags(Qt.ItemIsEditable)
                            mainWin.tblOrderDetails.setItem(i, j, item)      
                    
                    mainWin.tblOrderDetails.resizeColumnsToContents()  
                      
                    #self.vBox.addWidget(self.tblOrderDetails)
                    mainWin.tblOrderDetails.show() 
                    testBox = mainWin.totalBox()
                    mainWin.winGrid.addWidget(testBox, 2, 1, 1, 1)
                    #print("hit update orders")  
            else:
                mainWin.tblOrderDetails.hide()
              
    def updateNameDesign(self):
        treeName = self.sender()
        self.getTreeVars(treeName)
        
        if str(treeName.objectName()) == 'garmentTree':
            #If top level (Name) node is selected.
            if treeName.currentItem().parent() == None:
                var = treeName.currentItem().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    mainWin.lblTxtVar1.setText(var[0])
                    mainWin.lblTxtVar2.setText(var[1])
                else: 
                    mainWin.lblTxtVar1.setText(var)
                    mainWin.lblVar2.hide()
                    mainWin.lblTxtVar2.hide()
                skuCode = treeName.currentItem().child(0).text(0)
                self.orderVars = (treeName.currentItem().text(0))
            #Fourth tree node selected (sizes)
            elif treeName.currentItem().child(0) == None:
                var = treeName.currentItem().parent().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    mainWin.lblTxtVar1.setText(var[0]) 
                    mainWin.lblTxtVar2.setText(var[1])
                else:
                    mainWin.lblTxtVar1.setText(var)
                    mainWin.lblVar2.hide()
                    mainWin.lblTxtVar2.hide()                    
                skuCode = treeName.currentItem().parent().parent().text(0)
                self.orderVars = (treeName.currentItem().parent().parent().parent().text(0))               
            #Second tree node is selected (Sku)
            elif treeName.currentItem().child(0).child(0) != None and treeName.currentItem().parent() != None:
                var = treeName.currentItem().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    mainWin.lblTxtVar1.setText(var[0])
                    mainWin.lblTxtVar2.setText(var[1])
                else:
                    mainWin.lblTxtVar1.setText(var)
                    mainWin.lblVar2.hide()
                    mainWin.lblTxtVar2.hide()                   
                skuCode = treeName.currentItem().text(0)
                self.orderVars = (treeName.currentItem().parent().text(0))
            #Third tree node selected (garment, T-Shirts)
            elif treeName.currentItem().child(0) != None and treeName.currentItem().parent().parent() != None:
                var = treeName.currentItem().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    mainWin.lblTxtVar1.setText(var[0])
                    mainWin.lblTxtVar2.setText(var[1])
                else:
                    mainWin.lblTxtVar1.setText(var)
                    mainWin.lblVar2.hide()
                    mainWin.lblTxtVar2.hide                    
                skuCode = treeName.currentItem().parent().text(0)    
                self.orderVars = (treeName.currentItem().parent().parent().text(0))
        mainWin.lblSkuName.setText(skuCode)
        mainWin.loadDesignItem(skuCode)         
        #self.updateOrderDetails(self)    
        
    def getTreeVars(self, garmTree):
        treeName = garmTree
        if str(treeName.objectName()) == 'garmentTree':
            #If top level (Name) node is selected.
            if treeName.currentItem().parent() == None:
                var = treeName.currentItem().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0]
                    self.var2 = var[1]
                else: 
                    self.var1 = var
                    self.var2 = None
            #Fourth tree node selected (sizes)
            elif treeName.currentItem().child(0) == None:
                var = treeName.currentItem().parent().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0] 
                    self.var2 = var[1]
                else:
                    self.var1 = var
                    self.var2 = None
            #Second tree node is selected (Sku)
            elif treeName.currentItem().child(0).child(0) != None and treeName.currentItem().parent() != None:
                var = treeName.currentItem().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0]
                    self.var2 = var[1]
                else:
                    self.var1 = var
                    self.var2 = None
            #Third tree node selected (garment, T-Shirts)
            elif treeName.currentItem().child(0) != None and treeName.currentItem().parent().parent() != None:
                var = treeName.currentItem().parent().parent().text(0)
                if var.find('::', 0, len(var)) > 0:
                    var = var.split(' :: ')
                    self.var1 = var[0]
                    self.var2 = var[1]
                else:
                    self.var1 = var
                    self.var2 = None
    
        return self.var1, self.var2
    
    def changeCustName(self):
        sku_code = mainWin.lblSkuName.text()
        self.var1 = mysql_db.get_first_var(self, sku_code)
        self.var2 = mysql_db.get_second_var(self, sku_code)
        
        inVar1, ok = QInputDialog.getText(self, "Enter "+self.var1, "Please enter "+self.var1+":")
        if ok and inVar1:
            self.orderVars = inVar1
            mainWin.lblTxtVar1.setText(inVar1)
            mainWin.lblVar1.setText(self.var1)
            
            if self.var2:
                inVar2, ok = QInputDialog.getText(self, "Enter "+self.var2, "Please enter "+self.var2+":")
                if ok and inVar2:
                    self.orderVars = self.orderVars +" :: "+ inVar2
                    mainWin.lblTxtVar2.setText(inVar2)
                    mainWin.lblVar2.setText(self.var2)

    def getCustomerName(self, sku_code = None):
        #Grabs the last var2 that was used.
        if self.var2 == None and mainWin.lblVar2 != None:
            self.var2 = mainWin.lblVar2.text()
        #var2 = mysql_db.get_second_var(self, sku_code)
        if not self.var1:
            var1 = mysql_db.get_first_var(self, sku_code)
            inVar1, ok = QInputDialog.getText(self, "Enter "+var1, "Please Enter "+var1+":")
            if ok:
                mainWin.lblVar1.setText(var1)
                mainWin.lblTxtVar1.setText(inVar1)
                self.orderVars = inVar1
                var2 = mysql_db.get_second_var(self, sku_code)
                if not var2:
                    self.var2 = None
                    mainWin.lblVar2.hide()
                    mainWin.lblTxtVar2.hide()
                    QApplication.instance().processEvents()               
                    self.orderVars = mainWin.lblTxtVar1.text()                    
                else:
                    inVar2, ok = QInputDialog.getText(self, "Enter "+var2, "Please Enter " +var2+ ":")
                    if ok:
                        mainWin.lblVar2.setText(var2)
                        mainWin.lblTxtVar2.setText(inVar2)
                        mainWin.var2 = inVar2
                        self.orderVars = self.orderVars + " :: " + inVar2
        elif self.var1 and not self.var2:
            var2 = mysql_db.get_second_var(self, sku_code)
            if var2:
                inVar2, ok = QInputDialog.getText(self, "Enter "+var2, "Please Enter " +var2+ ":")
                if ok:
                    mainWin.lblVar2.setText(var2)
                    mainWin.lblTxtVar2.setText(inVar2)
                    mainWin.var2 = inVar2
                    self.orderVars = self.orderVars + " :: " + inVar2
        elif self.var1 and self.var2:
            var1 = mysql_db.get_first_var(self, sku_code)
            var2 = mysql_db.get_second_var(self, sku_code)
            if not var2:
                self.var2 = None
                mainWin.lblVar2.hide()
                mainWin.lblTxtVar2.hide()
                QApplication.instance().processEvents()
                if mainWin.lblVar1.text() == var1:               
                    self.orderVars = mainWin.lblTxtVar1.text()
                else:
                    inVar1, ok = QInputDialog.getText(self, "Enter "+var1+":", "Please Enter "+var1+":")
                    if ok and inVar1:
                        mainWin.lblVar1.setText(var1)
                        mainWin.lblTxtVar1.setText(inVar1)
                        self.orderVars = inVar1
            else:
                if mainWin.lblVar1.text() == var1:               
                    self.orderVars = mainWin.lblTxtVar1.text()
                else:
                    inVar1, ok = QInputDialog.getText(self, "Enter "+var1+":", "Please Enter "+var1+":")
                    if ok and inVar1:
                        mainWin.lblVar1.setText(var1)
                        mainWin.lblTxtVar1.setText(inVar1)
                        self.orderVars = inVar1
                if mainWin.lblVar2.text() == var2:
                    self.orderVars = self.orderVars + " :: " + mainWin.lblTxtVar2.text()
                else:
                    inVar2, ok = QInputDialog.getText(self, "Enter "+var2+":", "Please Enter "+var2+":")
                    if ok and inVar2:
                        mainWin.lblVar2.setText(var2)
                        mainWin.lblTxtVar2.setText(inVar2)
                        self.orderVars = self.orderVars + " :: " + inVar2    
                        
class EditTreeSku(QDialog):
    def __init__(self, parent=None):
        super(EditTreeSku, self).__init__(parent)
        
        self.createHeader()
        
#         self.printOut = QTextEdit()
#         self.printOut.setFont(QFont("Helvetica", 11, QFont.Bold))
#         self.printOut.setReadOnly(True)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.createHeader())
#        self.mainLayout.addWidget(self.printOut)
        
        self.setLayout(self.mainLayout)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        bgColor = QPalette()
        bgColor.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(bgColor)
        #self.setWindoIcon('don\'t have one yet.')

        pos = mainWin.pos()

        x = pos.x() - ((self.width()/2) - (mainWin.width()/2)) 
        y = pos.y() - ((self.height()/2) - (mainWin.height()/2)) 
        
        self.setGeometry(x,y, 350, 500)        
        
    def createHeader(self):
        wht = QPalette()
        wht.setColor(wht.Foreground, Qt.white)
        
        lblTitle = QLabel("Change Color")
        lblTitle.setFont(QFont("Times", 12, QFont.Bold))
        lblTitle.setPalette(wht)
        
        btnClose = QToolButton()
        btnClose.setIcon(QIcon("icon\close-widget.png"))
        btnClose.setAutoRaise(True)
        btnClose.setIconSize(QSize(25,25))
        btnClose.setStyleSheet("QToolButton:hover {background-color: gray;}")
        btnClose.clicked.connect(lambda: self.close())
        btnClose.clicked.connect(lambda: mainWin.setEnabled(True))
        
        hbHeader = QHBoxLayout()
        hbHeader.addWidget(lblTitle)
        hbHeader.addWidget(btnClose)
        hbHeader.setContentsMargins(0, 0, 0, 0)
        
        return hbHeader
        
    def editTreeSku(self, selItems):
        
        lsTree = []
        for item in selItems:
            #Get sku from tree to use when deleting
            sku = item.text(0)
            print(sku)
            #Get the variables from the tree for use later on.
            treeVars = item.parent().text(0)
            print(treeVars)
            
            for i in range(item.childCount()):
                for j in range(item.child(i).childCount()):
                    if item.child(i).child(j).text(3) != "":
                        lsTree.append(item.child(i).child(j).text(0) + " " + item.child(i).child(j).text(1))

        aSkus = mysql_db.get_assoc_skus(self, sku)
        skus = aSkus.split(":")
        
        rbSkus = {}
        for sku in skus:
            if sku != item.text(0):

                rbSkus = QRadioButton(sku)
                rbSkus.setFont(QFont("Times", 10, QFont.Bold))

                img = mysql_db.get_tshirt_image(self, sku)

                pix = QLabel()
                smImg = QPixmap("//wampserver/"+img[0])
                myScaledPixmap = smImg.scaled(75, 75, Qt.KeepAspectRatio)
                pix.setPixmap(myScaledPixmap)
                
                teNotAvail = QTextEdit()
                teNotAvail.setMaximumHeight(100)
                teNotAvail.setReadOnly(True)
                teNotAvail.setMaximumWidth(250)
                
                hbSkus = QHBoxLayout()

                vbImg = QVBoxLayout()
                vbImg.addWidget(QLabel())
                vbImg.addWidget(pix)
                vbImg.addWidget(rbSkus)
                vbImg.addStretch(1)
                
                lblNotAvail = QLabel("Not Available:")
                lblNotAvail.setFont(QFont("Times", 10, QFont.Bold))
                
                vbNotAvail = QVBoxLayout()
                vbNotAvail.addWidget(lblNotAvail)
                vbNotAvail.addWidget(teNotAvail)
                vbNotAvail.addStretch(1)                
                
                hbSkus.addLayout(vbImg)
                hbSkus.addLayout(vbNotAvail)
                
                line = QFrame()
                #line.setGeometry(QRect(320, 150, 118, 3))
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                
                self.mainLayout.addWidget(line)                
                self.mainLayout.addLayout(hbSkus)
                
                availSkus = mysql_db.get_garments_sizes(self, sku)
                for row in lsTree:
                    if row not in availSkus:
                        teNotAvail.insertPlainText("   " + row + "\n")

                        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftClick = True
            self.offset = event.pos()
    
    def mouseMoveEvent(self, event):
        if self.leftClick == True:
            x=event.globalX()
            y=event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x-x_w, y-y_w)
            
    def mouseReleaseEvent(self, event):                             
        self.leftClick = False 
                                
class mysql_db():
    def mysql_connect(self):
        try:
            mysql_db.conn = mysql.connector.connect(user = 'AI_APP', password = 'rowsby01', host = 'wampserver', database = 'inkpixi', raise_on_warnings = True) 
            mysql_db.db = mysql_db.conn.cursor()
        except BaseException as e:
            QMessageBox.critical(self, 'Database Error', "Can not connect to the MySQL database: \n" + str(e), QMessageBox.Ok)
        
        return mysql_db.db
    
    def sale_buttons(self):
        sb = mysql_db.mysql_connect(self)
        sb.execute("""SELECT  ic.inventories_name, ic.inventories_lines_sku, ic.inventories_image_url 
                     FROM inventories_cache ic 
                     WHERE ic.on_sale = 1 
                     GROUP BY ic.inventories_lines_sku""")
        return sb.fetchall()
    
    
    def design_info(self, sku_code):
        di = mysql_db.mysql_connect(self)
        di.execute("""
        SELECT ic.inventories_id,ic.inventories_name,ic.inventories_price, ic.inventories_lines_sku, i.inventories_code,i.inventories_name,i.inventories_color, 
               it.inventories_types_name, it.inventories_types_id, ic.inventories_image_url, it.inventories_types_icon_url,it.inventories_types_icon_hover_url
        FROM inventories_cache ic 
        LEFT JOIN inventories i on ic.inventories_id = i.inventories_id
        LEFT JOIN inventories_types it on ic.join_inventories_types_id = it.inventories_types_id
        WHERE ic.inventories_lines_sku = '""" + sku_code + """'
        GROUP BY it.inventories_types_id
        ORDER BY it.inventories_types_id, i.inventories_name
        """)
        return di.fetchall()
    
    def get_tshirt_image(self, sku_code):
        gti = mysql_db.mysql_connect(self)
        gti.execute("""
                        SELECT ic.inventories_image_url
                        FROM inventories_cache ic 
                        LEFT JOIN inventories i on ic.inventories_id = i.inventories_id
                        LEFT JOIN inventories_types it on ic.join_inventories_types_id = it.inventories_types_id
                        WHERE ic.inventories_lines_sku = '"""+ sku_code +"""'
                          AND inventories_types_id = 1
                        GROUP BY it.inventories_types_id
                        ORDER BY it.inventories_types_id, i.inventories_name
                    """)
        return gti.fetchone()


    def search_designs(self, searchTerm):
        sd = mysql_db.mysql_connect(self)
        sd.execute(""" 
        SELECT  ic.inventories_name, ic.inventories_lines_sku, ic.inventories_image_url 
        FROM inventories_cache ic
        LEFT JOIN inventories_lines il on il.inventories_lines_id = ic.inventories_lines_id
        WHERE  il.inventories_lines_search_keywords like '%"""+ searchTerm +"""%' 
        GROUP BY il.inventories_lines_id
        ORDER BY ic.inventories_name, ic.inventories_lines_sku
        """)
        return sd.fetchall()


    def garment_info(self, sku_code, garment_type):
        gi = mysql_db.mysql_connect(self)
        gi.execute("""
        SELECT inv.inventories_code,inv.inventories_name, io.inventories_options_name, ic.inventories_price, ic.inventories_name
        FROM `inventories` inv 
        LEFT JOIN inventories_cache ic on ic.inventories_id = inv.inventories_id
        LEFT JOIN inventories_accessories ia on inventories_accessories_id = ic.inventories_global_accessories_ids
        LEFT JOIN inventories_options io on io.join_inventories_accessories_id = ia.inventories_accessories_id
        
        LEFT JOIN inventories_types it on it.inventories_types_id = inv.join_inventories_types_id
        WHERE ic.inventories_lines_sku = '""" + sku_code + """' 
        AND it.inventories_types_id = '""" + garment_type  + """'
        ORDER BY it.inventories_types_order,inv.inventories_code, ia.inventories_accessories_order, io.inventories_options_order
        """)
        return gi.fetchall() 
    
    def get_second_var(self, sku_code):
        if sku_code:
            db = mysql_db.mysql_connect(self)
            db.execute("SELECT var_2_text FROM designs WHERE sku_code = '"+sku_code+"'")
            ds = db.fetchone()
            
            sv = ds[0]
    
            return sv
    
    def get_first_var(self, sku_code):
        db = mysql_db.mysql_connect(self)
        db.execute("SELECT var_1_text FROM designs WHERE sku_code = '"+sku_code+"'")
        ds = db.fetchone()
        
        fv = ds[0]
        
        return fv
    
    def get_assoc_skus(self, sku_code):
        db = mysql_db.mysql_connect(self)
        db.execute("SELECT sku_link FROM designs WHERE sku_code = '"+sku_code+"'")
        ds = db.fetchone()
        
        return ds[0]
    
    def get_garments_sizes(self, sku_code):
        db = mysql_db.mysql_connect(self)
        #removed ic.inventories_lines_sku, 
        db.execute("""SELECT CONCAT(inv.inventories_name, ' ', io.inventories_options_name) garm_type_size
                    FROM `inventories` inv 
                    LEFT JOIN inventories_cache ic on ic.inventories_id = inv.inventories_id
                    LEFT JOIN inventories_accessories ia on inventories_accessories_id = ic.inventories_global_accessories_ids
                    LEFT JOIN inventories_options io on io.join_inventories_accessories_id = ia.inventories_accessories_id
                    LEFT JOIN inventories_types it on it.inventories_types_id = inv.join_inventories_types_id
                    WHERE ic.inventories_lines_sku = '"""+sku_code+"""'
                    ORDER BY it.inventories_types_order,inv.inventories_code, ia.inventories_accessories_order, io.inventories_options_order""")
        ds = db.fetchall()
        
        lst = []
        for row in ds:
            lst.append(row[0])
        
        return lst

class mssql_db():
    def mssql_connect(self):
        try:
            mssql_db.conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SQLSERVER; DATABASE=ImportExport; Trusted_Connection=yes')
            mssql_db.db = mssql_db.conn.cursor()
        except BaseException as e:
            QMessageBox.critical(self, 'Database Error', "Cannont connect to the MS SQL Server: \n" + str(e), QMessageBox.Ok)
        
        return mssql_db.db                          

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
