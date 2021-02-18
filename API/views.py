import json, falcon
from utils import Utils, CLIENT_error

class SignUp(Utils, object):
    def on_get(self,req,res):
        res.body = "SINGUP! to http://192.168.0.158:81/signup"

    #GET DATA FROM CLIENT
    def on_post(self,req,res):
        data = super().JSON_loads(req.stream.read())

        #IF REQUIREMENTS IS FULFILLED
        try:
            uuid = super().makeUuid(10)
            required_fields = {
                "username": data["username"],
                "password": data["password"],
                "confirmpassword": data["confirmpassword"],
                "id": uuid
            }
            if (required_fields["password"] == required_fields["confirmpassword"]):
                res.body = super().JSON_dumps(required_fields)
            else:
                res.body = CLIENT_error.PASSWORDS_DO_NOT_MATCH
            
        
        except:
            res.body = CLIENT_error.SINGUP_REQUIREMENT_NOT_FULFILLED
