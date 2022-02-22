# import mysql.connector
# import os
# from dotenv import load_dotenv, find_dotenv
#
# load_dotenv(find_dotenv())
#
#
# class trial1():
#     mydb= mysql.connector.connect(
#         host=os.environ['DB_HOST'],
#         user=os.environ['DB_USER'],
#         passwd=os.environ['DB_PWD'],
#         database=os.environ['DB_NAME']
#     )
#
#     mycrr=mydb.cursor()
#     # mycrr.execute("CREATE TABLE StoreData (name VARCHAR(50), date DATE )")
#
#     # dt= mycrr.execute("SELECT CURRENT_USER()")
#     # print("ye lo",dt)
#     # tm= mycrr.execute("SELECT CURDATE()")
#     sql= "INSERT INTO StoreData (name, date) VALUES (SESSION_USER(), NOW())"
#     # val= dt
#     mycrr.execute(sql)
#     mydb.commit()
