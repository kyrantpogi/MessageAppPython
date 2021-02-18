import falcon
from views import SignUp


app = application = falcon.API()
app.req_options.auto_parse_form_urlencoded = True

#routes
app.add_route("/signup", SignUp())