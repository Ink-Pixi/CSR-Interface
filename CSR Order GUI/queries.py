import mysql.connector


class getQueries():

    def get_onSale(self):
        conn = mysql.connector.connect(user = 'AI_APP', password = 'rowsby01', host = 'wampserver', database = 'xaotees-inkpixi', raise_on_warnings = True) 
        db = conn.cursor()  
        # Get all "on sale" items
        db.execute ("""SELECT  ic.inventories_id,ic.inventories_name,ic.inventories_lines_sku, inv.inventories_code,ic.inventories_price, inv.inventories_color, inv.inventories_name as garment_name,ic.inventories_image_url 
        FROM inventories_cache ic 
        LEFT JOIN inventories inv on inv.inventories_id = ic.inventories_id WHERE ic.on_sale = 1 GROUP BY ic.inventories_lines_sku
        """)
        # fetch all of the rows from the query
        on_sale_designs = db.fetchall()    
        db.close()
        return on_sale_designs   
    
    
    def get_Search(self, sku_code):
        conn = mysql.connector.connect(user = 'AI_APP', password = 'rowsby01', host = 'wampserver', database = 'xaotees-inkpixi', raise_on_warnings = True) 
        db = conn.cursor()
        
        # Get all "on sale" items
        db.execute ("""SELECT ic.inventories_id,ic.inventories_name,ic.inventories_lines_sku, inv.inventories_code,ic.inventories_price, inv.inventories_color, inv.inventories_name as garment_name,ic.inventories_image_url
        FROM inventories_cache ic
        LEFT JOIN inventories inv on inv.inventories_id = ic.inventories_id
        WHERE ic.inventories_lines_sku = """ + sku_code + """
        GROUP BY ic.inventories_lines_sku
        """)
        # fetch all of the rows from the query
        search_result = db.fetchall()    
        db.close()
        return search_result 