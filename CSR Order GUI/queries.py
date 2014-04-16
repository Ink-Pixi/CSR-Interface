import mysql.connector
import pyodbc

class mysql_db():
    def mysql_connect(self):
        mysql_db.conn = mysql.connector.connect(user = 'AI_APP', password = 'rowsby01', host = 'wampserver', database = 'xaotees-inkpixi', raise_on_warnings = True) 
        mysql_db.db = mysql_db.conn.cursor()
        return mysql_db.db
    
    def saleButtons(self):
        sb = mysql_db.mysql_connect(self)
        sb.execute("""SELECT  ic.inventories_id,ic.inventories_name,ic.inventories_lines_sku, inv.inventories_code,ic.inventories_price, inv.inventories_color, inv.inventories_name as garment_name,ic.inventories_image_url 
                     FROM inventories_cache ic 
                     LEFT JOIN inventories inv on inv.inventories_id = ic.inventories_id WHERE ic.on_sale = 1 GROUP BY ic.inventories_lines_sku""")
        return sb.fetchall()
    
    
    def designInfo(self, sku_code):
        di = mysql_db.mysql_connect(self)
        di.execute("""SELECT ic.inventories_id,ic.inventories_name,ic.inventories_lines_sku, inv.inventories_code,ic.inventories_price, inv.inventories_color, inv.inventories_name as garment_name,ic.inventories_image_url, concat('//wampserver/data/store/',ic.inventories_lines_sku,'-collage-box.jpg')
        FROM inventories_cache ic
        LEFT JOIN inventories inv on inv.inventories_id = ic.inventories_id
        WHERE ic.inventories_lines_sku = '""" + sku_code + """'
        GROUP BY ic.inventories_lines_sku
        """)
        return di.fetchall()
    
    

class mssql_db():
    def mssql_connect(self):
        mssql_db.conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SQLSERVER; DATABASE=ImportExport; UID=ReportCreator; PWD=rowsby01;')
        mssql_db.db = mssql_db.conn.cursor()
        return mssql_db.db
    
    
    