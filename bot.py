import os
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication,Session
from graia.application.message.chain import  MessageChain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch,OptionalParam,RequireParam
import asyncio

from graia.application.message.elements.internal import At,Plain,Quote,Image,Face,Source
from graia.application.friend import Friend
from graia.application.group import Group,Member

from func.translate import Translate
import func.arknights.arknights as arknights
from func.pixivpic import Pixivpic

loop=asyncio.get_event_loop()
bcc=Broadcast(loop=loop)
s=Session(
    host='http://47.93.148.239:8080',
    authKey='INITKEYzch6rcNE',
    account=2167480761,
    websocket=True
)
if os.path.exists('./Local'):
    #本地
    host = 'http://47.93.148.239:8080',
    pass
else:
    host = 'http://127.0.0.1:8080',
    pass
app=GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=s
)

@bcc.receiver('FriendMessage')
async def friend_message_listener(app: GraiaMiraiApplication,friend: Friend):
    print(friend.id,friend.nickname)
    pass

@bcc.receiver('GroupMessage',dispatchers=[
    Kanata([FullMatch('翻译'),RequireParam(name='strPara')])
])
async def group_message_handler(
        message:MessageChain,
        app:GraiaMiraiApplication,
        group:Group,
        member:Member,
        strPara:MessageChain
):
    print("翻译handle "+strPara.asDisplay())
    tran=Translate()
    strCmd=strPara.asDisplay()
    #print(strCmd)
    if strCmd[0]==' ':
        #翻译 你好！
        ret = tran.tran(strCmd[1:])
        pass
    else:
        #翻译到日语 你好！
        nPos=strCmd.find(' ')
        ret=tran.tran(strCmd[nPos:],strCmd[1:nPos])
        pass

    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain(ret)
    ]))
    pass

@bcc.receiver('GroupMessage',dispatchers=[
    Kanata([FullMatch('方舟 '),RequireParam(name='strPara')])
])
async def group_message_handler(
        message:MessageChain,
        app:GraiaMiraiApplication,
        group:Group,
        member:Member,
        strPara:MessageChain
):
    print("方舟handle " + strPara.asDisplay())
    ret=arknights.queryDrap(strPara.asDisplay())
    if type(ret)!=str:
        return
    ret='%s\n%s'%(strPara.asDisplay(),ret)

    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain(ret)
    ]))
    pass


@bcc.receiver('GroupMessage',dispatchers=[
    Kanata([FullMatch('P图 '),RequireParam(name='mcPara')])
])
async def group_message_handler(
        message:MessageChain,
        app:GraiaMiraiApplication,
        group:Group,
        member:Member,
        mcPara:MessageChain
):
    strPara = mcPara.asDisplay()
    print("P图handle " + strPara)

    pix=Pixivpic()
    ret=pix.query(strPara)
    if ret=='':
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain('没有'), Face(faceId=98)
        ]))
        return
        pass
    await app.sendGroupMessage(group, MessageChain.create([
        At(member.id), Plain('\n'),Image.fromNetworkAddress(ret)
    ]))
    pass


@bcc.receiver("GroupMessage")
async def group_message_handler(
    message: MessageChain,
    app: GraiaMiraiApplication,
    group: Group, member: Member,
):
    strMessage=message.asDisplay()
    print("普通handle " + strMessage)

    if strMessage.startswith('/测试'):
        await app.sendGroupMessage(group,MessageChain.create([
            At(member.id),Plain("你测个锤子!!!\n给你一个张图片吧！"),Image.fromLocalFile('C:\\Users\\MACHENIKE\\Pictures\\01.jpg')
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
            print(item.__class__,item)
            pass
        print(message.__root__)
        print("message__root__:")
        for item in message.__root__:
            print(item.__class__,item)
            pass
        pass
    pass

app.launch_blocking()