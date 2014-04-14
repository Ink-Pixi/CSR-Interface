#Connect to Wampserver db xaotees-inkpixi
import mysql.connector

class ConnectDB():
    def conn(self): 
        config = {
        'user': 'AI_APP',
        'password': 'rowsby01',
        'host': 'wampserver',
        'database': 'xaotees-inkpixi',
        'raise_on_warnings': True
        }           
        cnx = mysql.connector.connect(**config)
        # prepare a cursor object using cursor() method
        c1 = cnx.cursor()
        
        return c1
        

        
        

#connect() 
#for i in on_sale_designs:  
    #print(i[7])