import falcon
from views import *


app = application = falcon.API()
app.req_options.auto_parse_form_urlencoded = True

#routes
app.add_route("/signup", SignUp())
app.add_route("/login", Login())