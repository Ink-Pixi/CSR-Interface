from PyQt5.QtWidgets import QMessageBox
import mysql.connector
import pyodbc

class mysql_db():
    def mysql_connect(self):
        try:
            mysql_db.conn = mysql.connector.connect(user = 'AI_APP', password = 'rowsby01', host = 'wampserver', database = 'inkpixi', raise_on_warnings = True) 
            mysql_db.db = mysql_db.conn.cursor()
        except BaseException as e:
            QMessageBox.critcal(self, 'Database Error', "Can not connect to the MySQL database: \n" + str(e), QMessageBox.Ok)
        
        return mysql_db.db
    
    def saleButtons(self):
        sb = mysql_db.mysql_connect(self)
        sb.execute("""SELECT  ic.inventories_name, ic.inventories_lines_sku, ic.inventories_image_url 
                     FROM inventories_cache ic 
                     LEFT JOIN inventories inv on inv.inventories_id = ic.inventories_id WHERE ic.on_sale = 1 GROUP BY ic.inventories_lines_sku""")
        return sb.fetchall()
    
    
    def designInfo(self, sku_code):
        di = mysql_db.mysql_connect(self)
        di.execute("""
        SELECT ic.inventories_id,ic.inventories_name,ic.inventories_price, ic. inventories_lines_sku, i.inventories_code,i.inventories_name,i.inventories_color, 
               it.inventories_types_name, it.inventories_types_id
        FROM inventories_cache ic 
        LEFT JOIN inventories i on ic.inventories_id = i.inventories_id
        LEFT JOIN inventories_types it on ic.join_inventories_types_id = it.inventories_types_id
        WHERE ic.inventories_lines_sku = '""" + sku_code + """'
        ORDER BY it.inventories_types_id, i.inventories_name
        """)
        return di.fetchall()



    def garmentInfo(self, sku_code, garment_type):
        gi = mysql_db.mysql_connect(self)
        gi.execute("""
        SELECT inventories_code,ia.inventories_accessories_details, io.inventories_options_name 
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

    

class mssql_db():
    def mssql_connect(self):
        try:
            mssql_db.conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SQLSERVER; DATABASE=ImportExport; UID=ReportCreator; PWD=rowsby01;')
            mssql_db.db = mssql_db.conn.cursor()
        except BaseException as e:
            QMessageBox.critical(self, 'Database Error', "Cannon connect to the MS SQL Server: \n" + str(e), QMessageBox.Ok)
        
        return mssql_db.db
    
    
    
