import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20201013', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

music_list = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for music in music_list:
    music_title = music.select_one('.info a').text.strip()
    music_rank = music.select_one('.number').text[0:2].strip()
    music_singer = music.select_one('a.artist.ellipsis').text
    music_id = music.select_one('.info a')['onclick'].split("'")[1]

    music = db.music_db.find_one({'music_id': music_id})

    if music is None:
        doc = {
            'music_rank': music_rank,
            'music_title': music_title,
            'music_singer': music_singer,
            'music_id': music_id
        }

        db.music_db.insert_one(doc)

        print('insert')

