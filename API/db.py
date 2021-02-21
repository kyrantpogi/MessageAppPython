import mysql.connector
from utils import bcolors

class Db:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="tom",
            password="Redhat@123456",
            database="polling_app"
        )

        self.cursor = self.mydb.cursor(dictionary=True)

        
    def addUser(self,id,u,p,D):
        sql = "INSERT INTO users (uuid,username,password,date_created) VALUES (%s,%s,%s,%s)"
        val = (id,u,p,D)
        self.cursor.execute(sql,val)
        self.mydb.commit()

    def login(self,username,d_t):
        sql = "INSERT INTO logged (username, date_time) VALUES (%s,%s)"
        val = (username,d_t)
        self.cursor.execute(sql,val)
        self.mydb.commit()

    def check_if_user_exist(self,username):
        sql = f"SELECT * FROM users WHERE username='{username}'"
        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()
        return myresult



