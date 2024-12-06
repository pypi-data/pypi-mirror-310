# coding=utf-8
import requests
from urllib3.exceptions import HTTPError
import platform

import encrypto

_headers = {
    'Host': 'music.163.com',
    'Connection': 'keep-alive',
    'Origin': 'http://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://music.163.com/search/',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

URL_SONG_DETAIL = "http://music.163.com/api/song/detail?ids=[{song_ids}]"
URL_SONG_LYRIC = "http://music.163.com/api/song/lyric?id={song_id}&lv=1&tv=1"
URL_PLAYLIST_DETAIL = "http://music.163.com/weapi/v3/playlist/detail"
URL_ARTIST = "http://music.163.com/api/artist/{artist_id}"
URL_ALBUM = "http://music.163.com/api/album/{album_id}"


def send_request(method, url, json=True, **kwargs):
    """
    Send comment request.
    """
    with requests.Session() as session:
        try:
            response = session.request(
                method=method,
                url=url,
                headers=_headers,
                verify=False,
                **kwargs
            )
            content = response.json() if json else response.content
        except (requests.RequestException, HTTPError) as ex:
            # TODO fix ex
            print(ex)
            content = None
    return content


def request_songs(song_ids, proxies=None):
    str_song_ids = ",".join(map(lambda value: str(value), song_ids))
    url = URL_SONG_DETAIL.format(song_ids=str_song_ids)
    data = send_request(method='POST', url=url, proxies=proxies)
    return {
        song["id"]: song
        for song in data.get("songs", [])
    }


def request_lyric(song_id, proxies=None):
    url = URL_SONG_LYRIC.format(song_id=song_id)
    content = send_request(method='POST', url=url, proxies=proxies)
    return content


def request_playlist(playlist_id, proxies=None):
    url = URL_PLAYLIST_DETAIL
    # data = {'id': playlist_id, 'total': 'true', 'csrf_token': csrf, 'limit': 1000, 'n': 1000, 'offset': 0}
    text = {
        'id': playlist_id,
        'total': 'true',
        'limit': 1000,
        'n': 1000,
        'offest': 0
    }
    cookies = dict(
        os=platform.system()
    )
    data = encrypto.generate_data(text)
    content = send_request(method='POST', url=url, data=data, cookies=cookies, proxies=proxies)
    return content


def request_artist(artist_id, proxies=None):
    url = URL_ARTIST.format(artist_id=artist_id)
    content = send_request(method='GET', url=url, proxies=proxies)
    return content


def request_album(album_id, proxies=None):
    url = URL_ALBUM.format(album_id=album_id)
    content = send_request(method='GET', url=url, proxies=proxies)
    return content
