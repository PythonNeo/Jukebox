import spotify
import threading

from jukebox_manager import JukeboxManager
from webserver import Server
from credentials import *

logged_in_event = threading.Event()

def connection_state_listener(session):
	if session.connection.state is spotify.ConnectionState.LOGGED_IN:
		logged_in_event.set()

session = spotify.Session()
loop = spotify.EventLoop(session)
loop.start()

session.on(
	spotify.SessionEvent.CONNECTION_STATE_UPDATED, 
	connection_state_listener)

print "Logging in..."

session.login( username, passwd)

logged_in_event.wait()

if session.connection.state == 1:
	print "Logged in!"

jukebox = JukeboxManager(session)

server = Server(jukebox)
server.start()

jukebox.set_playlist( playlist_uri)
jukebox.set_queue( queue_uri )
jukebox.set_server(server)

jukebox.list_tracks()

jukebox.run()
