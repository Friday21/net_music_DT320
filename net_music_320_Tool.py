import requests
print('请输入列表ID ')
PLAY_LIST_ID = input()
print('列表ID是 ',PLAY_LIST_ID)
print('正在解析API')
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

#下载歌曲
def download():
    try:
        for song_url in songs_url:
            for name in song_name:
                url = requests.get(song_url).json()['data'][0]['url']
                r = requests.get(url)
                print('开始下载歌曲到当前的文件夹')
                with open('%s.mp3' % name, 'wb') as f:
                    f.write(r.content)
                del song_name[0]
                break
        print('下载结束，看看去吧')
    except Exception as e:
        print('网易云版权问题，链接挂了')
    finally:
        download()
if __name__ == '__main__':
    try:
        get_song_id()
        get_songs_url()
        get_song_name()
    except Exception as e:
        print('列表ID是否输对了啊？')
    download()
