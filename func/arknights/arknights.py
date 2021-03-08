import requests

'''
查询掉率
https://penguin-stats.cn/PenguinStats/api/v2/result/matrix

查询关卡
https://penguin-stats.cn/PenguinStats/api/v2/stages

查询材料
https://penguin-stats.cn/PenguinStats/api/v2/items
'''


# 返回单件理智最低的相关信息
# {'stageId': 'main_01-07', 'itemId': '30012', 'quantity': 356060, 'times': 286284, 'start': 1556676000000, 'unitAP': 4.82}
def queryRate(itemId):
    url = 'https://penguin-stats.cn/PenguinStats/api/v2/result/matrix'
    d = {'itemFilter': itemId}
    r = requests.get(url, params=d)
    data = r.json()
    if 'matrix' not in data:
        return {}
        pass
    data = data['matrix']
    # 计算单件理智
    for item in data:
        apCost = queryStageAP(item['stageId'])
        dropRate = item['quantity'] / item['times']
        if dropRate == 0:
            unitAP = 0x7fffffff
            pass
        else:
            unitAP = 100 * apCost // dropRate / 100
            pass
        item['unitAP'] = unitAP
        pass
    data = sorted(data, key=lambda i: i['unitAP'])

    titile = '\n   关 卡  |单件预估理智\n'
    value = titile
    for row in data[0:2]:
        value = value + '%s|%.2f\n' % (row['stageId'], row['unitAP'])
        pass
    return value
    pass


def queryItem(name):
    url = 'https://penguin-stats.cn/PenguinStats/api/v2/items'
    r = requests.get(url)
    print(r.status_code)
    data = r.json()

    for item in data:
        # print(type(item))
        alias = item['alias']['zh']

        for a in alias:
            if a == name:
                return item['itemId']
            pass
        pass
    return 0


url = 'https://penguin-stats.cn/PenguinStats/api/v2/stages'
r = requests.get(url)
stageInfomations = r.json()


# 查询关卡所需理智
def queryStageAP(stageId):
    for item in stageInfomations:
        if (item['stageId'] == stageId):
            return item['apCost']
            pass
        pass
    return 0
    pass


def queryDrap(name):
    return queryRate(queryItem(name))
    pass


if __name__ == '__main__':
    print(type(queryDrap('异铁组')))

    pass
