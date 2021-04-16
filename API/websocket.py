import socketio
from db import *
# from waitress import serve

sio = socketio.Server(cors_allowed_origins = "*")
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print(sid,'connected')
    sio.emit("connect", {"m":sid}, room=sid)

#custom event
@sio.on("message")
def message(sid,data):
    db = MessageDb()
    time = db.insertMessage(data)
    final =  {**data, **{"date_time":time}}
    print(final)
    sio.emit("message",final)

@sio.event
def disconnect(sid):
    print(sid,'disconnected')

# if __name__ == "__main__":
#     serve(app,host='0.0.0.0', port=5000)