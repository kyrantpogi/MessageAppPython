import falcon
import requests
from utils import *
from views import *


class HandleCORS(object):
    def process_request(self, req, res):
        res.set_header('Access-Control-Allow-Origin', '*')
        res.set_header('Access-Control-Allow-Methods', '*')
        res.set_header('Access-Control-Allow-Headers', '*')
        res.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        # if req.method == 'OPTIONS':
        #    raise HTTPStatus(falcon.HTTP_200, body='\n')

app = application = falcon.API(middleware=[HandleCORS()])
app.req_options.auto_parse_form_urlencoded = True


#routes
app.add_route("/signup", SignUp())
app.add_route("/login", Login())
app.add_route("/compose-message", ComposeMessage())
app.add_route("/get-rooms", getRooms())
app.add_route("/send-message", sendMessage())
app.add_route("/get-messages", getMessages())
app.add_route("/last-message", lastMessage())
app.add_route("/scroll-load-message", scrollLoadMessage())
app.add_route("/test", Test())

