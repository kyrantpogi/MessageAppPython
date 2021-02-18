import json
import random
import string

class CLIENT_error:
    SINGUP_REQUIREMENT_NOT_FULFILLED = """{"error":"SIGNUP UNSATISFIED <u,p,cp>"}"""
    PASSWORDS_DO_NOT_MATCH = """{"error": "PASSWORD & CONFIRMPASSWORD IS NOT THE SAME"}"""

class Utils:
    def makeUuid(self,size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    #STRING TO PYTHON DICT
    def JSON_loads(self,string="{}"):
        return json.loads(string)
    
    #FALCON WILL ONLY RESPOND AS STRING
    def JSON_dumps(self, dct):
        return json.dumps(dct)
