import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (QApplication, QDockWidget, QListWidget, QMainWindow, QMessageBox, QLineEdit, QDesktopWidget, QTreeWidget, QTableWidgetItem, QGridLayout, QToolButton, QAction,
                             QTreeWidgetItemIterator, QPushButton, QLabel, QListWidgetItem, QHBoxLayout, QFrame, QTableWidget, QVBoxLayout, QWidget, QScrollArea, QTreeWidgetItem, QInputDialog,
                             QDialog, QTextEdit, QRadioButton, QSizePolicy, QFormLayout, QGroupBox, QTabWidget, QCompleter, QCheckBox)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPalette
import mysql.connector
import pyodbc
from PyQt5.Qt import QTextCursor, QComboBox

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.gt = GarmentTree()

        self.createMenus()
        self.createToolbars()
        self.createStatusBar()
        self.createDockWindows()
       
        self.setCentralWidget(self.createTabs())
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
        #self.homeToolBar = self.addToolBar("Home")

        
        self.searchToolBar = self.addToolBar("Search")
        
#         self.searchToolBar.addAction(self.homeAct)
#         self.searchToolBar.addSeparator()
                
        self.searchBar = QLineEdit()
        self.searchBar.setMaximumWidth(150)
        self.searchBar.setPlaceholderText('Search for a design')
        self.searchBar.returnPressed.connect(self.btnSearch_Click)
        self.searchToolBar.addWidget(self.searchBar)
        
        self.searchToolBar.addAction(self.searchAct)   
        
        self.searchToolBar.addSeparator()
        
        btnAddVars = QPushButton('Add Name', self)
        btnAddVars.clicked.connect(self.btnAddVars_Click)
        self.searchToolBar.addWidget(btnAddVars)
        
        self.searchToolBar.addSeparator()
        
        self.lblVar1 = QLabel()
        self.lblVar1.setFont(QFont('Veranda', 14, QFont.Bold))
        #self.lblVar1.setMargin(10)
        self.lblVar1.setStyleSheet('padding-left:10px')
        self.searchToolBar.addWidget(self.lblVar1)
        
        self.lblTxtVar1 = QLabel()
        self.lblTxtVar1.setFont(QFont('Veranda', 14, QFont.Bold))
        #self.lblTxtVar1.setMargin(0)
        self.lblTxtVar1.setStyleSheet('padding-left:1px')
        self.searchToolBar.addWidget(self.lblTxtVar1)
        
        self.lblVar2 = QLabel()
        self.lblVar2.setFont(QFont('Veranda', 14, QFont.Bold))
        self.lblVar2.setMargin(10)  
        self.searchToolBar.addWidget(self.lblVar2)
        
        self.lblTxtVar2 = QLabel()
        self.lblTxtVar2.setFont(QFont('Veranda', 14, QFont.Bold))
        self.lblTxtVar2.setMargin(0)              
        self.searchToolBar.addWidget(self.lblTxtVar2)
        
        self.lblSkuName = QLabel()
        self.lblSkuName.setFont(QFont('Veranda', 14, QFont.Bold))
        self.lblSkuName.setMargin(10)
        self.searchToolBar.addWidget(self.lblSkuName)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.searchToolBar.addWidget(spacer)
        
        self.searchToolBar.addSeparator()
        self.searchToolBar.addAction(self.quitAct)
        
        
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
        
    def btnAddVars_Click(self):
        self.gt.addVariables()
        
        
    def btnSearch_Click(self):
        self.availableItems.clear()
        #self.orderItem.clear()
        searchTerm = self.searchBar.text()
        self.clearLayout(self.vbSearch)
        self.vbSearch.addLayout(self.createDesignButtons(searchTerm))
        self.twMain.setCurrentIndex(0)

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
            qryResult = mysql_db.search_designs(self, qryId)
            
        
            
        k = 0
        j = 0
        if qryResult:
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
        else:
            QMessageBox.information(self, 'No Match', 'No designs match the search terms.  Please try again.', QMessageBox.Ok)
            
        return btnLayout
    
    def createTabs(self):
        self.twMain = QTabWidget()
        
        self.tabSearch = QWidget()
        self.tabOrder = QWidget()
        self.tabCust = QWidget()
        
        self.vbSearch = QVBoxLayout(self.tabSearch)
        self.vbSearch.addLayout(self.createDesignButtons('default'))
        self.twMain.addTab(self.tabSearch, 'Search')
        
        self.vbOrder = QVBoxLayout(self.tabOrder)
        self.twMain.addTab(self.tabOrder, 'Order Details')
        
        self.hbCust = QVBoxLayout(self.tabCust)
        self.hbCust.addLayout(self.createCustInfo())
        self.hbCust.addStretch()
        self.twMain.addTab(self.tabCust, 'Customer Details')
        
        return self.twMain
        
        
    
    def createActions(self):

        self.quitAct = QAction(QIcon('icon/exit.png'), "&Quit", self, shortcut="Ctrl+Q", statusTip="Quit the application", 
                               triggered=self.close)

        self.aboutAct = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)  
        self.searchAct = QAction(QIcon('icon/search.png'), '&Search', self, statusTip="Find a design.",
                                 triggered=self.btnSearch_Click)
#         self.homeAct = QAction(QIcon('icon/home-icon.png'), '&Home', self, shortcut="Ctrl+H", statusTip="Return to home screen.", 
#                                triggered=self.btnHome_Click)
        
    def loadDesignItem(self, sku_code):
        self.lblSkuName.setText(sku_code)
        des = mysql_db.design_info(self, sku_code)
        
        self.clearLayout(self.vbOrder)

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

        self.tblOrderDetails = self.createOrderTable()
        frmCust = self.showCustInfo()
        totBox = self.totalBox()
        
        vbDetails = QVBoxLayout()
        vbDetails.addWidget(totBox)
        vbDetails.addLayout(frmCust)
        vbDetails.addStretch()
        
        hbTbl = QHBoxLayout()
        hbTbl.addWidget(self.tblOrderDetails)
        hbTbl.addLayout(vbDetails)
        #self.hbTbl.addStretch()
        
        if self.leFirstName.text() != "":
            self.gbCustInfo.show()
            if self.cbPayType.currentIndex() != 0:
                self.gbPayInfo.show()
            #self.lblCustTitle.show()
            if self.chkDitto.isChecked() == False:
                self.gbShipInfo.show()
        
        self.vbOrder.addWidget(hFrame)
        self.vbOrder.addLayout(hbTbl)
        #self.vbOrder.addWidget(totBox)
       
        self.vbOrder.addStretch(1)
        
        self.updateOrderDetails()
        self.gt.getCustomerName(sku_code) 
        self.twMain.setCurrentIndex(1)
        
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())        
        
    def createOrderTable(self):
        #Create table to hold and display details of order order as they are selected from the tree. 
        tblOrderDetails = QTableWidget(7, 0)
        # Build the table to hold the information from the tree.
        tblOrderDetails.setMinimumHeight(500)
        #tblOrderDetails.setMaximumWidth(500)             
        tblOrderDetails.setColumnCount(7)
        tblOrderDetails.setAlternatingRowColors(True)
        head = tblOrderDetails.horizontalHeader()
        head.setStretchLastSection(True)           

        lstHeader = ["Variables", "Design", "Category", "Type", "Size", "Price", "Qty" ]     
        tblOrderDetails.setHorizontalHeaderLabels(lstHeader)
        tblOrderDetails.setWordWrap(False)        
        
        return tblOrderDetails        
        
    def updateOrderDetails(self):
        # If there is already a garment tree we want to clear out the old lists we do this to catch in an error
        # in case this function get's called before there is a tree build or grown, ha ha.
        od = self.tblOrderDetails
        if self.gt.garmentTree:
            lstItems = []
            totPcs = 0
            totPri = 0
            # Open a iterator to iterate through the tree (again) and build a list of lists of items in the tree to be added to the table.
            itOrders = QTreeWidgetItemIterator(self.gt.garmentTree)
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
                            totPcs += int(itOrders.value().text(3))
                            totPri += float(itOrders.value().text(2)) * float(itOrders.value().text(3))
                itOrders += 1
            # A check to make sure the iterator picked up items from the list.
            if len(lstItems) > 0:
                od.setRowCount(len(lstItems))
                # Another check to make sure the list is there and has data, then we go through it and add data to the table.
                if lstItems:
                    for i, row in enumerate(lstItems):
                        for j, col in enumerate(row):
                            item = QTableWidgetItem(col)
                            item.setFlags(Qt.ItemIsEditable)
                            od.setItem(i, j, item)      
                    
                    od.resizeColumnsToContents()  
                    #below will resize the table based on the contents of the length of the data in the rows and columns.
                    tblWidth = od.columnWidth(0) + od.columnWidth(1) + od.columnWidth(2) + od.columnWidth(3) + od.columnWidth(4) + od.columnWidth(5) + od.columnWidth(6) + od.columnWidth(7) + 15
                    #for the double digit numbering on left of the table.
                    if len(lstItems) > 9:
                        tblWidth = tblWidth + 10
                    #for the scroll bar when table hits its max height.
                    if len(lstItems) > 15:
                        tblWidth = tblWidth + 10 

                    od.setMaximumWidth(tblWidth)
                    od.setMinimumWidth(tblWidth)
                    od.show() 
                    self.lblTotPcs.setText(str(totPcs))
                    tenPct = False
                    if totPcs >= 1 and totPcs <= 2:
                        shipCost = 7.95
                    elif totPcs >= 3 and totPcs <= 6:
                        shipCost = 6.95
                    elif totPcs >= 7:
                        shipCost = 0.00
                    if totPcs >= 12:
                        tenPct = True
                    print(totPcs, tenPct)
                    self.lblTotShip.setText('$' + format(shipCost, '.2f'))
                    self.lblTotPri.setText('$' + format(totPri, '.2f'))
                    if tenPct == True:
                        totFinal = totPri - (totPri * .1)
                        self.lblTotPct.setText("10 Percent Off.")
                    else:
                        totFinal = totPri + shipCost
                        self.lblTotPct.setText(None)
                    self.lblTotFinal.setText('$' + format(totFinal, '.2f'))
                    
            else:
                od.hide()        
                self.gbTotal.hide()
                self.gbCustInfo.hide()
                self.gbShipInfo.hide()

        
    def totalBox(self):
        
        style = """QGroupBox 
                   { 
                         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                           stop: 0 #E0E0E0, stop: 1 #FFFFFF);
                         border: 2px solid gray;
                         border-radius: 5px;
                         margin-top: 2.5ex; /* leave space at the top for the title */
                         font-size: 14px;
                         font-weight: bold;
                         margin-left: 25px;
                    } 
                   QLabel 
                   { 
                       font-size: 12px; 
                       font-weight: bold; 
                       font-family: Veranda; 
                   } 
                   QGroupBox::title
                   {
                         subcontrol-origin: margin;
                         subcontrol-position: top center; /* position at the top center */
                         padding: 0 3px;
                    }
                    """            
        
        self.gbTotal = QGroupBox('Order Totals')
        self.gbTotal.setStyleSheet(style)
        self.gbTotal.setMaximumWidth(325)
        
        frmTotal = QFormLayout()

        self.lblTotPcs = QLabel()
        frmTotal.addRow(QLabel('Total Pieces:'), self.lblTotPcs)
        
        self.lblTotPri = QLabel()
        frmTotal.addRow(QLabel('Sub-Total:'), self.lblTotPri)
        
        self.lblTotShip = QLabel()
        frmTotal.addRow(QLabel('Shipping:'), self.lblTotShip)

        self.lblTotPct = QLabel()
        frmTotal.addRow(QLabel('Qty Discount:'), self.lblTotPct)
        
        self.lblTotFinal = QLabel()
        frmTotal.addRow(QLabel('Grand-Total:'), self.lblTotFinal)
        
        self.gbTotal.setLayout(frmTotal)
        
        return self.gbTotal
    
    def groupBoxStyle(self):
        style = """QGroupBox 
                   { 
                         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                           stop: 0 #E0E0E0, stop: 1 #FFFFFF);
                         border: 2px solid gray;
                         border-radius: 5px;
                         margin-top: 2.5ex; /* leave space at the top for the title */
                         font-size: 12px;
                         font-weight: bold;
 
                   } 
                   QLabel 
                   { 
                       font-size: 12px; 
                       font-weight: bold; 
                       font-family: Veranda; 
                   } 
                   QCheckBox 
                   { 
                       font-size: 12px; 
                       font-weight: bold; 
                       font-family: Veranda; 
                   } 
                   QGroupBox::title
                   {
                         subcontrol-origin: margin;
                         subcontrol-position: top center; /* position at the top center */
                         padding: 0 3px;
                    }
                    """
        
        return style        
        
    
    def custInfoForm(self):
        
        style = self.groupBoxStyle()
                
        gbCustInfo = QGroupBox('Customer\Billing Info')
        gbCustInfo.setStyleSheet(style)        
        gbCustInfo.setMaximumWidth(325)
        gbCustInfo.setMinimumWidth(325)
        gbCustInfo.setMaximumHeight(375)
        
        frmCustInfo = QFormLayout()
        
        self.leFirstName = QLineEdit()
        self.leFirstName.textChanged.connect(self.custInfoChanged)
        self.leFirstName.setObjectName('firstName')
        self.leFirstName.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('First Name:'), self.leFirstName)
        
        self.leLastName = QLineEdit()
        self.leLastName.textChanged.connect(self.custInfoChanged)
        self.leLastName.setObjectName('lastName')
        self.leLastName.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('Last Name:'), self.leLastName)

        self.leCompany = QLineEdit()
        self.leCompany.setPlaceholderText('Not Required')
        self.leCompany.textChanged.connect(self.custInfoChanged)
        self.leCompany.setObjectName('company')
        self.leCompany.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('Company:'), self.leCompany)
        
        self.leAdd1 = QLineEdit()
        self.leAdd1.textChanged.connect(self.custInfoChanged)
        self.leAdd1.setObjectName('add1')
        self.leAdd1.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('Address 1:'), self.leAdd1)
        
        self.leAdd2 = QLineEdit()
        self.leAdd2.textChanged.connect(self.custInfoChanged)
        self.leAdd2.setObjectName('add2')
        self.leAdd2.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('Address 2:'), self.leAdd2)
       
        self.leCity = QLineEdit()
        self.leCity.textChanged.connect(self.custInfoChanged)
        self.leCity.setObjectName('city')
        self.leCity.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('City:'), self.leCity)        

        states = mssql_db.getStates(self)
        
        stateCompleter = QCompleter(states)
        stateCompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)        
        stateCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        
        self.leState = QLineEdit()
        self.leState.setPlaceholderText("State")
        self.leState.setCompleter(stateCompleter)
        self.leState.textChanged.connect(self.custInfoChanged)
        self.leState.setObjectName('state')
        frmCustInfo.addRow(QLabel('State:'), self.leState)
        self.leState.setMaximumWidth(50)
        
        self.leZip = QLineEdit()
        self.leZip.textChanged.connect(self.custInfoChanged)
        self.leZip.setObjectName('zip')
        self.leZip.setMaximumWidth(75)
        frmCustInfo.addRow(QLabel('Zip:'), self.leZip)
        
        self.lePhone = QLineEdit()
        self.lePhone.textChanged.connect(self.custInfoChanged)
        self.lePhone.setObjectName('phone')
        self.lePhone.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('Phone:'), self.lePhone)
        
        self.leEmail = QLineEdit()
        self.leEmail.textChanged.connect(self.custInfoChanged)
        self.leEmail.setObjectName('email')
        self.leEmail.setMaximumWidth(200)
        frmCustInfo.addRow(QLabel('Email:'), self.leEmail)
        
        self.chkOffers = QCheckBox('Send product news and special offers.')
        frmCustInfo.addRow(self.chkOffers)
        
        self.chkDitto = QCheckBox('Shipping name and address same as billing.')
        self.chkDitto.clicked.connect(self.custInfoChanged)
        self.chkDitto.setObjectName('ditto')
        frmCustInfo.addRow(self.chkDitto)
        
        gbCustInfo.setLayout(frmCustInfo)
        
        return gbCustInfo        
    
    def shippingInfoForm(self):
        
        style = self.groupBoxStyle()
        
        frmShipInfo = QFormLayout()
        self.gbShippingInfo = QGroupBox('Shipping Info')
        self.gbShippingInfo.setStyleSheet(style)
        self.gbShippingInfo.setMaximumWidth(325)
        self.gbShippingInfo.setMinimumWidth(325)
        
        self.leShipFn = QLineEdit()
        self.leShipFn.textChanged.connect(self.custInfoChanged)
        self.leShipFn.setObjectName('shipFn')
        self.leShipFn.setMaximumWidth(200)
        frmShipInfo.addRow(QLabel('First Name:'), self.leShipFn)
        
        self.leShipLn = QLineEdit()
        self.leShipLn.textChanged.connect(self.custInfoChanged)
        self.leShipLn.setObjectName('shipLn')
        self.leShipLn.setMaximumWidth(200)
        frmShipInfo.addRow(QLabel('Last Name:'), self.leShipLn)
        
        self.leShipCompany = QLineEdit()
        self.leShipCompany.textChanged.connect(self.custInfoChanged)
        self.leShipCompany.setObjectName('shipCompany')
        self.leShipCompany.setPlaceholderText('Not Required')
        self.leShipCompany.setMaximumWidth(200)
        frmShipInfo.addRow(QLabel('Company:'), self.leShipCompany)
        
        self.leShipAdd1 = QLineEdit()
        self.leShipAdd1.textChanged.connect(self.custInfoChanged)
        self.leShipAdd1.setObjectName('shipAdd1')
        self.leShipAdd1.setMaximumWidth(200)
        frmShipInfo.addRow(QLabel('Address 1:'), self.leShipAdd1)
        
        self.leShipAdd2 = QLineEdit()
        self.leShipAdd2.textChanged.connect(self.custInfoChanged)
        self.leShipAdd2.setObjectName('shipAdd2')
        self.leShipAdd2.setMaximumWidth(200)
        frmShipInfo.addRow(QLabel('Address 2:'), self.leShipAdd2)
        
        self.leShipCity = QLineEdit()
        self.leShipCity.textChanged.connect(self.custInfoChanged)
        self.leShipCity.setObjectName('shipCity')
        self.leShipCity.setMaximumWidth(200)
        frmShipInfo.addRow(QLabel('City:'), self.leShipCity)
        
        states = mssql_db.getStates(self)
        
        stateCompleter = QCompleter(states)
        stateCompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)        
        stateCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        
        self.leShipState = QLineEdit()
        self.leShipState.setPlaceholderText("State")
        self.leShipState.setCompleter(stateCompleter)
        self.leShipState.textChanged.connect(self.custInfoChanged)
        self.leShipState.setObjectName('shipState')
        self.leShipState.setMaximumWidth(50)
        frmShipInfo.addRow(QLabel('State:'), self.leShipState)
        
        self.leShipZip = QLineEdit()
        self.leShipZip.textChanged.connect(self.custInfoChanged)
        self.leShipZip.setObjectName('shipZip')
        self.leShipZip.setMaximumWidth(75)
        frmShipInfo.addRow(QLabel('Zip:'), self.leShipZip)
        
        self.leShipPhone = QLineEdit()
        self.leShipPhone.textChanged.connect(self.custInfoChanged)
        self.leShipPhone.setObjectName('shipPhone')
        self.leShipPhone.setMaximumWidth(200)
        frmShipInfo.addRow(QLabel('Phone:'), self.leShipPhone)
        
        self.gbShippingInfo.setLayout(frmShipInfo)
        
        return self.gbShippingInfo
    
    def paymentForm(self):
        
        style = self.groupBoxStyle()
        
        self.frmPayInfo = QFormLayout()
        gbPayInfo = QGroupBox('Payment Info')
        gbPayInfo.setStyleSheet(style)
        gbPayInfo.setMaximumWidth(325)
        gbPayInfo.setMinimumWidth(325)

        payTypes = ['- Please Select Payment -', 'Credit Card', 'Check or Money Order']
                
        self.cbPayType = QComboBox()
        self.cbPayType.addItems(payTypes)
        self.cbPayType.currentIndexChanged.connect(self.cbPayTypeChanged)
        self.cbPayType.currentIndexChanged.connect(self.custInfoChanged)
        self.cbPayType.setObjectName('cbPayType')
        self.frmPayInfo.addRow(self.cbPayType)
        
        gbPayInfo.setLayout(self.frmPayInfo)
        
        return gbPayInfo
    
    def cbPayTypeChanged(self):
        if self.cbPayType.currentIndex() == 1:
            print('I am a credit card.')
            
            self.removePayInfo()
            self.frmPayInfo.addRow(self.cbPayType)
            
            ccTypes = [' - Please Select Card Type -', 'Visa', 'MasterCard', 'Discover', 'American Express']
            
            self.cbCardType = QComboBox()
            self.cbCardType.addItems(ccTypes)
            self.cbCardType.setObjectName('cardType')
            self.cbCardType.currentIndexChanged.connect(self.custInfoChanged)
            self.frmPayInfo.addRow(QLabel('Credit Card:'), self.cbCardType)
            
            self.leCardNumber = QLineEdit()
            self.frmPayInfo.addRow(QLabel('Card Number:'), self.leCardNumber)
            
            self.leCardExpire = QLineEdit()
            self.frmPayInfo.addRow(QLabel('Expiration Date:'), self.leCardExpire)
            
            self.leCardCode = QLineEdit()
            self.frmPayInfo.addRow(QLabel('Security Code:'), self.leCardCode)
            
            
        elif self.cbPayType.currentIndex() == 2:
            print('I am a money order')
            
            self.removePayInfo()
            self.frmPayInfo.addRow(self.cbPayType)
            
            self.checkNumber = QLineEdit()
            self.frmPayInfo.addRow(QLabel('Check\MO Number:'), self.checkNumber)
        else:
            self.removePayInfo()
        
    def removePayInfo(self):
        for cnt in reversed(range(self.frmPayInfo.count())):
            # takeAt does both the jobs of itemAt and removeWidget
            # namely it removes an item and returns it
            widget = self.frmPayInfo.takeAt(cnt).widget()
    
            if widget is not None: 
                if widget.objectName() != 'cbPayType':
                    # widget will be None if the item is a layout
                    widget.deleteLater()         
    
    def createCustInfo(self):

        btnReview = QToolButton()
        btnReview.setIcon(QIcon("icon/review.png"))
        btnReview.setAutoRaise(1)
        btnReview.setIconSize(QSize(50, 50))
        btnReview.clicked.connect(lambda: self.twMain.setCurrentIndex(1))
        
        custInfo = self.custInfoForm()
        shipInfo = self.shippingInfoForm()
        payInfo = self.paymentForm()
        
        gbSpecial = QGroupBox('Special Instructions')
        gbSpecial.setStyleSheet(self.groupBoxStyle())
        gbSpecial.setMaximumWidth(325)
        gbSpecial.setMaximumHeight(125)
        
        self.teSpecial = QTextEdit()
        self.teSpecial.setMaximumWidth(300)
        
        hbSpecial = QHBoxLayout()
        hbSpecial.addWidget(self.teSpecial)
        
        gbSpecial.setLayout(hbSpecial)
        
        gbGiftMsg = QGroupBox('Gift Message')
        gbGiftMsg.setStyleSheet(self.groupBoxStyle())
        gbGiftMsg.setMaximumWidth(325)
        gbGiftMsg.setMaximumHeight(125)
        
        self.teGiftMsg = QTextEdit()
        self.teGiftMsg.setMaximumWidth(300)
        hbGift = QHBoxLayout()
        hbGift.addWidget(self.teGiftMsg)
        
        gbGiftMsg.setLayout(hbGift)
                
        grdCust = QGridLayout()
        grdCust.addWidget(custInfo, 0, 0)
        grdCust.addWidget(shipInfo, 0, 1)
        grdCust.addWidget(payInfo, 0, 2)
        grdCust.addWidget(gbGiftMsg, 1, 0, 1, 1)
        grdCust.addWidget(gbSpecial, 1, 1, 1, 1)
        grdCust.addWidget(btnReview, 1, 2)
        
        return grdCust
    
    def showCustInfo(self):
        
        styleCust = """QGroupBox 
                   { 
                         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                           stop: 0 #E0E0E0, stop: 1 #FFFFFF);
                         border: 2px solid gray;
                         border-radius: 5px;
                         margin-top: 2.5ex; /* leave space at the top for the title */
                         font-size: 14px;
                         font-weight: bold;
                         margin-left: 25px;
                    } 
                   QLabel 
                   { 
                       font-size: 12px; 
                       font-weight: bold; 
                       font-family: Veranda; 
                   } 
                   QGroupBox::title
                   {
                         subcontrol-origin: margin;
                         subcontrol-position: top center; /* position at the top center */
                         padding: 0 3px;
                    }
                    """        
                    
        styleShip = """QGroupBox 
                   { 
                         background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                           stop: 0 #E0E0E0, stop: 1 #FFFFFF);
                         border: 2px solid gray;
                         border-radius: 5px;
                         margin-top: 2.5ex; /* leave space at the top for the title */
                         font-size: 14px;
                         font-weight: bold;
                         margin-left: 5px;
                    } 
                   QLabel 
                   { 
                       font-size: 12px; 
                       font-weight: bold; 
                       font-family: Veranda; 
                   } 
                   QGroupBox::title
                   {
                         subcontrol-origin: margin;
                         subcontrol-position: top center; /* position at the top center */
                         padding: 0 3px;
                    }
                    """                        
        
        
        self.gbCustInfo = QGroupBox('Customer\Billing Info')
        self.gbCustInfo.setStyleSheet(styleCust)
        self.gbCustInfo.setMinimumWidth(325)
        
        frmCustInfo = QFormLayout()
        
        self.lblTxtFname = QLabel()
        self.lblTxtFname.setText(self.leFirstName.text())
        #frmCustInfo.addRow(QLabel('First Name:'), self.lblTxtFname)
        
        self.lblTxtLname = QLabel()
        self.lblTxtLname.setText(self.leLastName.text())
        #frmCustInfo.addRow(QLabel('Last Name:'), self.lblTxtLname)
        
        hbName = QHBoxLayout()
        #hbName.addWidget(QLabel('First Name:'))
        hbName.addWidget(self.lblTxtFname)
        #hbName.addWidget(QLabel('Last Name:'))
        hbName.addWidget(self.lblTxtLname)
        hbName.addStretch()
        frmCustInfo.addRow(QLabel('Name:'), hbName)

        self.lblTxtCompany = QLabel()
        self.lblTxtCompany.setText(self.leCompany.text())
        frmCustInfo.addRow(QLabel('Company:'), self.lblTxtCompany)
                
        self.lblTxtAdd1 = QLabel()
        self.lblTxtAdd1.setText(self.leAdd1.text())
        frmCustInfo.addRow(QLabel('Address 1:'), self.lblTxtAdd1)
        
        self.lblTxtAdd2 = QLabel()
        self.lblTxtAdd2.setText(self.leAdd2.text())
        frmCustInfo.addRow(QLabel('Address 2:'), self.lblTxtAdd2)

        self.lblTxtCity = QLabel()
        if self.leCity.text() != '':
            self.lblTxtCity.setText(self.leCity.text() + ',')
        #frmCustInfo.addRow(QLabel('City:'), self.lblTxtCity)        
        
        self.lblTxtState = QLabel()
        self.lblTxtState.setText(self.leState.text())
        #frmCustInfo.addRow(QLabel('State:'), self.lblTxtState)
        
        self.lblTxtZip = QLabel()
        self.lblTxtZip.setText(self.leZip.text())
        #frmCustInfo.addRow(QLabel('Zip:'), self.lblTxtZip)
       
        hbAddy = QHBoxLayout()
        hbAddy.addWidget(self.lblTxtCity)
        hbAddy.addWidget(self.lblTxtState)
        hbAddy.addWidget(self.lblTxtZip)
        hbAddy.addStretch()
        frmCustInfo.addRow(QLabel('City/State/Zip:'), hbAddy)
       
        self.lblTxtPhone = QLabel()
        self.lblTxtPhone.setText(self.lePhone.text())
        frmCustInfo.addRow(QLabel('Phone:'), self.lblTxtPhone)
        
        self.lblTxtEmail = QLabel()
        self.lblTxtEmail.setText(self.leEmail.text())
        frmCustInfo.addRow(QLabel('Email:'), self.lblTxtEmail)
        
        self.lblTxtShipSame = QLabel()
        if self.chkDitto.isChecked():
            self.lblTxtShipSame.setText('*Shipping name and address same as billing.')

        frmCustInfo.addRow(self.lblTxtShipSame)
        
        self.gbCustInfo.setLayout(frmCustInfo)
        self.gbCustInfo.hide()
        
        
        self.gbShipInfo = QGroupBox('Shipping Info')
        self.gbShipInfo.setStyleSheet(styleShip)
        self.gbShipInfo.setMinimumWidth(325)
        frmShipInfo = QFormLayout()
        
        self.lblTxtShipFn = QLabel()
        self.lblTxtShipFn.setText(self.leShipFn.text())
        #frmShipInfo.addRow(QLabel('First Name:'), self.lblTxtShipFn)
        
        self.lblTxtShipLn = QLabel()
        self.lblTxtShipLn.setText(self.leShipLn.text())
        #frmShipInfo.addRow(QLabel('Last Name:'), self.lblTxtShipLn)
        
        hbShipName = QHBoxLayout()
        hbShipName.addWidget(self.lblTxtShipFn)
        hbShipName.addWidget(self.lblTxtShipLn)
        hbShipName.addStretch()
        frmShipInfo.addRow(QLabel('Name:'), hbShipName)
        
        self.lblTxtShipCompany = QLabel()
        self.lblTxtShipCompany.setText(self.leShipCompany.text())
        frmShipInfo.addRow(QLabel('Company:'), self.lblTxtShipCompany)
        
        self.lblTxtShipAdd1 = QLabel()
        self.lblTxtShipAdd1.setText(self.leShipAdd1.text())
        frmShipInfo.addRow(QLabel('Address 1:'), self.lblTxtShipAdd1)
        
        self.lblTxtShipAdd2 = QLabel()
        self.lblTxtShipAdd2.setText(self.leShipAdd2.text())
        frmShipInfo.addRow(QLabel('Address 2:'), self.lblTxtShipAdd2)
        
        self.lblTxtShipCity = QLabel()
        if self.leShipCity.text() != '':
            self.lblTxtShipCity.setText(self.leShipCity.text() + ',')
        
        self.lblTxtShipState = QLabel()
        self.lblTxtShipState.setText(self.leShipState.text())
        
        self.lblTxtShipZip = QLabel()
        self.lblTxtShipZip.setText(self.leShipZip.text())
        
        hbShipAdd = QHBoxLayout()
        hbShipAdd.addWidget(self.lblTxtShipCity)
        hbShipAdd.addWidget(self.lblTxtShipState)
        hbShipAdd.addWidget(self.lblTxtShipZip)
        hbShipAdd.addStretch()
        frmShipInfo.addRow(QLabel('City/State/Zip:'), hbShipAdd)
        
        self.lblTxtShipPhone = QLabel()
        self.lblTxtShipPhone.setText(self.leShipPhone.text())
        frmShipInfo.addRow(QLabel('Phone:'), self.lblTxtShipPhone)
                
        self.gbShipInfo.setLayout(frmShipInfo)
        self.gbShipInfo.hide()
        
        self.gbPayInfo = QGroupBox('Payment Details')
        self.gbPayInfo.setStyleSheet(styleCust)
        
        frmPayInfo = QFormLayout()
        self.lblTxtPayType = QLabel()
        self.lblTxtPayType.setText(self.cbPayType.currentText())
        frmPayInfo.addRow(QLabel('Payment Type:'), self.lblTxtPayType)
        
        self.lblTxtCardType = QLabel()
        self.lblTxtCardType.setText('test')
        frmPayInfo.addRow(QLabel('Card Type:'), self.lblTxtCardType)
        
        self.gbPayInfo.setLayout(frmPayInfo)
        self.gbPayInfo.hide()
        
        
        grdShipBill = QGridLayout()
        grdShipBill.addWidget(self.gbCustInfo, 0, 0, 2, 1)
        grdShipBill.addWidget(self.gbShipInfo, 0, 1)
        grdShipBill.addWidget(self.gbPayInfo, 2, 0)
        
        return grdShipBill
    
    def custInfoChanged(self, text):
        wdt = self.sender()
        print(wdt.objectName(), text)
        if wdt != None:
            self.gbCustInfo.show()
            #self.lblCustTitle.show()
            self.gbShipInfo.show()
            if wdt.objectName() == 'firstName':
                self.lblTxtFname.setText(text)
            elif wdt.objectName() == 'lastName':
                self.lblTxtLname.setText(text)
            elif wdt.objectName() == 'add1':
                self.lblTxtAdd1.setText(text)
            elif wdt.objectName() == 'add2':
                self.lblTxtAdd2.setText(text)
            elif wdt.objectName() == 'company':
                self.lblTxtCompany.setText(text)
            elif wdt.objectName() == 'city':
                self.lblTxtCity.setText(text + ',')                
            elif wdt.objectName() == 'state':
                self.lblTxtState.setText(text)
            elif wdt.objectName() == 'zip':
                self.lblTxtZip.setText(text)
            elif wdt.objectName() == 'phone':
                self.lblTxtPhone.setText(text)
            elif wdt.objectName() == 'email':
                self.lblTxtEmail.setText(text)
            elif wdt.objectName() == 'cardType':
                self.lblTxtCardType = self.cbCardType.currentText()
                print(self.cbCardType.currentText())
            elif wdt.objectName() == 'ditto':
                if wdt.isChecked() == True:
                    self.lblTxtShipSame.setText('*Shipping name and address same as billing.')
                    self.lblTxtShipSame.show()
                    self.gbShipInfo.hide()
                    self.gbShippingInfo.setEnabled(False)
                else:
                    self.lblTxtShipSame.hide()
                    self.gbShipInfo.show()
                    self.gbShippingInfo.setEnabled(True)
            if self.leFirstName.text() == '':
                self.gbCustInfo.hide()
                self.gbShipInfo.hide()
                self.gbPayInfo.hide()
            if wdt.objectName() == 'cbPayType':
                if wdt.currentText() != '- Please Select Payment -':
                    self.lblTxtPayType.setText(wdt.currentText())
                    self.gbPayInfo.show()
                else:
                    self.gbPayInfo.hide()
            #if the shipping and the billing addresses are the same.
            if self.chkDitto.isChecked() == False:
                if wdt.objectName() == 'shipFn':
                    self.lblTxtShipFn.setText(text)
                elif wdt.objectName() == 'shipLn':
                    self.lblTxtShipLn.setText(text)
                elif wdt.objectName() == 'shipCompany':
                    self.lblTxtShipCompany.setText(text)
                elif wdt.objectName() == 'shipAdd1':
                    self.lblTxtShipAdd1.setText(text)
                elif wdt.objectName() == 'shipAdd2':
                    self.lblTxtShipAdd2.setText(text)
                elif wdt.objectName() == 'shipCity':
                    self.lblTxtShipCity.setText(text + ',')
                elif wdt.objectName() == 'shipState':
                    self.lblTxtShipState.setText(text)
                elif wdt.objectName() == 'shipZip':
                    self.lblTxtShipZip.setText(text)
                elif wdt.objectName() == 'shipPhone':
                    self.lblTxtShipPhone.setText(text)
        
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
            nm.setToolTip(0, self.orderVars)
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
            removeName.clicked.connect(self.removeTreeItem)
            
            removeSku = QToolButton(self)
            removeSku.setIcon(QIcon("icon/close-widget.png"))
            removeSku.setIconSize(QSize(14, 14))
            removeSku.setAutoRaise(True)
            removeSku.clicked.connect(self.removeTreeItem)
            
            removeGarment = QToolButton(self)
            removeGarment.setIcon(QIcon("icon/close-widget.png"))
            removeGarment.setIconSize(QSize(14, 14))
            removeGarment.setAutoRaise(True)
            removeGarment.clicked.connect(self.removeTreeItem)
            
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
                                removeGarment.clicked.connect(self.removeTreeItem)
                                
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
                                removeSku.clicked.connect(self.removeTreeItem)
                                
                                removeGarment = QToolButton(self)
                                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                                removeGarment.setIconSize(QSize(14, 14))
                                removeGarment.setAutoRaise(True)
                                removeGarment.clicked.connect(self.removeTreeItem)
                                
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
                nm.setToolTip(0, self.orderVars)
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
                removeName.clicked.connect(self.removeTreeItem)                
                
                removeSku = QToolButton(self)
                removeSku.setIcon(QIcon("icon/close-widget.png"))
                removeSku.setIconSize(QSize(14, 14))
                removeSku.setAutoRaise(True)
                removeSku.clicked.connect(self.removeTreeItem)
                
                removeGarment = QToolButton(self)
                removeGarment.setIcon(QIcon("icon/close-widget.png"))
                removeGarment.setIconSize(QSize(14, 14))
                removeGarment.setAutoRaise(True)
                removeGarment.clicked.connect(self.removeTreeItem)
                
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
        ets.getAlternateSkus(selItems)
        ets.show()
        mainWin.setEnabled(False)
                
    def editTreeName(self):
        #If a customer wants to change the name or place during ordering.
        
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
        mainWin.updateOrderDetails()

    def removeTreeItem(self):
        #This is for removing items as cleaning and efficiently as possible for the CSR's.
        btn = self.sender()
        btn.setFocus()
        root = self.garmentTree.invisibleRootItem()

        for item in self.garmentTree.selectedItems():
            #if the item has a parent keep moving.
            if item.parent():
                #sku level, if the item's parent does not have a parent
                if not item.parent().parent():
                    itemParent = item.parent()
                    #if the item being deleted is the only child left to the parent then we want to remove the parent as well.
                    if itemParent.childCount() == 1:
                        (item.parent() or root).removeChild(item)
                        (item.parent() or root).removeChild(itemParent)
                    #if there are other children with the item that is being deleted we only want to delete the item.
                    else:
                        (item.parent() or root).removeChild(item)
                #if the items parent has a parent then we are dealing with garment styles (ie. T-shirts)
                else:
                    itemParent = item.parent()
                    if itemParent.childCount() == 1:
                        if itemParent.parent().childCount() == 1:
                            (itemParent.parent().parent() or root).removeChild(itemParent.parent())
                        else:
                            (item.parent() or root).removeChild(item)
                            (itemParent.parent() or root).removeChild(itemParent)
                    else:
                        (item.parent() or root).removeChild(item)
            #get rid of everything.            
            else:
                (item.parent() or root).removeChild(item)
        
        #mainWin.updateOrderDetails()
        self.updateRemovedVars()
    
    def updateRemovedVars(self):
        #This is for updating the tree variables the best possible way so that the CSR's can keep moving.
        #Open another iterator.
        itVars = QTreeWidgetItemIterator(mainWin.gt.garmentTree)
        #variable to hold the new variables if needed.
        oldVars = None  
        treeVars = None
        skuCode = None
        if mainWin.gt.garmentTree:
            while itVars.value():
                #if the orderVars of the last edited item are still in the tree we want to keep those..
                if itVars.value().text(0) == self.orderVars:
                    oldVars = itVars.value().text(0)
                    #next we want to get the sku value of the item that was selected.
                    skuCode = itVars.value().child(itVars.value().childCount() - 1).text(0)
                    for item in self.garmentTree.selectedItems():
                        if item:
                            #order variable level
                            if not item.parent():
                                skuCode = item.child(0).text(0)
                            #sku level
                            elif not item.parent().parent():
                                skuCode = item.text(0)
                            #garment level
                            else:
                                skuCode = item.parent().text(0)
                #if the orderVars are not in the tree anymore we need new ones.
                if itVars.value().text(0) != self.orderVars:
                    #grabs parents as we are iterating through
                    parent = itVars.value().parent()
                    #if the parent does not have a parent then we have our order variables  
                    if not parent:
                        # this will hold the last item needed for the order variables
                        treeVars = itVars.value().text(0)
                        skuCode = itVars.value().child(itVars.value().childCount() - 1).text(0)
                itVars += 1

            #if the variables haven't been assigned yet, it means they aren't in the tree
            if oldVars:
                self.orderVars = oldVars
            elif treeVars:
                self.orderVars = treeVars
            
            if self.orderVars:
                if self.orderVars.find('::', 0, len(self.orderVars)) > 0:
                    #split them up in case there are more than one so we can set the labels.
                    varis = self.orderVars.split(' :: ')
                    #set our labels
                    mainWin.lblTxtVar1.setText(varis[0])
                    mainWin.lblTxtVar2.setText(varis[1])
                    #get the second variable type for the variables(ie place, name, etc...)
                    self.var2 = mysql_db.get_second_var(self, skuCode)
                    #set the text label for the second variable
                    mainWin.lblVar2.setText(self.var2)
                else:
                    #otherwise we can just set the variable.
                    mainWin.lblTxtVar1.setText(self.orderVars)
                    mainWin.lblTxtVar2.setText(None)
                    mainWin.lblVar2.setText(None)

            if skuCode:
                #get the variable type for the first variable(ie place, name, etc...)
                self.var1 = mysql_db.get_first_var(self, skuCode)
                #set the text label for the second variable
                mainWin.lblVar1.setText(self.var1)
                #set the sku label
                mainWin.lblSkuName.setText(skuCode)             
                #load that design
                mainWin.loadDesignItem(skuCode)    
        else:
            print('nothing left homes.')
            
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
                      
    def updateNameDesign(self, item):
        treeName = self.sender()
       
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
                    mainWin.lblVar2.setText(None)
                    mainWin.lblTxtVar2.setText(None)
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
                    mainWin.lblVar2.setText(None)
                    mainWin.lblTxtVar2.setText(None)                 
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
                    mainWin.lblVar2.setText(None)
                    mainWin.lblTxtVar2.setText(None)                   
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
                    mainWin.lblVar2.setText(None)
                    mainWin.lblTxtVar2.setText(None)               
                skuCode = treeName.currentItem().parent().text(0)    
                self.orderVars = (treeName.currentItem().parent().parent().text(0))
        
        self.var1 = mysql_db.get_first_var(self, skuCode)
        self.var2 = mysql_db.get_second_var(self, skuCode)   
        if self.var2:
            mainWin.lblVar2.setText(self.var2)     
   
        mainWin.lblSkuName.setText(skuCode)
        mainWin.loadDesignItem(skuCode)
 
    def addVariables(self):
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
        if self.var2 == None and mainWin.lblVar2.text() != None:
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
                    mainWin.lblVar2.setText(None)
                    mainWin.lblTxtVar2.setText(None)
                    #self.orderVars = inVar1                   
                else:
                    inVar2, ok = QInputDialog.getText(self, "Enter "+var2, "Please Enter " +var2+ ":")
                    if ok:
                        mainWin.lblVar2.setText(var2)
                        mainWin.lblTxtVar2.setText(inVar2)
                        self.var2 = inVar2
                        self.orderVars = self.orderVars + " :: " + inVar2
        elif self.var1 and not self.var2:
            var2 = mysql_db.get_second_var(self, sku_code)
            if var2:
                inVar2, ok = QInputDialog.getText(self, "Enter "+var2, "Please Enter " +var2+ ":")
                if ok:
                    mainWin.lblVar2.setText(var2)
                    mainWin.lblTxtVar2.setText(inVar2)
                    self.var2 = inVar2
                    self.orderVars = self.orderVars + " :: " + inVar2
        elif self.var1 and self.var2:
            var1 = mysql_db.get_first_var(self, sku_code)
            var2 = mysql_db.get_second_var(self, sku_code)
            if not var2:
                self.var2 = None
                mainWin.lblVar2.setText(None)
                mainWin.lblTxtVar2.setText(None)
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

#########################################################################################################################################################################
### Class for widget pop up to change sku value in garment tree. ########################################################################################################
#########################################################################################################################################################################                        
class EditTreeSku(QDialog):
    newSku = ""
    
    def __init__(self, parent=None):
        super(EditTreeSku, self).__init__(parent)
        
        self.createHeader()
        
        self.gt = GarmentTree()
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.createHeader())
        
        self.setLayout(self.mainLayout)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        bgColor = QPalette()
        bgColor.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(bgColor)
        
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
        
    def getAlternateSkus(self, selItems):
        
        lsTree = []
        for item in selItems:
            #Get sku from tree to use when deleting
            selSku = item.text(0)
            #Get the variables from the tree for use later on (ie Name and Place).
            treeVars = item.parent().text(0)
            self.gt.orderVars = treeVars
            
            lsGarmName = []
            lsGarmQty = []
            for i in range(item.childCount()):
                #get a list of all garment types that have been added to the tree for the sku.
                lsGarmName.append(item.child(i).text(0))
                for j in range(item.child(i).childCount()):
                    #get a list of all the garment names and sizes that have a quantity of more that one for each garment type
                    if item.child(i).child(j).text(3) != "":
                        lsTree.append(item.child(i).child(j).text(0) + " " + item.child(i).child(j).text(1))
                        lsGarmQty.append([item.child(i).child(j).text(0) + " " + item.child(i).child(j).text(1), item.child(i).child(j).text(3)]) 
        #get a list of all the skus that are associated with the sku that was selected.                        
        aSkus = mysql_db.get_assoc_skus(self, selSku)
        skus = aSkus.split(":")
        
        layout = QGridLayout()
        rbSkus = {}
        hbSkus = {}
        i = 0
        j = 0
        #loop through the list of skus and create buttons and a list of items not available for each associated sku.
        for sku in skus:
            #so we do see the sku that was selected in the dialog.
            if sku != item.text(0):
                
                rbSkus = QRadioButton(sku)
                rbSkus.toggled.connect(self.setSku)
                rbSkus.setFont(QFont("Times", 10, QFont.Bold))
                
                #get the t-shirt image from the database
                img = mysql_db.get_tshirt_image_color(self, sku)
                #get color of the t-shirt
                col = img[1]
                
                pix = QLabel()
                smImg = QPixmap("//wampserver/"+img[0])
                myScaledPixmap = smImg.scaled(75, 75, Qt.KeepAspectRatio)
                pix.setPixmap(myScaledPixmap)
                
                #text edit to display items that are not available in the sku that were in the selected sku.
                teNotAvail = QTextEdit()
                teNotAvail.setMaximumHeight(100)
                teNotAvail.setReadOnly(True)
                teNotAvail.setMaximumWidth(200)
                teNotAvail.insertHtml("<b><u>Not Available:</u></b><br/>\n")
                
                hbSkus[sku] = QHBoxLayout()
                hbSkus[sku].setObjectName(sku)

                vbImg = QVBoxLayout()
                vbImg.setObjectName("img")
                vbImg.addWidget(QLabel())
                vbImg.addWidget(pix)
                vbImg.addWidget(rbSkus)
                vbImg.addStretch(1)
                
                lblColor = QLabel(col)
                lblColor.setFont(QFont("Times", 10, QFont.Bold))
                
                vbNotAvail = QVBoxLayout()
                vbNotAvail.setObjectName('not avail')
                vbNotAvail.addWidget(lblColor)
                vbNotAvail.addWidget(teNotAvail)
                vbNotAvail.addStretch(1)                
                
                lnColor = QPalette()
                lnColor.setColor(self.foregroundRole(), Qt.white)
                
                vline = QFrame()
                vline.setFrameShape(QFrame.VLine)
                vline.setLineWidth(4)
                vline.setPalette(lnColor)
                                
                hbSkus[sku].addLayout(vbImg)
                hbSkus[sku].addLayout(vbNotAvail)
                hbSkus[sku].addWidget(vline)
                
                hline = QFrame()
                hline.setFrameShape(QFrame.HLine)
                hline.setPalette(lnColor)
                hline.setLineWidth(3)
                
                vbSkus = QVBoxLayout()
                vbSkus.setObjectName('vb sku')
                vbSkus.addWidget(hline)
                vbSkus.addLayout(hbSkus[sku])
                
                layout.addLayout(vbSkus, j, i)
                layout.setObjectName('layout')
                
                availSkus = mysql_db.get_garments_sizes(self, sku)
                for row in lsTree:
                    if row not in availSkus:
                        teNotAvail.insertPlainText("   " + row + "\n")
                teNotAvail.moveCursor(QTextCursor.Start)
                
                if j == 3:
                    i += 1
                    j = 0
                else:
                    j += 1
        
        self.mainLayout.addLayout(layout)
                
        btnLayout = QHBoxLayout()
        
        btnChangeSku = QPushButton('Change SKU')
        btnChangeSku.clicked.connect(lambda: self.changeSku(lsGarmName, lsGarmQty))
        btnChangeSku.clicked.connect(lambda: self.removeOldSku(selItems))
        btnLayout.addWidget(btnChangeSku)
        
        btnCancel = QPushButton('Cancel')
        btnCancel.clicked.connect(self.reject)
        btnCancel.clicked.connect(lambda: mainWin.setEnabled(True))
        btnLayout.addWidget(btnCancel)
        
        self.mainLayout.addLayout(btnLayout)

    def setSku(self):
        rbSku = self.sender()
        self.newSku = rbSku.text()

    def changeSku(self, garmName, garmQtys):
        #garmName = list of garment names that were loaded for the sku that is being changed.
        #garmQtys = list of lists of the qtys that were attached to each individual garments.
        
        #make sure a radio button was selected
        if not self.newSku:
            QMessageBox.information(self, "Select SKU", "Please Select a SKU!", QMessageBox.Ok)
        else:
            #get information of the design
            availGarmTypes = mysql_db.design_info(self, self.newSku)
            #create a list and fill it with only the garment types available for that design
            lsAvailTypes = []
            for garm in availGarmTypes:
                lsAvailTypes.append(garm[7])

            for name in garmName:
                #if the garment type is in the list keep going.
                if name in lsAvailTypes:
                    #grabs the id for the garment name (i.e. T-Shirt)
                    garmID = mysql_db.get_garment_type_id(self, name)
                    #loads the tree garments for the new sku, based on what was in the tree
                    mainWin.gt.loadGarmentInfo(self.newSku, str(garmID), name)
            #this will refresh the design buttons on the top so the sku's match up.
            mainWin.loadDesignItem(self.newSku)
            
            #Update new sku with the order quantities of the old sku
            itChange = QTreeWidgetItemIterator(mainWin.gt.garmentTree)
            #First open yet another iterator.
            while itChange.value():        
                #if the variables and the sku match...keep going.
                if itChange.value().text(0) == self.newSku and itChange.value().parent().text(0) == self.gt.orderVars:
                    tot = 0
                    #get a count of all of the garment types for the sku.
                    for j in range(itChange.value().childCount()):
                        #set item equal to the garment type (ie T-Shirts)
                        item = itChange.value().child(j)
                        #get a count of all the styles and sizes for the garment type.
                        for k in range(item.childCount()):
                            #for every style and size that had a quantity we want to add that quantity to the new sku that was added.
                            for i in range(len(garmQtys)):
                                #make sure the style and size match.
                                if item.child(k).text(0) + " " + item.child(k).text(1) == garmQtys[i][0]:
                                    #if there is a match set the quantity on the new sku
                                    item.child(k).setText(3, garmQtys[i][1]) 
                                    #finally keep a running total for each garment and add the total to the garment type itself.
                                    if int(garmQtys[i][1]) > 0:
                                        tot += int(garmQtys[i][1])
                                        item.setText(3, str(tot))
                        tot = 0
                itChange += 1
            self.close()
            mainWin.setEnabled(True)
                
    def removeOldSku(self, selItems):
        #make sure a radio button was selected
        if self.newSku:
            root = mainWin.gt.garmentTree.invisibleRootItem()
            for item in selItems:
                (item.parent() or root).removeChild(item)
            
            #this will update the table with the new sku and proper values from the old sku.
            mainWin.updateOrderDetails()
        else: pass
                                                    
    def mousePressEvent(self, event):
        #This is to be able to move the window around without a frame
        if event.button() == Qt.LeftButton:
            self.leftClick = True
            self.offset = event.pos()
        else:
            self.leftClick = False
    
    def mouseMoveEvent(self, event):
        #This is to be able to move the window around without a frame
        if self.leftClick == True:
            x=event.globalX()
            y=event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x-x_w, y-y_w)
            
    def mouseReleaseEvent(self, event):                             
        self.leftClick = False 

#########################################################################################################################################################################
### Class for connecting, retrieving and setting data on MySql ##########################################################################################################
#########################################################################################################################################################################
                                
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
    
    def get_tshirt_image_color(self, sku_code):
        gti = mysql_db.mysql_connect(self)
        gti.execute("""
                        SELECT ic.inventories_image_url, i.inventories_color
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
    
    def get_garment_type_id(self, garmType):
        db = mysql_db.mysql_connect(self)
        db.execute("SELECT inventories_types_id FROM inventories_types WHERE inventories_types_name = '"+ garmType +"'")
        ds = db.fetchone()
        return ds[0]

#########################################################################################################################################################################
### Class for connecting, retrieving and setting data on SQL Server #####################################################################################################
#########################################################################################################################################################################

class mssql_db():
    def mssql_connect(self, db):
        try:
            mssql_db.conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SQLSERVER; DATABASE='+db+'; Trusted_Connection=yes')
            mssql_db.db = mssql_db.conn.cursor()
        except BaseException as e:
            QMessageBox.critical(self, 'Database Error', "Cannot connect to the MS SQL Server: \n" + str(e), QMessageBox.Ok)
        return mssql_db.db        
        
    def getStates(self):
        db = mssql_db.mssql_connect(self, "ProblemSheets")
        db.execute("SELECT stateAbbr FROM dbo.tblState")
        ds = db.fetchall()
        states = []
        for i in ds:
            states.append(i[0])
        return states
                          

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
