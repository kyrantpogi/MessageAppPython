import json, falcon
from utils import *
from db import Db


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
        