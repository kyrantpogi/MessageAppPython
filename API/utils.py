import json
import random
import string
import datetime
import hashlib

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CLIENT_error:
    SINGUP_REQUIREMENT_NOT_FULFILLED = """{"error":"SIGNUP UNSATISFIED <u,p,cp>"}"""
    PASSWORDS_DO_NOT_MATCH = """{"error": "PASSWORD & CONFIRMPASSWORD IS NOT THE SAME"}"""
    USERNAME_ALREADY_EXIST = """{"error": "USERNAME ALREADY EXIST"}"""
    INVALID_LOGIN = """{"error": "INVALID LOGIN"}"""
    WRONG_PASSWORD = """{"error": "WRONG PASSWORD"}"""
    UNSATISFIED_LOGIN = """{"error": "UNSATISFIED LOGIN"}"""
    CANNOT_CREATE_ROOM = """{"error": "CANNOT CREATE ROOM"}"""
    WRONG_MESSAGE_OBJ = """{"error": "WRONG MESSAGE OBJECT"}"""
    INVALID_ROOM = """{"error": "INVALID ROOM"}"""

class Utils:
    def makeUuid(self,size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def makeRoomName(self,size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    #STRING TO PYTHON DICT
    def JSON_loads(self,string="{}"):
        return json.loads(string)
    
    #FALCON WILL ONLY RESPOND AS STRING
    def JSON_dumps(self, dct):
        return json.dumps(dct)

    def getDateToday(self):
        return datetime.datetime.today().strftime("%Y-%m-%d")

    def getDateAndTime(self):
        return datetime.datetime.today().strftime('%Y-%m-%d-%H:%M %p')

    #used to encrypt password
    def hash_pass(self,x):
        sha_signature = hashlib.sha256(x.encode()).hexdigest()
        return sha_signature


