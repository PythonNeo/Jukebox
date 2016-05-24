import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

class Server(threading.Thread):

    def __init__(self, jukebox):
        threading.Thread.__init__(self)
        self.jukebox = jukebox

    def run(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.socketio = SocketIO(self.app)

        @self.socketio.on('connect')
        def handle_connect():
            emit('newSong', self.jukebox.current_song_name)

        @self.socketio.on('playback')
        def handle_message(playback):
            if playback == "pause":
                self.jukebox.pause()
            elif playback == "play":
                self.jukebox.play()
            elif playback == "next":
                self.jukebox.play_next_song()
                return self.jukebox.current_song_name
            print(playback)

        @self.socketio.on('addToQueue')
        def handle_add_to_queue(song):
        	if self.jukebox.add_to_queue(song):
			return True
		else:
			return False

        @self.app.route("/")
        def index():
            return render_template("queue.html")

        @self.app.route("/playstyring")
        def control():
            return render_template("index.html")

        self.socketio.run(self.app, host='0.0.0.0', port=80)

    def new_song(self, song):
        with self.app.test_request_context('/'):
            self.socketio.send('newSong', song)

if __name__ == '__main__':
    server = Server()
    server.start()
