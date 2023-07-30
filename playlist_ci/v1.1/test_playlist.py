"""
Test the *_original_artist routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import playlist
import uuid


@pytest.fixture
def mserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


@pytest.fixture
def playlist1(request):
    return ('likes', ["6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea", "c2573193-f333-49e2-abec-182915747756"])

def test_get_playlist(mserv, playlist1):
    trc, p_id = mserv.create(playlist1[0], playlist1[1])
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id)
    assert (trc == 200 
            and playlist_name == playlist1[0]
            and music_id_list == playlist1[1])
    # assert(music_list[0]["Artist"] == "Taylor Swift" 
    #        and music_list[0]["SongTitle"] == "The Last Great American Dynasty"
    #        and music_list[1]["Artist"] == "Backxwash" 
    #        and music_list[1]["SongTitle"] == "Bad Juju")
    mserv.delete(p_id)
    
    
@pytest.fixture
def playlist2(request):
    return ('likes', ["6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea", "c2573193-f333-49e2-abec-182915747756"])

def test_delete_playlist(mserv, playlist2):
    trc, p_id = mserv.create(playlist2[0], playlist2[1])
    assert trc == 200
    mserv.delete(p_id)  
    response = mserv.read(p_id)  
    assert response[0] == 404
    

@pytest.fixture
def playlist3(request):
    return ('likes', ["6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea", "c2573193-f333-49e2-abec-182915747756"])

def test_update_playlist_name(mserv, playlist3):
    trc, p_id = mserv.create(playlist3[0], playlist3[1])
    assert trc == 200
    new_playlist_name = "korean pop"
    trc = mserv.update_playlist_name(p_id, new_playlist_name)  
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id)  
    assert (trc == 200 
            and playlist_name == new_playlist_name
            and music_id_list == playlist3[1])
    mserv.delete(p_id)

# TODO: not very unit-test, refactor so it test one use case only
@pytest.fixture
def playlist4(request):
    return (str(uuid.uuid4()), [str(uuid.uuid4())])

def test_add_song_to_playlist(mserv, playlist4):
    trc, p_id = mserv.create(playlist4[0], playlist4[1])
    m_id = str(uuid.uuid4())
    assert trc == 200
    trc = mserv.add_song_to_list(m_id, p_id)
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id) 
    assert (trc == 200 
        and playlist_name == playlist4[0]
        and music_id_list == playlist4[1]+[m_id])

# TODO: not very unit-test, refactor so it test one use case only
@pytest.fixture
def playlist5(request):
    return (str(uuid.uuid4()), [str(uuid.uuid4())])
def test_remove_song_to_playlist(mserv, playlist5):
    trc, p_id = mserv.create(playlist5[0], playlist5[1])
    m_id = str(uuid.uuid4())
    assert trc == 200
    trc = mserv.add_song_to_list(m_id, p_id)
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id) 
    assert (trc == 200 
        and playlist_name == playlist5[0]
        and music_id_list == playlist5[1]+[m_id])
    trc = mserv.remove_song_from_list(m_id, p_id)
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id)
    assert (trc == 200
        and playlist_name == playlist5[0]
        and music_id_list == playlist5[1])
    
@pytest.fixture
def playlist6(request):
    return ('myPlaylist1', ["0894ddc7-0c84-4f13-a037-ddcaa1134ec8"])

def test_remove_non_exist_song_to_playlist(mserv, playlist6):
    """ testing remove a music id not from playlist

    Args:
        mserv (_type_): playlist server
        playlist6 (_type_): playlist object
    """
    trc, p_id = mserv.create(playlist6[0], playlist6[1])
    assert trc == 200
    m_id = "6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea"
    trc = mserv.remove_song_from_list(m_id, p_id)
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id)
    assert (trc == 200
        and playlist_name == playlist6[0]
        and music_id_list == ["0894ddc7-0c84-4f13-a037-ddcaa1134ec8"])          
    

@pytest.fixture
def playlist7(request):
    return ('myPlaylist2', ["0894ddc7-0c84-4f13-a037-ddcaa1134ec8"])

def test_remove_song_to_playlist_empty(mserv, playlist7):
    trc, p_id = mserv.create(playlist7[0], playlist7[1])
    assert trc == 200
    m_id = "0894ddc7-0c84-4f13-a037-ddcaa1134ec8"
    trc = mserv.remove_song_from_list(m_id, p_id)
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id)
    assert (trc == 200
        and playlist_name == playlist7[0]
        and music_id_list == [])    
    

@pytest.fixture
def playlist8(request):
    return ('myPlaylist3', [])

def test_add_song_to_empty_playlist(mserv, playlist8):
    trc, p_id = mserv.create(playlist8[0], playlist8[1])
    assert trc == 200
    m_id = "0894ddc7-0c84-4f13-a037-ddcaa1134ec8"
    trc = mserv.add_song_to_list(m_id, p_id)
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id)
    assert (trc == 200
        and playlist_name == playlist8[0]
        and music_id_list == ["0894ddc7-0c84-4f13-a037-ddcaa1134ec8"])
    # add again, this time music id will not be added since already in list
    trc = mserv.add_song_to_list(m_id, p_id)
    assert trc == 200
    trc, playlist_name, music_id_list = mserv.read(p_id)
    assert (trc == 200
        and playlist_name == playlist8[0]
        and music_id_list == ["0894ddc7-0c84-4f13-a037-ddcaa1134ec8"])
         
    
    