"""
本文件用来在地图中绘制路线图，可以在一张图中同时绘制不同的路线
"""
import requests
from OpenSSL import SSL
import numpy as np
import folium
from folium import plugins
import pandas as pd
import webbrowser
import os
from replaceJS import replaceJsRef
from location_search import search_location
import time
import argparse
from dotenv import load_dotenv
load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(description='usage of road_map')

    parser.add_argument('--raw_location_dir',type=str,help='存储要绘制路径的地点文件，一个文件代表要绘制的一条路线')
    parser.add_argument('--jingweidu_location_dir',type=str,help='存储带有经纬度的地点文件')
    parser.add_argument('--html_file_name',type=str,help='保存路径的html文件名')
    parser.add_argument('--map_type',type=str,help='地图类型，街道图，路网图，卫星图')

    args = parser.parse_args()
    return args


# 颜色
colors = ['#0166ff','#65fbfa','#04fccc','#fe0000','#f842b5','#8a78bf','#acf1e3','#fbb1fa','#56777a'
         ,'#97f496','#fa8781','#227709','#f90e89','#4f70a6','#a503c9','#770076','#99f928','#ef84bd',
         '#d1ced4','#eebbf7','#b2838c','#8a0903','#95da02','#f6f7ec','#07357c','#3a0088','#5792ff',
         '#cc8767','#840740','#fd41ab','#ff0188','#a32c01','#96a01d','#d4f8fb','#020278','#01349c',
         '#c907f1','#6e6469','#71c5e8','#33cbf6','#009fcc','#00aaaa','#fcfb36','#cf6605','#c63300']

# 得到路径
def get_road(file_name,strategy,amap_key):
    """
    param:file_name 一个文件代表一条车的路径
    param:strategy 路径规划的策略
    param:amap_key: api的key
    return:list_latlon: list 路径上每个点的经纬度
    """
    list_latlon = []
    location = pd.read_csv(file_name,sep=',',names=['position','lon','lat'])#读取csv
    data = location.iloc[:,1:]#读取经纬度
    for i in range(len(data)-1):
        start = str(data.lon[i]) + ',' + str(data.lat[i])
        end = str(data.lon[i+1]) + ',' + str(data.lat[i+1])
        time.sleep(0.5)
        route = get_route(start, end, strategy, amap_key)
        if route:
            for i, step in enumerate(route):
                list_latlon.append(step["polyline"])
                print(f'步骤 {i+1}: {step["instruction"]}:{step["polyline"]}')
                print(f'步骤 {i+1}: {step["instruction"]}')
        else:
            print('无法获取路线规划。')
    return list_latlon


# 根据起点和终点的经纬度来获取它们中间的路径
def get_route(start, end, strategy, amap_key):
    """
    param:start str 路线的起点（经度，纬度）
    param:end str 路线的终点（经度，纬度）
    param:strategy 行车的策略
    param:amap_key api key
    """
    # 这里的url中选择是步行，公交还是驾车路径，本文中driving?表示驾车，具体介绍见：https://lbs.amap.com/api/webservice/guide/api/direction
    url = f'https://restapi.amap.com/v3/direction/driving?origin={start}&destination={end}&strategy={strategy}&key={amap_key}'
    try:
        response = requests.get(url)
    except Exception as e:
        print("错误：",e)
    data = response.json()
    if data['status'] == '1':
        route = data['route']['paths'][0]['steps']
        return route
    else:
        print(f"请求失败 {data.get('info')}")
        return None

# 根据经纬度来绘制路线图
def PlotLineOnMap(Lat, Lon,jingweidu_file_names,html_file_path,map_title):
    """
    param: Lat纬度
    param: Lon经度
    param: jingweidu_file_names 包含地点经纬度的文件
    param: html_file_path 最终绘制的路线html文件名
    """
    # 给出的坐标系为GCJ-02，如果需要测试google地图，需要进行坐标转换
    tri_total = []
    #将每辆车的路线给添加进去
    for i in range(len(Lat)):
        tri = np.array(list(zip(Lat[i],Lon[i])))
        tri_total.append(tri)
    #绘制地图
    # location代表以哪个地点为中心展示地图（纬度，经度）
    san_map = folium.Map(
        location=[39.952279,116.342809],
        zoom_start=16,
        # titles地图在线的瓦片图层
        tiles=map_title,
        attr='default')
    color_number = 0
    
    # 绘制每条路径的路线图
    for tri in tri_total:
        folium.PolyLine(tri, 
            weight=6,  # 线的大小
            color=colors[color_number],  # 线的颜色
            opacity=0.8,  # 线的透明度
            ).add_to(san_map)
        color_number += 1

    # 标记每个地点
    marker_cluster = plugins.MarkerCluster().add_to(san_map)
    for index,jingweidu_file_name in enumerate(jingweidu_file_names):
        count = 0
        location = pd.read_csv(jingweidu_file_name,sep=',',names=['position','lon','lat'])#读取csv
        data = location.iloc[:,0:]#读取经纬度
        for i in range(len(data)):
            # 给每个地点打标记
            label = str(count+1) + " " + data.position[i]
            count = count + 1
            popup = folium.Popup(label, parse_html=True)
            folium.Marker([data.lat[i],data.lon[i]], color=colors[index+1],
                          popup=popup,tooltip=label,show=True
                        ).add_to(marker_cluster)#绘制点
    
    # 保存路径图html
    san_map.save(html_file_path)
    #将在线的javascript替换为离线的javascript
    replaceJsRef(html_file_path)
    
if __name__ == '__main__':
    args = parse_args()
    raw_location_dir = args.raw_location_dir
    jingweidu_location_dir = args.jingweidu_location_dir
    html_file_name = args.html_file_name
    map_type = args.map_type
    # 原始的地点文件
    all_names = os.listdir(raw_location_dir)
    # 过滤出仅文件（排除子目录）
    file_names = [name for name in all_names 
                if os.path.isfile(os.path.join(raw_location_dir, name))]
    # 存储原始路径的文件
    raw_location_file_names = [os.path.join(raw_location_dir,file_name) for file_name in file_names]
    # 存储地点的经纬度文件
    jingweidu_file_names = [os.path.join(jingweidu_location_dir,file_name) for file_name in file_names]
    for raw_location_file_name,jingweidu_file_name in zip(raw_location_file_names,jingweidu_file_names):
        search_location(raw_file_name=raw_location_file_name,save_file_name=jingweidu_file_name)
    strategy = 2#策略二，走距离优先道路
    # api_key
    amap_key = os.getenv('AMAP_KEY')
    list_latlon_total = []
    # 存储每条路径的经过的点的纬度
    Lat_total = []
    # 存储每条路径的经过的点的经度
    Lon_total = []
    for jingweidu_file_name in jingweidu_file_names:
        list_latlon = get_road(file_name=jingweidu_file_name,strategy=strategy,amap_key=amap_key)
        list_latlon_total.append(list_latlon)
    for items in list_latlon_total:
        Lon = []
        Lat = []
        for item in items:
            points = item.split(';')
            for point in points:
                coords = point.split(',')
                Lon.append(float(coords[0]))
                Lat.append(float(coords[1]))
        Lat_total.append(Lat)
        Lon_total.append(Lon)
    # 存储的路线图的文件名
    weixing_map = "https://webst01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=6&x={x}&y={y}&z={z}"#高德卫星图
    luwang_map = "https://webst01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}"#高德路网图
    jiedao_map = "https://webst01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}"#高德街道图
    if map_type == '街道图':
        PlotLineOnMap(Lat_total, Lon_total,jingweidu_file_names=jingweidu_file_names,html_file_path=html_file_name,map_title=jiedao_map)
    elif map_type == '路网图':
        PlotLineOnMap(Lat_total, Lon_total,jingweidu_file_names=jingweidu_file_names,html_file_path=html_file_name,map_title=luwang_map)
    elif map_type == '卫星图':
        PlotLineOnMap(Lat_total, Lon_total,jingweidu_file_names=jingweidu_file_names,html_file_path=html_file_name,map_title=weixing_map)
    # webbrowser.open(html_file_name)
