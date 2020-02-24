import json
from bs4 import BeautifulSoup
from urllib import request

# 一年前写的代码结果还能用...
singer_url_prefix = "https://music.163.com/artist?id="
eason_url = "https://music.163.com/artist?id=2116"
avicii_url = "https://music.163.com/artist?id=45236"
lizhi_url = "https://music.163.com/artist?id=3681"


def find_hotsong_ids(url):
    ids = []
    headers = {}
    headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    headers["Host"] = "music.163.com"
    headers["Referer"] = "https://music.163.com/"
    headers["Upgrade-Insecure-Requests"] = "1"

    target_url = url
    req = request.Request(target_url, headers=headers)
    res = request.urlopen(req)
    html_soup = BeautifulSoup(res.read().decode(
        "utf-8"), features="html.parser")
    hotsong_list = BeautifulSoup(
        str(html_soup.find(id='hotsong-list')), features='lxml')
    for each_li in hotsong_list.find('ul'):
        link = each_li.a.attrs["href"]
        id = link[9:]
        ids.append(id)
    return ids


def cheek_outer_link(outer_play_link):
    result = False
    out_headers = {}
    out_headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    out_req = request.Request(outer_play_link, headers=out_headers)
    res_code = request.urlopen(out_req).geturl()[-3:]
    if res_code != "404":
        result = True
    return result


# 输入歌手的id就可以了
if __name__ == '__main__':
    user_id = input("singer id:").strip()
    singer_url_prefix += user_id
    for each_id in find_hotsong_ids(singer_url_prefix):
        song_id = each_id
        outer_play_link = "http://music.163.com/song/media/outer/url?id={}.mp3".format(
            song_id)
        outer_play_link = outer_play_link if cheek_outer_link(
            outer_play_link) else "-"
        headers = {}
        headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        headers["Host"] = "music.163.com"
        headers["Origin"] = "https://music.163.com"
        headers["Referer"] = "https://music.163.com/song?".format(song_id)
        song_info_url = "http://music.163.com/api/song/detail/?id={}&ids=[{}]&csrf_token=".format(
            song_id, song_id)

        req = request.Request(song_info_url, headers=headers)
        res = request.urlopen(req)

        res_json = res.read().decode("utf-8")
        song_info_dic = json.loads(res_json)

        for song in song_info_dic["songs"]:
            name = song["name"]
            artist = song["artists"][0]["name"]
            album = song["album"]["name"]
            frequency = song["mMusic"]["bitrate"]
            duration = song["mMusic"]["playTime"]
            link = outer_play_link
            score = 0
            song_image = song["album"]["picUrl"]
            t = []
            t.append(name)
            t.append(artist)
            t.append(album)
            t.append(frequency)
            t.append(duration)
            t.append(link)
            t.append(score)
            t.append(song_image)
            print("%s: %s" % (name, link))
            # s = Song(name, artist, album, frequency, duration, link, score, song_image)
            # mysql_util.insert(s)
