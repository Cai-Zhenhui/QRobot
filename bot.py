import os
import random
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch, OptionalParam, RequireParam,OptionalParam
import asyncio

from graia.application.message.elements.internal import At, Plain, Quote, Image, Face, Source
from graia.application.friend import Friend
from graia.application.group import Group, Member

from func.translate import Translate
import func.arknights.arknights as arknights
from func.arknights.card import Card
from func.pixivpic import Pixivpic

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
RobotNumber = 2167480761
s = Session(
    host='http://47.93.148.239:8080',
    authKey='INITKEYzch6rcNE',
    account=RobotNumber,
    websocket=True
)
if os.path.exists('./Local'):
    # 本地
    s.host = 'http://47.93.148.239:8080'
    print(s.host)
    pass
else:
    s.host = 'http://127.0.0.1:8080'
    print(s.host)
    pass
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=s
)


@bcc.receiver('FriendMessage')
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    print(friend.id, friend.nickname)
    pass


@bcc.receiver('GroupMessage', dispatchers=[
    Kanata([FullMatch('翻译'), RequireParam(name='mcPara')])
])
async def group_message_handler(
        message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        mcPara: MessageChain
):
    if group.id != 817108947 and group.id != 434598019:
        return
    strPara = mcPara.asDisplay()
    print("翻译handle " + strPara)

    tran = Translate()
    # print(strCmd)
    if strPara[0] == ' ' or strPara[0] == '\n':
        # 翻译 你好！
        ret = tran.tran(strPara[1:])
        pass
    else:
        # 翻译到日语 你好！
        nPos = strPara.find(' ')
        ret = tran.tran(strPara[nPos:], strPara[1:nPos])
        pass

    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain('\n' + ret)
    ]))
    pass

'''
@bcc.receiver('GroupMessage', dispatchers=[
    Kanata([FullMatch('方舟 '), RequireParam(name='mcPara')])
])
async def group_message_handler(
        message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        mcPara: MessageChain
):
    strPara = mcPara.asDisplay()
    print("方舟handle " + strPara)
    ret = arknights.queryDrap(strPara)
    if not isinstance(ret, str):
        return
    ret = '%s\n%s' % (strPara, ret)

    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain('\n' + ret)
    ]))
    pass
'''
arknightsCard=Card()
@bcc.receiver('GroupMessage', dispatchers=[
    Kanata([FullMatch('方舟 '), RequireParam(name='mcPara')])
])
async def group_message_handler(
        message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        mcPara: MessageChain
):
    if group.id != 817108947 and group.id != 434598019:
        return
    strPara = mcPara.asDisplay()
    print("方舟handle " + strPara)
    #材料 研磨石
    if strPara=='1':
        ret=arknightsCard.getCard(member.id)
        pass
    elif strPara=='10':
        ret = arknightsCard.getCard10(member.id)
        pass
    elif strPara=='reset':
        ret = arknightsCard.resetRecord(member.id)
        pass
    else:
        ret = arknights.queryDrap(strPara)
        if not isinstance(ret, str):
            return
        ret = '%s\n%s' % (strPara, ret)
        pass



    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain('\n' + ret)
    ]))
    pass


@bcc.receiver('GroupMessage', dispatchers=[
    Kanata([FullMatch('P图 '), RequireParam(name='mcPara')])
])
async def group_message_handler(
        message: MessageChain,
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        mcPara: MessageChain
):
    if group.id!=817108947 and group.id!=434598019:
        return
    strPara = mcPara.asDisplay()
    print("P图handle " + strPara)

    '''
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain('修复ing')
    ]))
    return'''

    pix = Pixivpic()
    ret = pix.query(strPara)
    print(ret)
    if ret == '':
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain('没有'), Face(faceId=98)
        ]))
        return
        pass
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Image.fromNetworkAddress(ret)
    ]))

    pass


@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    if group.id != 817108947 and group.id != 434598019:
        return
    strMessage = message.asDisplay()
    print("普通handle " + strMessage)

    if strMessage.startswith('/测试'):
        ch = random.randint(0, 256)
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),
            Plain("你测个锤子!!!\n给你一个随机表情吧！ch:" + str(ch)),
            Face(faceId=ch)
        ]))
        pass
    elif strMessage.startswith('好家伙'):
        print(message)
        print(message.__root__[0].id)
        print(type(message))

        await app.sendGroupMessage(group, MessageChain.create([
            Plain(' '),
            At(member.id),
            Plain('这是回复内容')
        ]))
        pass
    elif strMessage.endswith('好家伙'):
        print(message.asSerializationString())
        print("message:")
        for item in message:
            print(item.__class__, item)
            pass
        print(message.__root__)
        print("message__root__:")
        for item in message.__root__:
            print(item.__class__, item)
            pass
        pass
    pass

app.launch_blocking()
