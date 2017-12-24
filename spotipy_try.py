import spotipy
import sys
import pprint
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='ccae2e7a3a0f48088d24563289eb71d0', client_secret='0204fbff5f2c438a816b7c01ede9d9ce')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 1:
    urn = sys.argv[1]
else:
    urn = 'spotify:track:0Svkvt5I79wficMFgaqEQJ'

track = sp.track(urn)
pprint.pprint(track)