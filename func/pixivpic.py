import requests
import random
_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4314.150 Safari/537.36'
}
_URL_VIS = 'https://pixivel.moe/'
_DATA = {
    'type': 'search',
    'word': '明日方舟',
    'page': 0,
    'mode': 'partial_match_for_tags'
}


class Pixivpic:
    def __init__(self):
        self.session = requests.session()
        ret = self.session.get(_URL_VIS, headers=_HEADERS)
        print('Pixivpic 初始化结果:%d' % ret.status_code)
        pass

    def __del__(self):
        self.session.close()

        pass

    def query(self, kw):
        _DATA['word'] = kw
        ret = self.session.get(
            'https://api.pixivel.moe/pixiv',
            headers=_HEADERS,
            params=_DATA)
        data = ret.json()
        if 'illusts' not in data:
            return ''
        data = data['illusts']
        if len(data) == 0:
            return ''
        ch = random.randint(0, len(data) - 1)
        id = data[ch]['id']
        thpic = data[ch]['image_urls']['large']
        url = 'https://p1.pximg.pixivel.moe/' + thpic[thpic.find('c/'):]
        return url
        pass
    pass


if __name__ == '__main__':
    pix = Pixivpic()
    print(pix.query('明日方舟'))
    pass
