from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('playback')
def handle_message(playback):
    print(playback)

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)