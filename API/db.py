import mysql.connector
from datetime import datetime as dt

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
    
    def addRoom(self,room_name,owner,shared):
        sql = "INSERT INTO room_info (room_name, owner, shared) VALUES (%s,%s,%s)"
        val = (room_name,owner,shared)
        self.cursor.execute(sql,val)
        self.mydb.commit()
    
    def getRooms(self,owner):
        sql = f"SELECT * FROM room_info WHERE owner='{owner}' UNION SELECT * FROM room_info WHERE shared='{owner}'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class MessageDb:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="tom",
            password="Redhat@123456",
            database="messages"
        )

        self.cursor = self.mydb.cursor(dictionary=True)

    def createTableRoom(self,room_name):
        sql = f"CREATE TABLE {room_name} (id INT NOT NULL AUTO_INCREMENT, message TEXT, sender VARCHAR(255), reciever VARCHAR(255), date_time DATETIME, PRIMARY KEY (id))"
        self.cursor.execute(sql)
        self.mydb.commit()

    def insertMessage(self,x):
        timestamp=(dt.now()).strftime('%Y-%m-%d %I:%M:%S')
        sql = f"""INSERT INTO {x["room_name"]} (message, sender, reciever, date_time) VALUES (%s, %s, %s, %s)"""
        val = (x["message"], x["sender"], x["receiver"],timestamp)
        print(sql,val)
        self.cursor.execute(sql,val)
        self.mydb.commit()

    def getMessages(self,room):
        sql = f"SELECT * FROM {room} ORDER BY id DESC LIMIT 20"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def lastMessage(self,room):
        sql = f"SELECT * FROM {room} ORDER BY id DESC LIMIT 1"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def scrollLoadMessage(self,room,x):
        sql = f"SELECT * FROM {room} ORDER BY id DESC LIMIT {x},20"
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
