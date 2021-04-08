import json, falcon
from utils import *
from db import *


class SignUp(Utils, object):
    def on_get(self,req,res):
        res.body = "SINGUP! to http://192.168.0.158:81/signup"

    #GET DATA FROM CLIENT
    def on_post(self,req,res):
        data = super().JSON_loads(req.stream.read())
        db = Db()

        #IF REQUIREMENTS IS FULFILLED
        try:
            uuid = super().makeUuid(10)
            required_fields = {
                "username": data["username"],
                "password": super().hash_pass(data["password"]),
                "confirmpassword": super().hash_pass(data["confirmpassword"]),
                "id": uuid
            }
            if (required_fields["password"] == required_fields["confirmpassword"]):
                check = db.check_if_user_exist(required_fields["username"])
                if (len(check) > 0):
                    res.body = CLIENT_error.USERNAME_ALREADY_EXIST
                else:
                    db.addUser(required_fields["id"],required_fields["username"],required_fields["password"],str(super().getDateToday()))
                    res.body = super().JSON_dumps(required_fields)
            else:
                res.body = CLIENT_error.PASSWORDS_DO_NOT_MATCH
            
        
        except:
            res.body = CLIENT_error.SINGUP_REQUIREMENT_NOT_FULFILLED


class Login(Utils,object):
    def on_post(self,req,res):
        data = super().JSON_loads(req.stream.read())
        db = Db()

        try:
            required_fields = {
                "username": data["username"],
                "password": super().hash_pass(data["password"])
            }

            user = db.check_if_user_exist(required_fields["username"])

            if (len(user) > 0):
                    if (user[0]["password"] == required_fields["password"]):
                        # add to log
                        crt = str(super().getDateAndTime())
                        db.login(user[0]["username"],crt)
                        res.body = """{"login": "true"}"""
                    else:
                        res.body = CLIENT_error.WRONG_PASSWORD
            else:
                res.body = CLIENT_error.INVALID_LOGIN
        
        except:
            res.body = CLIENT_error.UNSATISFIED_LOGIN

class ComposeMessage(Utils,object):
    def on_post(self,req,res):
        data = super().JSON_loads(req.stream.read())
        db=Db()
        mdb = MessageDb()
        try:
            room_name = super().makeRoomName(15)
            required_fields = {
                "owner": data["owner"],
                "shared": data["shared"],
                "room_name": room_name
            }
            db.addRoom(room_name,required_fields["owner"],required_fields["shared"])
            mdb.createTableRoom(required_fields["room_name"])
            
            res.body = "Success"
        except:
            print("ERROR!")
            res.body = CLIENT_error.CANNOT_CREATE_ROOM

class getRooms(Utils, object):
    def on_get(self,req,res):
        owner = req.params["owner"]
        db = Db()

        data = db.getRooms(req.params["owner"])
        res.body = super().JSON_dumps(data)

class sendMessage(Utils, object):
    def on_post(self,req,res):
        data = super().JSON_loads(req.stream.read())
        mdb = MessageDb()
        print(data)
        try:
            required_fields = {
                "room_name": data["room_name"],
                "message": data["message"],
                "sender": data["sender"],
                "receiver": data["receiver"]
            }
            mdb.insertMessage(required_fields)
            res.body = "Succesful"
        except:
            res.body = CLIENT_error.WRONG_MESSAGE_OBJ
            print(CLIENT_error.WRONG_MESSAGE_OBJ)

class getMessages(Utils, object):
    def on_get(self,req,res):
        room = req.params["room"]
        mdb = MessageDb()

        try:
            messages = mdb.getMessages(room)
            for data in messages:
                data["date_time"] = str(data["date_time"])
            res.body = super().JSON_dumps(messages)
        except:
            res.body = CLIENT_error.INVALID_ROOM

class lastMessage(Utils, object):
    def on_get(self,req,res):
        room = req.params["room"]
        mdb = MessageDb()

        try:
            messages = mdb.lastMessage(room)
            for data in messages:
                data["date_time"] = str(data["date_time"])
            res.body = super().JSON_dumps(messages)
        except:
            res.body = CLIENT_error.INVALID_ROOM

class scrollLoadMessage(Utils,object):
    def on_get(self,req,res):
        room = req.params["room"]
        multiplyValue = req.params["x"]
        mdb = MessageDb()
        x=int(multiplyValue)*20

        messages = mdb.scrollLoadMessage(room,x)
        print("scrollLoadMessage")
        for data in messages:
            data["date_time"] = str(data["date_time"])
        res.body = super().JSON_dumps(messages)



#test url
class Test(Utils,object):
    def on_get(self,req,res):
        print(req.params["msg"])
        res.body = req.params["msg"]

    def on_post(self,req,res):
        data = super().JSON_loads(req.stream.read())
        print(req.method)
        print(json.dumps(data))
        
           