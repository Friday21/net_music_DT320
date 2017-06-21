import requests
import os

print('请输入列表ID ')
PLAY_LIST_ID = input()
print('列表ID是 ',PLAY_LIST_ID)
print('正在解析中......')
PLAY_LIST_JSON = requests.get('https://api.imjad.cn/cloudmusic/?type=playlist&id=%s' % PLAY_LIST_ID).json()

#获取歌曲名字
song_name = []
def get_song_name():
    for i in range(0,len(PLAY_LIST_JSON['privileges'])):
        song_name.append(str(PLAY_LIST_JSON['playlist']['tracks'][i]['name']))
    return song_name

#获取歌曲ID
song_id = []
def get_song_id():
    for i in range(0,len(PLAY_LIST_JSON['privileges'])):
        song_id.append(str(PLAY_LIST_JSON['privileges'][i]['id']))
    return song_id

# 获取歌曲列表的URL
songs_url = []
def get_songs_url():
    for id in song_id:
        songs_url.append('https://api.imjad.cn/cloudmusic/?type=song&id=%s&br=320000' % id)
    return songs_url

#获取下载地址
download_urls = []
def get_download_urls():
    for song_url in songs_url:
        url = requests.get(song_url).json()['data'][0]['url']
        download_urls.append(url)
    return download_urls

#生成字典
download_dicts = {}
def combine():
    for i in range(len(song_name)):
        download_dicts[song_name[i]] = download_urls[i]
    return download_dicts

#下载
def download():
    pwd = os.path.abspath('.')
    directory = pwd+'/'+'music'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for key in download_dicts:
        if download_dicts[key] == None:
            print('这首%s有版权问题' % key)
            continue
        else:
            r = requests.get(download_dicts[key])
            print('开始下载%s到当前的文件夹' % key)
            with open(directory+'/'+'%s.mp3' % key, 'wb') as f:
                f.write(r.content)

if __name__ == '__main__':
    try:
        get_song_id()
        get_songs_url()
        get_song_name()
    except Exception as e:
        print('列表ID是否输对了啊？')
    get_download_urls()
    combine()
    download()
