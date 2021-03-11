import requests
_HEADERS = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    "x-client-data": "CJK2yQEIpLbJAQjEtskBCKmdygEIqKPKAQi5pcoBCLGnygEI4qjKAQjxqcoBCJetygEIza3KAQ=="}
_DATA = {
    "client": "webapp",  # 基于网页访问服务器
    "sl": "auto",  # 源语言,auto表示由谷歌自动识别
    "tl": "vi",  # 翻译的目标语言
    "hl": "zh-CN",  # 界面语言选中文，毕竟URL都是cn后缀了，就不装美国人了
    # dt表示要求服务器返回的数据类型
    "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],
    "otf": "2",
    "ssel": "0",
    "tsel": "0",
    "kc": "1",
    "tk": "",  # 谷歌服务器会核对的token
    "q": ""  # 待翻译的字符串
}
_URL_VIS = 'https://translate.google.cn/'
_URL_TRAN = 'https://translate.google.cn/translate_a/single'

dictLang = {
    '中文': 'zh-CN',
    '中文繁体': 'zh-TW',
    '英语': 'en',
    '日语': 'ja',
    '印地语': 'hi',
    '普什图语': 'ps',
    '葡萄牙语': 'pt',
    '苗语': 'hmn',
    '克罗地亚语': 'hr',
    '海地克里奥尔语': 'ht',
    '匈牙利语': 'hu',
    '意第绪语': 'yi',
    '亚美尼亚语': 'hy',
    '约鲁巴语': 'yo',
    '印尼语': 'id',
    '伊博语': 'ig',
    '布尔语(南非荷兰语)': 'af',
    '冰岛语': 'is',
    '意大利语': 'it',
    '阿姆哈拉语': 'am',
    '希伯来语': 'iw',
    '阿拉伯语': 'ar',
    '阿塞拜疆语': 'az',
    '南非祖鲁语': 'zu',
    '罗马尼亚语': 'ro',
    '宿务语': 'ceb',
    '白俄罗斯语': 'be',
    '俄语': 'ru',
    '保加利亚语': 'bg',
    '卢旺达语': 'rw',
    '孟加拉语': 'bn',
    '印尼爪哇语': 'jw',
    '波斯尼亚语': 'bs',
    '信德语': 'sd',
    '格鲁吉亚语': 'ka',
    '僧伽罗语': 'si',
    '斯洛伐克语': 'sk',
    '斯洛文尼亚语': 'sl',
    '萨摩亚语': 'sm',
    '修纳语': 'sn',
    '索马里语': 'so',
    '阿尔巴尼亚语': 'sq',
    '加泰罗尼亚语': 'ca',
    '塞尔维亚语': 'sr',
    '哈萨克语': 'kk',
    '塞索托语': 'st',
    '高棉语': 'km',
    '印尼巽他语': 'su',
    '卡纳达语': 'kn',
    '瑞典语': 'sv',
    '韩语': 'ko',
    '斯瓦希里语': 'sw',
    '中文（繁体）': 'zh-TW',
    '库尔德语': 'ku',
    '科西嘉语': 'co',
    '泰米尔语': 'ta',
    '吉尔吉斯语': 'ky',
    '捷克语': 'cs',
    '泰卢固语': 'te',
    '塔吉克语': 'tg',
    '泰语': 'th',
    '拉丁语': 'la',
    '卢森堡语': 'lb',
    '威尔士语': 'cy',
    '土库曼语': 'tk',
    '菲律宾语': 'tl',
    '丹麦语': 'da',
    '土耳其语': 'tr',
    '鞑靼语': 'tt',
    '德语': 'de',
    '老挝语': 'lo',
    '立陶宛语': 'lt',
    '拉脱维亚语': 'lv',
    '维吾尔语': 'ug',
    '乌克兰语': 'uk',
    '马尔加什语': 'mg',
    '毛利语': 'mi',
    '乌尔都语': 'ur',
    '马其顿语': 'mk',
    '马拉雅拉姆语': 'ml',
    '夏威夷语': 'haw',
    '蒙古语': 'mn',
    '马拉地语': 'mr',
    '乌兹别克语': 'uz',
    '马来语': 'ms',
    '马耳他语': 'mt',
    '希腊语': 'el',
    '世界语': 'eo',
    '缅甸语': 'my',
    '西班牙语': 'es',
    '爱沙尼亚语': 'et',
    '巴斯克语': 'eu',
    '越南语': 'vi',
    '尼泊尔语': 'ne',
    '波斯语': 'fa',
    '荷兰语': 'nl',
    '挪威语': 'no',
    '芬兰语': 'fi',
    '齐切瓦语': 'ny',
    '法语': 'fr',
    '弗里西语': 'fy',
    '爱尔兰语': 'ga',
    '苏格兰盖尔语': 'gd',
    '奥利亚语': 'or',
    '加利西亚语': 'gl',
    '古吉拉特语': 'gu',
    '南非科萨语': 'xh',
    '旁遮普语': 'pa',
    '豪萨语': 'ha',
    '波兰语': 'pl'
}


class Translate:
    def __init__(self):
        self.session = requests.session()
        ret = self.session.get(_URL_VIS, headers=_HEADERS)
        print('Translate 初始化结果:%d' % ret.status_code)
        pass

    def __del__(self):
        self.session.close()
        pass

    def tran(self, q: str, to=''):
        log = ''
        _DATA['q'] = q
        if to == '':
            # 没有提供具体翻译方向 按照默认方向翻译
            _DATA['tl'] = 'en'
            '''
            默认翻译方向
            zh --> en
            其他 --> zh-CN
            '''
            # 进行测试翻译 用于判断翻译方向
            ret = self.session.post(_URL_TRAN, headers=_HEADERS, data=_DATA)
            if ret.status_code != 200:
                log = '翻译失败！SC：%d RAISE:%s' % (
                    ret.status_code, ret.raise_for_status())
                return log
            result = ret.json()
            if result[2] == 'zh-CN':
                _DATA['tl'] = 'en'
                pass
            else:
                _DATA['tl'] = 'zh-CN'
                pass
            pass
        else:
            if to not in dictLang:
                log = '翻译失败！不支持%s'%to
                return log
            else:
                _DATA['tl'] = dictLang[to]
                pass
            pass

        # 翻译
        ret = self.session.post(_URL_TRAN, headers=_HEADERS, data=_DATA)
        if ret.status_code != 200:
            log = '翻译失败！SC：%d RAISE:%s' % (
                ret.status_code, ret.raise_for_status())
            return log
        data = ret.json()
        # 以 “你好” 为例
        # 0 列表 翻译结果
        #  00 列表 第一行翻译结果列表
        #   000 str 第一行翻译文本
        #   001 str 第一行原始文本
        #   002 None 未知
        #   003 None 未知
        #   004 int 未知
        #  ...
        #  0n 列表 发音标识列表
        #   0n0 None 未知
        #   0n1 None 未知
        #   0n2 None 未知
        #   0n3 发音标识文本
        # 1 列表 推荐翻译列表
        #  10 列表
        #   100 str 词性
        #   101 列表 该词性可翻译的列表 长度为n
        #   102 列表 所有上述列表中每一项的翻译 长度为n
        #    1020 列表 第0项翻译
        #     10200 str 第0项翻译内容
        #     10201 列表 第0项原始文本同义项
        #     10202 None 未知
        #     10203 float 使用频率
        #    ...
        #    102n 列表 第n项翻译
        #   103 str 原始文本
        #   104 int 未知
        #  ..
        # 2 str 原始语言
        # 3 None 未知
        # 4 None 未知
        # 5 列表 改进方案
        # 7 float 未知
        # 8 列表 未知
        # 9 列表 未知
        for item in data:
            print(item)
            pass
        #拼合翻译结果
        length=len(data[0])-1
        result=''
        for i in range(length):
            result=result+data[0][i][0]
            pass
        return result
        pass  # 方法结束
    pass


if __name__ == '__main__':
    tran = Translate()
    print(tran.tran('want\ngood'))
    #print(tran.tran('第一行\n第二行\n'))
    #print(tran.tran('こんにちは！'))
    #print(tran.tran('Hello！'))
    #print(tran.tran('你好！','日语'))
    #print(tran.tran('こんにちは！','英语'))
    #print(tran.tran('Hello！','中文繁体'))
    pass
