import redis
import threading

class Listener(threading.Thread):
    def __init__(self, r, channels, jukebox):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
        self.jukebox = jukebox

    def work(self, item):
        if item['data'] == "pause":
            self.jukebox.pause()
        elif item['data'] == "play":
            self.jukebox.play()
        print item['channel'], ":", item['data']

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsub"
                break
            else:
                self.work(item)

if __name__ == "__main__":
    r = redis.Redis()
    client = Listener(r, ['test'])
    client.start()

    r.publish('test', 'this will reach the listener')
    r.publish('fail', 'this will not')

    #r.publish('test', 'KILL')
