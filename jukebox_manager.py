import spotify
import threading

class JukeboxManager():

    def __init__(self, session):
        self.session = session
        spotify.AlsaSink(session)
        self.end_of_track = threading.Event()
        self.current_song = -1
        self.current_song_name = ""

        self.session.on(spotify.SessionEvent.END_OF_TRACK, self.on_end_of_track)

    def set_playlist(self, playlist):
        self.playlist = self.session.get_playlist(playlist)
        self.playlist.load()
        self.playlist.on(spotify.PlaylistEvent.TRACKS_ADDED, self.track_added_to_playlist)
        print('Playlist {} blev hentet med {} sange'.format(self.playlist.name, len(self.playlist.tracks)))
              
    def set_queue(self, queue):
        self.queue = self.session.get_playlist(queue)
        self.queue.load()
        self.queue.on(spotify.PlaylistEvent.TRACKS_ADDED, self.track_added_to_queue)

    def set_server(self, server):
        self.server = server

    def list_tracks(self):
        for track in self.playlist.tracks:
            print self.track_string(track)
            
    def track_string(self, track):
        track.load()
        artist = track.artists[0].load()
        trackName = track.name.encode('ascii', 'ignore')
        artistName = artist.name.encode('ascii', 'ignore')
        return '{} - {}'.format(artistName, trackName)

    def track_added_to_playlist(self, playlist, tracks, index):
        print "Playlist has been updated!"

    def track_added_to_queue(self, playlist, tracks, index):
        print "Song added to queue"

    def run(self):
        self.play_next_song()

        try:
                while True:
                        if not self.playing():
                                self.play_next_song()
        except KeyboardInterrupt:
                pass

    def play(self):
        self.session.player.play()

    def pause(self):
        self.session.player.pause()
              
    def playing(self):
        if self.end_of_track.wait(0.1):
              return False
        else:
            return True
                      
    def play_song(self, play_from_queue = False):
        if play_from_queue:
            track = self.queue.tracks[0].load()
        else:
            track = self.playlist.tracks[self.current_song].load()

        self.session.player.load(track)
        self.session.player.play()
        self.current_song_name = self.track_string(track)
        print('Now playing: {}'.format(self.track_string(track)))
        self.server.new_song(self.current_song_name)

    def play_next_song(self):
        self.end_of_track.clear()
        if (self.queue and len(self.queue.tracks) > 0):
            self.play_song(True)
            self.queue.remove_tracks(0)
        else:
			if self.current_song == len(self.playlist.tracks):
				self.current_song = 0
			else:
				self.current_song += 1

			self.play_song()
              
    def on_end_of_track(self, q):
        self.end_of_track.set()

    def add_to_queue(self, song):
		for track in self.queue.tracks:
			if track == song:
				return False
        
		track = self.session.get_track(song)
        	self.queue.add_tracks(track)
		return True
       
