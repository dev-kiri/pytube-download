from requests import get
from urllib.parse import urlsplit, parse_qsl
from json import loads

def downloadYT(videoId, file_name):
    try:
        response = get('https://youtube.com/get_video_info', params = {'video_id': videoId}).text
        rawjson = dict(parse_qsl(urlsplit(response).path))
        player_response = loads(rawjson['player_response'])
        formats = player_response['streamingData']['formats'][-1]

        if 'url' in formats.keys():
            url = formats['url']
        else:
            signatureCipher = formats['signatureCipher']
            url = dict(parse_qsl(urlsplit(signatureCipher).path))['url']

        response = get(url)

        if not response.status_code == 200:
            raise Exception('Failed to download YouTube Video...')

        with open(file_name, 'wb') as file:
            response = get(url)
            file.write(response.content)

        return f'download success\nCheck {file_name}'

    except Exception as e:
        return e
