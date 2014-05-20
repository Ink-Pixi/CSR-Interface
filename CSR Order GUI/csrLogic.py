from PyQt5.QtWidgets import (QWidget, QGridLayout, QToolButton, QAction, QHBoxLayout, QVBoxLayout, QFrame, QLabel, 
                             QListWidgetItem, QScrollArea, QTreeWidgetItemIterator, QTreeWidgetItem, QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QFont, QColor
from PyQt5.QtCore import QSize, Qt
from queries import mysql_db
from builtins import super


class CSRWidgets(QWidget):
    def __init__(self):
        super(self, self).__init__()    
   
    def createDesignButtons(self, qryId):
        btnLayout = QGridLayout()       
        buttons = {}
        if qryId == 'default':
            qryResult = mysql_db.saleButtons(self)
        else:
            qryResult = mysql_db.searchDesigns(self,qryId)
            

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
        #self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, shortcut=Qt.Key_Return, statusTip="Find a design.",
        #                         triggered=self.btnSearch_Click)
        self.homeAct = QAction(QIcon('icon/home-icon.png'), '&Home', self, shortcut="Ctrl+H", statusTip="Return to home screen.", 
                               triggered=self.btnHome_Click)
        self.undoAct = QAction(QIcon('icon/undo.png'), '&Undo', self, shortcut=QKeySequence.Undo, 
                               statusTip="This will undo actions added to order", triggered=self.btnUndo_Click)
        #self.enterAct = QAction(self, shortcut=Qt.Key_Enter, triggered=self.btnSearch_Click)
        
    def loadDesignItem(self, sku_code):
        self.availableItems.clear()
        #self.orderItem.clear()
        des = mysql_db.designInfo(self, sku_code)
        
        self.vBox = QVBoxLayout()
        
        if not des:
            lblOpps = QLabel("We could put a .png or something here, something better than text, to let the CSR's know that " + \
                             "they searched an empty string or that the design they were looking for does not exist or that " + \
                             "they mistyped what they were looking for.", self)
            self.vBox.addWidget(lblOpps)
            CSRWidgets.changeCentralWidget(self, self.vBox)
        #print(des)        

        self.currentInfo = {}
        for i in des:
            CSRWidgets.item = QListWidgetItem()
            CSRWidgets.item.setText(str(i[7]))         
            self.currentInfo[i[7]] = (str(i[7]),str(i[8]),str(i[3]),str(i[9]),str(i[10]),str(i[11]))
            self.availableItems.addItem(CSRWidgets.item)
                
        smImage = self.currentInfo['T-Shirts'][3]
        hBox = QHBoxLayout()
        
        
        pix = QLabel()
        smImg = QPixmap("//wampserver/"+ smImage)
        myScaledPixmap = smImg.scaled(125,125, Qt.KeepAspectRatio)
        pix.setPixmap(myScaledPixmap)

        hBox.addWidget(pix)
        hFrame = QFrame()
        hFrame.setLayout(hBox)
        hFrame.setStyleSheet("background-color: rgb(255, 255, 255);")
        
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
            #print("//wampserver/" + str(i[10]))
        
        
        hBox.addStretch(1)
        hBox.setAlignment(self, Qt.AlignTop)
        
        #Create table to hold and display details of order order as they are selected from the tree. 
        CSRWidgets.tblOrderDetails = QTableWidget()
        CSRWidgets.tblOrderDetails.setColumnCount(6)        
        lstHeader = ["Design", "Category", "Type", "Size", "Price", "Qty" ]     
        CSRWidgets.tblOrderDetails.setHorizontalHeaderLabels(lstHeader)
        CSRWidgets.tblOrderDetails.setColumnWidth(0, 50)
        CSRWidgets.tblOrderDetails.setColumnWidth(1, 125)
        CSRWidgets.tblOrderDetails.setColumnWidth(2, 200)
        CSRWidgets.tblOrderDetails.setColumnWidth(3, 50)
        CSRWidgets.tblOrderDetails.setColumnWidth(4, 65)
        CSRWidgets.tblOrderDetails.setColumnWidth(5, 25)
        
        self.vBox.addWidget(hFrame)
        self.vBox.addWidget(CSRWidgets.tblOrderDetails)
        CSRWidgets.updateOrderDetails(self)
        #self.vBox.addStretch(1)
        
        CSRWidgets.changeCentralWidget(self, self.vBox)
        
    def undo(self):
        print("this will \"undo\" items added to the order.")
        self.searchBar.clear()
  
    def changeCentralWidget(self, widgetLayout):
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(widgetLayout)
        self.mainWidget.setMinimumSize(900, 800)
        if str(widgetLayout.objectName()) == "designPage":
            self.mainWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        
        self.scrollWidget = QScrollArea()
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setWidget(self.mainWidget)
        self.scrollWidget.setAlignment(Qt.AlignTop)
        
        self.setCentralWidget(self.scrollWidget)

    def loadGarmentInfo(self,sku_code,garment_type,garment_name):
        #print(garment_type)
        #Query the database to get all garments available for this particular SKU.      
        garm = mysql_db.garmentInfo(self, sku_code, garment_type)
        columnList = ["Design", "Size","Price", "Qty",""]
        
        #Set tree header/title stuff
        self.garmentTree.setHeaderLabels(columnList)
        self.garmentTree.setColumnCount(5)
        self.garmentTree.header().resizeSection(0, 280)
        self.garmentTree.header().resizeSection(1, 75)
        self.garmentTree.header().resizeSection(2, 45)
        self.garmentTree.header().resizeSection(3, 30)
        self.garmentTree.header().resizeSection(4, 10)
        
        #If there are no nodes in this tree yet, create the first one
        if self.garmentTree.topLevelItemCount() == 0:
            #print("NEW PARENT NODE")
            CSRWidgets.lblTotal = {}
            
            sku = QTreeWidgetItem(self.garmentTree)
            sku.setText(0, sku_code)
            sku.setBackground(0, QColor(180,180,180,127))
            sku.setBackground(1, QColor(180,180,180,127))
            sku.setBackground(2, QColor(180,180,180,127))
            sku.setBackground(3, QColor(180,180,180,127))
            sku.setBackground(4, QColor(180,180,180,127))
            sku.setFont(0, QFont("Helvetica",14,QFont.Bold))
            
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
            
            removeSku = QToolButton(self)
            removeSku.setIcon(QIcon("icon/close-widget.png"))
            removeSku.setIconSize(QSize(14, 14))
            removeSku.setAutoRaise(True)
            removeSku.clicked.connect(lambda: CSRWidgets.remove_widget(self))
            
            removeGarment = QToolButton(self)
            removeGarment.setIcon(QIcon("icon/close-widget.png"))
            removeGarment.setIconSize(QSize(14, 14))
            removeGarment.setAutoRaise(True)
            removeGarment.clicked.connect(lambda: CSRWidgets.remove_widget(self))

            CSRWidgets.lblTotal[str(sku_code + garment_name)] = QLabel()
            CSRWidgets.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
            CSRWidgets.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
            
            self.garmentTree.setItemWidget(sku, 4, removeSku)
            self.garmentTree.setItemWidget(garmName, 4, removeGarment)              
            self.garmentTree.setItemWidget(garmName, 3, CSRWidgets.lblTotal[str(sku_code + garment_name)])
            CSRWidgets.le = {}
            #Create all the garment types for the first node
            for i in garm:
                kiddo = QTreeWidgetItem(garmName)
                kiddo.setText(0, i[1])
                kiddo.setText(2, str(i[3]))
                kiddo.setText(1, i[2])
                kiddo.setText(3,"")
                kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                kiddo.setText(4,"      -")

                sku.setExpanded(True)
                garmName.setExpanded(True)
                kiddo.setExpanded(True)
                #print(le.objectName())

                
                
        #If items already exist in the tree, do stuff depending on what sku/garment was clicked.
        else:
            sku_match = 0       
            itSku = QTreeWidgetItemIterator(self.garmentTree) 

            #iterate through all tree items and see if anything matches the SKU we selected.           
            while itSku.value():
                #If the SKU we selected exists somewhere in the tree, set variable to indicate that.
                if itSku.value().text(0) == sku_code:
                    sku_match = 1
                #Collapse all non-parent nodes so we can selectively open the nodes we are currently working on below.
                if itSku.value().parent() != None:   
                    itSku.value().setExpanded(False)
                itSku += 1


            #if the SKU we've selected already exists in the tree, check to see if the garment we've selected exists also   
            if sku_match == 1:
                garm_match = 0
                #print("already", sku_code)
                #Create an iterator to iterate through all the elements in the tree.
                itGarment = QTreeWidgetItemIterator(self.garmentTree)
                #Open up iterator
                while itGarment.value():
                    #If BOTH the SKU and garment already exist in the tree, just expand it while collapsing all other items.
                    if itGarment.value().text(0) == garment_name and itGarment.value().parent().text(0) == sku_code:
                        #itGarment.value().parent().setExpanded(True)
                        #itGarment.value().setExpanded(True)
                        garm_match = 1
                        
                        itGarment.value().parent().setExpanded(True)
                        itGarment.value().setExpanded(True)
                        
                    itGarment += 1


                #If the selected garment does NOT exist in the tree for this SKU, create it.
                if garm_match == 0:
                    #create tree iterator
                    itSizes = QTreeWidgetItemIterator(self.garmentTree)
                    while itSizes.value():
                        #When the iterator hits the correct SKU, create the new garment node that doesn't exist yet.                         
                        if itSizes.value().text(0) == sku_code:
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
                            
                            removeGarment = QToolButton(self)
                            removeGarment.setIcon(QIcon("icon/close-widget.png"))
                            removeGarment.setIconSize(QSize(14, 14))
                            removeGarment.setAutoRaise(True)
                            removeGarment.clicked.connect(lambda: CSRWidgets.remove_widget(self))
                            CSRWidgets.lblTotal[str(sku_code + garment_name)] = QLabel(self.garmentTree)
                            CSRWidgets.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                            CSRWidgets.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                            
                            self.garmentTree.setItemWidget(garmName, 4, removeGarment)
                            self.garmentTree.setItemWidget(garmName, 3, CSRWidgets.lblTotal[str(sku_code + garment_name)])
                            #Create all the garment types for the node
                            #CSRWidgets.le = {}
                            for i in garm:
                                kiddo = QTreeWidgetItem(garmName)
                                kiddo.setText(0, i[1])
                                kiddo.setText(2, str(i[3]))
                                kiddo.setText(1, i[2])
                                kiddo.setText(3,"")
                                kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                                kiddo.setText(4,"      -")
                                itSizes.value().setExpanded(True)
                                garmName.setExpanded(True)
                                kiddo.setExpanded(True)
                        itSizes += 1       
 
 
                                       
                
            #If the SKU does NOT exist in the tree yet, but others already do, create this particular SKU.
            else:
                sku = QTreeWidgetItem(self.garmentTree)
                sku.setText(0, sku_code)
                sku.setBackground(0, QColor(180,180,180,127))
                sku.setBackground(1, QColor(180,180,180,127))
                sku.setBackground(2, QColor(180,180,180,127))
                sku.setBackground(3, QColor(180,180,180,127))
                sku.setBackground(4, QColor(180,180,180,127))
                sku.setFont(0, QFont("Helvetica",14,QFont.Bold) )
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
                removeSku = QToolButton(self)
                removeSku.setIcon(QIcon("icon/close-widget.png"))
                removeSku.setIconSize(QSize(14, 14))
                removeSku.setAutoRaise(True)
                removeSku.clicked.connect(lambda: CSRWidgets.remove_widget(self))
                
                removeGarment = QToolButton(self)
                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                removeGarment.setIconSize(QSize(14, 14))
                removeGarment.setAutoRaise(True)
                removeGarment.clicked.connect(lambda: CSRWidgets.remove_widget(self))
                CSRWidgets.lblTotal[str(sku_code + garment_name)] = QLabel(self.garmentTree)
                CSRWidgets.lblTotal[str(sku_code + garment_name)].setMaximumWidth(30)
                CSRWidgets.lblTotal[str(sku_code + garment_name)].setFont(QFont("Helvetica",10,QFont.Bold))
                
                self.garmentTree.setItemWidget(sku, 4, removeSku)
                self.garmentTree.setItemWidget(garmName, 4, removeGarment)  
                self.garmentTree.setItemWidget(garmName, 3, CSRWidgets.lblTotal[str(sku_code + garment_name)])
                #CSRWidgets.le = {}
                #Create all the garment types for the first node
                for i in garm:
                    kiddo = QTreeWidgetItem(garmName)
                    kiddo.setText(0, i[1])
                    kiddo.setText(2, str(i[3]))
                    kiddo.setText(1, i[2])
                    kiddo.setText(3,"")
                    kiddo.setFont(3, QFont("Helvetica",10,QFont.Bold) )
                    kiddo.setText(4,"      -")
                    sku.setExpanded(True)
                    garmName.setExpanded(True)
                    kiddo.setExpanded(True)

        self.treeDock.show()
        self.viewMenu.addAction(self.treeDock.toggleViewAction())        
        self.vBox.addWidget(self.garmentTree)
        
        self.treeDock.setWidget(self.garmentTree)
        self.addDockWidget(Qt.RightDockWidgetArea, self.treeDock)
        
    def remove_widget(self):
        btn = self.sender()
        btn.setFocus()
        root = self.garmentTree.invisibleRootItem()
        
        for item in self.garmentTree.selectedItems():
            (item.parent() or root).removeChild(item)        
            
        CSRWidgets.updateOrderDetails(self)
        
    #This function is needed for creating multiple lambda connections in a loop
    #NOT USING THIS FUNCTION STARTING WITH BRANCH 4.
    def make_callback(self,sku_code,garment_name):
        return lambda: CSRWidgets.sumQuantity(self, sku_code, garment_name)

      
    def sumQuantity(self, column):

        if self.text(column):
            #If this row has no Quantity yet, set it to zero.
            if self.text(3) == "":
                newNum = 0
            else:
                newNum = int(self.text(3))
            if self.parent().text(3) == "":
                newSum = 0
            else:
                newSum = int(self.parent().text(3))
                                               
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
            self.parent().setText(3,newSum)
            self.setText(3,newNum)
                        
    def updateOrderDetails(self):

        lstItems = []

        itOrders = QTreeWidgetItemIterator(self.garmentTree)
        while itOrders.value():
            if itOrders.value() != None:
                if itOrders.value().text(3) != "" and itOrders.value().text(2) != "":
                    if itOrders.value().parent().parent() != None:
                        txtItems = []
                        txtItems = [itOrders.value().parent().parent().text(0), itOrders.value().parent().text(0), itOrders.value().text(0),
                                    itOrders.value().text(1), str(format(float(itOrders.value().text(2)) * float(itOrders.value().text(3)), '.2f')), 
                                    itOrders.value().text(3)]
                        lstItems.append(txtItems)
            itOrders += 1
        print(lstItems)

        CSRWidgets.tblOrderDetails.setRowCount(len(lstItems))   
        print(len(lstItems))
        
        for i, row in enumerate(lstItems):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                item.setFlags(Qt.ItemIsEditable)
                CSRWidgets.tblOrderDetails.setItem(i, j, item)         
        self.vBox.addWidget(CSRWidgets.tblOrderDetails)
        

