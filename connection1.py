import mysql.connector

def fun():

    # Establish a database connection to retrieve data from the Test table

    db = mysql.connector.connect(

        host="localhost",

        user="root",

        password="Saadhvi03ss",    #Enter your SQL Workbench password here.

        database="wardrobe_db",

        #auth_plugin="mysql_native_password"
       # auth_plugin="caching_sha2_password"


    )
    return db