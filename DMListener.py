from tweepy import Stream
from tweepy import OAuthHandler
import json
from tweepy.streaming import StreamListener

keys = json.load(open('keys.json'))
consumer_key = keys['consumer_key']
consumer_key_secret = keys['consumer_key_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

class DMListener( StreamListener ):

    def on_connect( self ):
        print("Stream Connected")

    def on_disconnect( self, notice ):
        print("Stream Connection Lost:", notice)

    def on_data( self, status ):
        status_json = json.loads(status)
        print(status)
        if 'direct_message' in status_json:
            name = str(status_json['direct_message']['sender']['screen_name'])
            text = str(status_json['direct_message']['text'])
            time = str(status_json['direct_message']['created_at'])
            print '----------------------------------------------------------------'
            print 'Message Received from: ' + name
            print 'Message: ' + text
            print 'Message Received at: ' + time
            print '----------------------------------------------------------------'
            determineResponse(text, name, time)
        return True
    

    def on_error( self, status ):
        print("Error:", status)

class SnapNGoBot:
    def __init__(self):
        self.auth = OAuthHandler(consumer_key, consumer_key_secret)
        self.auth.secure = True
        self.auth.set_access_token(access_token, access_token_secret)

        self.dmlistener = Stream(self.auth, DMListener())
        self.dmlistener.userstream()

def main():
    auth = OAuthHandler(consumer_key, consumer_key_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    dmlistener = Stream(auth, DMListener())
    dmlistener.userstream()

if __name__ == '__main__':
    main()