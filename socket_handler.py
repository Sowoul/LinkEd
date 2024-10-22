from flask_socketio import SocketIO

socket = SocketIO(async_mode='eventlet')

@socket.on('connect')
def connected():
    print('connected')
