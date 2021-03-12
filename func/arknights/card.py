from random import *
import os
class Card:
    dictRole={
        '六星':[],
        '五星':[],
        '四星':[],
        '三星':[],
    }
    dictRoleUp = {
        '六星': ['史尔特尔','黑'],
        '五星': ['雷蛇','崖心','奥斯塔']
    }
    listRecord={
        274252932:{
            'getNums':0,
            'guaranteedNums':0
        }
    }
    def __init__(self):
        #加载干员列表
        with open(os.path.dirname(__file__)+'./role.txt','r',encoding='utf-8') as f:
            rows=f.read().splitlines()
            for row in rows:
                _result=row.split(' ')
                self.dictRole[_result[0]].append(_result[1])
            pass

        pass
    def __del__(self):
        pass
    #添加成员 不进行检查
    def addMember(self,memberId):
        temp = {
            'getNums': 0,
            'guaranteedNums': 0
        }
        self.listRecord[memberId] = temp
        pass
    #设置up干员
    def setRoleUp(self):
        pass

    #清除抽取记录
    def resetRecord(self,memberId):
        if memberId not in self.listRecord:
            self.addMember(memberId)
            pass
        else:
            self.listRecord[memberId]['getNums']=0
            self.listRecord[memberId]['guaranteedNums'] = 0
            pass
        return str(self.listRecord[memberId])
        pass

    def calcProb(self,memberId):
        prob ={
            '三星': 40,
            '四星': 50,
            '五星': 8,
            '六星': 2,
        }
        # 获取该成员的抽取记录
        record = self.listRecord[memberId]
        if record['guaranteedNums'] >= 50:
            # 六星概率开始增加
            extnums = record['guaranteedNums'] - 50
            prob['六星'] = prob['六星'] + extnums * 2
            if extnums <= 20:
                # 减少3星概率
                prob['三星'] = prob['三星'] - extnums * 2
                pass
            elif extnums <= 45:
                # 减少3,4星概率
                prob['三星'] = 0
                extnums = extnums - 20
                prob['四星'] = prob['四星'] - extnums * 2
                pass
            elif extnums <= 48:
                # 减少3,4,5星概率
                prob['三星'] = 0
                extnums = extnums - 20
                prob['四星'] = 0
                extnums = extnums - 25
                prob['五星'] = prob['五星'] - extnums * 2
                pass
            else:
                # 必出
                prob['三星'] = 0
                prob['四星'] = 0
                prob['五星'] = 0
                pass
            print(prob)
            pass
        return prob
        pass

    #抽取
    def getCard(self,memberId):
        if memberId not in self.listRecord:
            self.addMember(memberId)
            pass
        #计算当次抽取概率
        prob=self.calcProb(memberId)
        #计算概率分布
        prob['四星']=prob['四星']+prob['三星']
        prob['五星'] = prob['五星'] + prob['四星']
        prob['六星'] = prob['六星'] + prob['五星']
        #print(prob)
        #星级抽取
        ch=randint(1,100)
        star=''
        for key in prob:
            if ch<=prob[key]:
                star = key
                break
                pass
            pass
        #print(star)
        #相应星级的干员抽取
        role=''
        if star in self.dictRoleUp:
            #5,6 有up
            ch=randint(1,100)
            if(ch<=50):
                role=choice(self.dictRole[key])
                pass
            else:
                role = choice(self.dictRoleUp[key])
                pass
            pass
        else:
            role = choice(self.dictRole[key])
            pass


        self.listRecord[memberId]['getNums']=self.listRecord[memberId]['getNums']+1
        if star=='六星':
            self.listRecord[memberId]['guaranteedNums'] = 0
            pass
        else:
            self.listRecord[memberId]['guaranteedNums'] = self.listRecord[memberId]['guaranteedNums'] + 1
            pass

        nextProb=self.calcProb(memberId)
        ##print(key,role,self.listRecord[memberId],nextProb)
        return str([key,role,self.listRecord[memberId],nextProb])
        pass

    def getCard10(self,memberId):
        ret=''
        for i in range(10):
            ret=ret+str(self.getCard(memberId))+'\n'
            pass
        #print(ret)
        return ret
        pass
    pass
if __name__=='__main__':
    c=Card()
    member=274252932
    c.getCard(member)
    c.getCard(member)
    c.getCard(member)
    c.getCard10(member)
    pass