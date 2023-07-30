"""
Python  API for the playlist service.
"""

# Standard library modules

# Installed packages
import requests


class Playlist():
    """Python API for the music service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s3:30003/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, playlist_name, music_id_list):
        """
        create new playlist by user id and play list name
        """
        payload = {'playlist_name': playlist_name,
                   'music_id_list': music_id_list}
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['playlist_id']

    def read(self, playlist_id):
        r = requests.get(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
            )
        # check status code is 200
        if r.status_code != 200:
            return r.status_code, None, None
        items = r.json()['Items']
        # check whether this id has data
        if len(items) == 0:
            return 404, None, None
        else:
            item = items[0]
            # [i['music_id'] for i in item['music_list']]
            # return r.status_code, item['playlist_name'], item["music_id_list"], item['music_list']
            return r.status_code, item['playlist_name'], item['music_id_list']

    def delete(self, playlist_id):
        requests.delete(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
        )

    def update_playlist_name(self, p_id, new_playlist_name):
        """_summary_

        Args:
            p_id (string): uuid of playlist
            new_playlist_name (string): the new name of the playlist

        Returns:
            int: status code
        """
        r = requests.put(
            self._url + 'playlist-name/' + p_id,
            json={'playlist_name': new_playlist_name},
            headers={'Authorization': self._auth}
        )
        return r.status_code

# not sure code is right:
    def add_song_to_list(self, music_id, playlist_id):
        r = requests.put(
            self._url+'add_song',
            json={
                'playlist_id': playlist_id,
                'music_id': music_id
            },
            headers={'Authorization': self._auth}
        )
        return r.status_code
    def remove_song_from_list(self, music_id, playlist_id):
        r = requests.put(
            self._url+'remove_song',
            json={
                'playlist_id': playlist_id,
                'music_id': music_id
            },
            headers={'Authorization': self._auth}
        )
        return r.status_code