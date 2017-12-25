"""
This is a scraper for Spotify data.
It receives a query to search and a starter page of search in case of crash.
It creates a csv on a data directory on the same page as the script.

Usage:
python spotify_scraper.py [QUERY] [RANGE].
Both arguments are optional.
Author: Alex Ingberg
"""



import spotipy
import time
import json
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import os.path
import sys


def main(query, start_range):
    # Establish a session and instantiate it
    client_credentials_manager = SpotifyClientCredentials(client_id='ccae2e7a3a0f48088d24563289eb71d0',
                                                          client_secret='0204fbff5f2c438a816b7c01ede9d9ce')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    filename = 'data/' + query + '_db.csv'
    start = time.time()

    # Extract features from API
    with open(filename, 'a+', encoding='utf-8') as f:

        for i in range(start_range, 1000):
            print('Getting %d/1000 50s...' % i)
            an_offset = 50 * i
            results = sp.search(q='genre:' + query, type='track', limit=50, offset=an_offset)  # if limit > 50, crashes

            if an_offset > results['tracks']['total']:  # if theres less search result that the loop
                break
            tids = np.array([])
            names = np.array([])
            artists = np.array([])
            for t in results['tracks']['items']:
                names = np.append(names, t['name'])
                artists = np.append(artists, t['artists'][0]['name'])
                # print(json.dumps(t, sort_keys=True, indent=4, separators=(',', ': ')))
                tids = np.append(tids, t['uri'])

            # construct a DF with the results
            features = pd.DataFrame(sp.audio_features(tids))
            features['name'] = names
            features['artist'] = artists
            features['genre'] = query

            # puts our label columns first
            cols = features.columns.tolist()
            cols = cols[-3:] + cols[:-3]
            features = features[cols]
            # save
            use_header = i == 0
            features.to_csv(f, sep=';', header=use_header, index=False, encoding='utf-8')
            print('Saved %d/1000 50s...' % i)
            print('File %s is %.02f MB' % (filename, (os.path.getsize(filename) / 1000000)))

    print("\n######!!!!!!!!!#######\n")
    print("FINISHED!")
    print('%s generated. It weighs %.05f MB' % (filename, (os.path.getsize(filename) / 1000000)))

    # time measuring
    seconds = time.time() - start
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    total_time = "%d:%02d:%02d (h:mm:ss)" % (h, m, s)
    print('It took', total_time, 'in total')


if __name__ == '__main__':
    args = sys.argv[1:]
    query = ''
    start_range = 0
    if args:
        for i, arg in enumerate(args):
            if i == 0:
                query = args[0]
            if i == 1:
                start_range = args[1]
    if not query:
        query = 'pop'
    if not start_range:
        start_range = 0

    main(query, start_range)