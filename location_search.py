import pandas as pd
import requests
import time
import csv
import json
import os
from dotenv import load_dotenv
load_dotenv()

# 根据地址来得到经纬度
def gaode(addr):
        """
        param:addr 地点的地址，例如北京交通大学南门
        return:m 经纬度，例如"116.341772,39.948189"
        """
        para = {
            'key':os.getenv('AMAP_KEY'),  #高德地图开放平台申请的key
            'address':addr #传入地址参数
        }
        url = os.getenv('AMAP_URL') #高德地图API接口
        try:
            req = requests.get(url,para)
            req = req.json()
            if req["status"] == "1" and int(req["count"]) > 0:
                # print('-' * 30)
                m = req['geocodes'][0]['location']
                print(addr,m)
            else:
                print(f"请求失败: {req.get('info', '未知错误')}")
                return None
        except Exception as e:
            print(f"请求异常: {str(e)}")
            return None
        return m

def search_location(raw_file_name,save_file_name):
    """
    param:raw_file_name 里面是原始的地点如北京交通大学
    param:save_file_name 存储原始地点的经纬度的文件
    """
    # 读取地点
    location = pd.read_csv(raw_file_name,header=None)
    data = location.values[0::,0::]
    # 存储经纬度
    m_s = []
    # 存储地点
    addrs = []
    for i in range(len(data)):
        addr = data[i][0]
        addrs.append(addr)
        # 由于免费的api调用并发数是3次每秒
        time.sleep(0.4)
        m = gaode(addr)
        m_s.append(m)
    # 将经纬度存储起来
    with open(save_file_name,'w',newline='',encoding="utf-8") as f:
        writer = csv.writer(f)
        for addr, m in zip(addrs,m_s):
            m_list = m.split(',')
            writer.writerow([addr,m_list[0],m_list[1]])
         
if __name__ == "__main__":
    raw_file_name = "raw_location.csv"
    save_file_name = "test_jingweidu.csv"
    search_location(raw_file_name=raw_file_name,save_file_name=save_file_name)
    

 
     