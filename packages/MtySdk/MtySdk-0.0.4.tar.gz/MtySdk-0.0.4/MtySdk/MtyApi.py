#coding=utf-8

from websocket import create_connection
import json
import time
import numpy as np
import matplotlib.pyplot as plt

class MtyAuth(object):
    """
    客户信息类
    """
    def __init__(self,user_name: str = "", password: str = ""):
        self.username=user_name;
        self.password=password;

class MtyApi(object):
    """
    API类
    """
    def __init__(self,auth: MtyAuth=""):
        """
        初始化通信管道
        :param auth:
        """
        self.ws = create_connection("ws://192.168.0.114:9999/mtyj/regres/%s/%s/" %(auth.username,auth.password))
        createresult = self.ws.recv()
        print(createresult)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    def is_having(self):
        """
        队列是否还有数据
        :return:
        """
        param = {
            'function': 'ishaving'
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 200):
            return result['result']

    def query_math(self,name: str,starttime: str=None , endtime: str=None):
        """
        # 申请消费队列的消息
        ;param name:         名称
        :param starttime:   开始时间
        :param endtime:     结束时间
        :return:
        """
        param={
            'function':'registerserver',
            'name':name,
            'startDate':starttime,
            'endData':endtime
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        if (result['code'] == 0):
            print(result['msg'])
            return;
        if (result['code'] == 200):
            result['name']=name
            result['testplanid']=result['result']
            return result

        self.close();
        return None;

    def get_math(self,math):

        if math is None: return;

        """
        队列消费数据
        :param order:
        :return:
        """
        param = {
            'function': 'queryqueue',
            'name':math['name']
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        result = json.loads(result)
        return result;

    def closeposition(self,math,result,statu,price:float,volume:int):

        if statu != 'BUY' and statu!= 'SELL':
            print("statu必须是 SELL 或 BUY")
            return;

        symbol = math['name']
        if symbol is None:
            print("品种名称未填写");
            return;

        testplanid = math['testplanid']
        if testplanid is None:
            print("不符合规则的使用")
            return;

        datetime = result['datetime']
        if datetime is None:
            print("不符合规则的使用")
            return;

        if price is None:
            print("请填写报价");
            return

        if volume is None:
            print("请填写手数")
            return

        param = {
            'function': 'closeposition',
            'statu': statu,
            'symbol': symbol,
            'testplanid': testplanid,
            'datetime': datetime,
            'price': price,
            'volume': volume
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        print(result)

    def openoptions(self,math,result,statu,price:float,volume:int):

        if statu != 'BUY' and statu!= 'SELL':
            print("statu必须是 SELL 或 BUY")
            return;

        symbol = math['name']
        if symbol is None:
            print("品种名称未填写");
            return;

        testplanid = math['testplanid']
        if testplanid is None:
            print("不符合规则的使用")
            return;

        datetime = result['datetime']
        if datetime is None:
            print("不符合规则的使用")
            return;

        if price is None:
            print("请填写报价");
            return

        if volume is None:
            print("请填写手数")
            return

        param = {
            'function': 'openposition',
            'statu': statu,
            'symbol': symbol,
            'testplanid': testplanid,
            'datetime': datetime,
            'price':price,
            'volume':volume
        }
        self.ws.send(json.dumps(param))
        result = self.ws.recv()
        print(result)

    def incomeline(self,testPlanId):

        param = {
            'function': 'earnings',
            'testPlanId': testPlanId
        }
        self.ws.send(json.dumps(param))

    def incomelineresult(self):
        result = self.ws.recv()
        return result;

    def close(self):
        self.ws.close();

def showline(code):
    # 使用员工账号连接系统
    api = MtyApi(auth=MtyAuth('credi', 'admin123'))

    # 2. 查询资金
    api.incomeline(code);

    # 开窗
    plt.ion()
    # 开窗
    plt.figure(1)
    # x轴
    t_list = []
    # 实时价格
    result_list = []
    # 实时收益
    result_list2 = []

    while True:
        try:

            result = api.incomelineresult()
            if result is '':
                api.close();
                while True:
                    plt.pause(10)  # 暂停0,1秒

            result = json.loads(result)
            print(result)

            t_list.append(result['datetime'])  # x轴
            # result_list.append(result['close'])
            result_list2.append(result['income'])

            # plt.plot(t_list, result_list, color='red', marker='*', linestyle='-', label='A')
            plt.plot(t_list, result_list2, color='blue', marker='*', linestyle='-', label='B')

            plt.pause(0.1)  # 暂停0,1秒

        except:
            api.close();
            t_list.clear()
            result_list2.clear()
            result_list.clear()
            plt.clf()  # 清理窗体数据
            break
            pass