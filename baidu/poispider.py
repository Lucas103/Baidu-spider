#coding: utf-8
import requests
import json
import time
import os
import pandas as pd


class spider:
    def __init__(self,KeyWord):
        self.KeyWord = KeyWord
        self.filepath = "data/poi.txt"
        self.URL = "http://api.map.baidu.com/place/v2/search?query=" #多边形搜索
        self.baiduAk = [
            #这里要用自己申请到的key
            #我把自己的删了，因为总是有人用，百度平台老是给我发警告邮件 
        ]
        self.keyNum = 0
        title = open('data/new_title.txt', 'r').read()
        open(self.filepath, 'w').write(title)


    def getSmallRect(self,bigRect, windowSize, windowIndex):
        """
        获取小矩形的左上角和右下角坐标字符串（百度坐标系）
        :param bigRect: 关注区域坐标信息
        :param windowSize:  细分窗口数量信息
        :param windowIndex:  Z型扫描的小矩形索引号
        :return: lat,lng,lat,lng
        """
        offset_x = (bigRect['right']['x'] - bigRect['left']['x'])/windowSize['xNum']
        offset_y = (bigRect['right']['y'] - bigRect['left']['y'])/windowSize['yNum']
        left_x = bigRect['left']['x'] + offset_x * (windowIndex % windowSize['xNum'])
        left_y = bigRect['left']['y'] + offset_y * (windowIndex // windowSize['yNum'])
        right_x = (left_x + offset_x)
        right_y = (left_y + offset_y)
        return str(left_y) + ',' + str(left_x) + ',' + str(right_y) + ',' + str(right_x)


    def requestBaiduApi(self,smallRect):
        pageNum = 0
        pois = []
        while True:
            try:
                URL = self.URL + self.KeyWord + \
                    "&bounds=" + smallRect + \
                    "&output=json" +  \
                    "&ak=" + self.baiduAk[self.keyNum] + \
                    "&scope=2" + \
                    "&page_size=20" + \
                    "&page_num=" + str(pageNum)
                print(pageNum)
                #print(URL)
                resp = requests.get(URL)
                jsondata = json.loads(resp.text)
                # status = 0表示API访问成功
                if jsondata['status'] == 0:
                    if len(jsondata['results']) == 0:
                        print('当前所有页数查找完成')
                        break
                    else:
                        for r in jsondata['results']:
                            pois.append(r)
                    pageNum += 1
                    time.sleep(1)
                else:
                #如果访问不成功就换一个key继续请求
                    self.keyNum = self.keyNum +1
                    print(self.keyNum)
                    self.requestBaiduApi(smallRect)       
            except:
                #如果出现异常就休息1秒，然后继续请求API
                time.sleep(60)
                self.requestBaiduApi(smallRect)
                print('except')
                break
        return pois

    """
        poiwrite函数说明
        将poi中的location分开成log和lng，生成poilist
        之后将poilist数据写入poi.txt文件中
    """
    def poiwrite(self,all_pois):
        poilist = []
        for poi in all_pois:
            content = {}
            if poi == None:
                continue
            content['name'] = poi.get('name')
            content['address'] = poi.get('address')
            location = poi['location']
            content['lat'] = location['lng']
            content['lng'] = location['lat']
            content['province'] = poi.get('province')
            content['city'] = poi.get('city')
            content['area'] = poi.get('area')
            content['street_id'] = poi.get('street_id')
            content['uid'] = poi.get('uid')
            content['detail_info'] = poi.get('detail_info')
            poilist.append(content)
        #将poi数据写入poi.txt文件中
        for POIDict in poilist:
            POIArr = list(POIDict.values())
            POIArr = [str(value).replace(',', '，') for value in POIArr]
            POILine = ','.join(POIArr) + '\n'
            open(self.filepath, 'a', encoding='utf-8').write(POILine)

    ## 导入经纬度范围文件，输出是list格式的最大最小经纬度+count
    """
    loadDatadet函数说明
    infile是txt文件
    k是txt文件中的列数
    输出dataset是xmin，ymin，xmax，ymax，count
    后续要del(dataset[0]),因为第一行是title
    """
    def loadDatadet(self,infile,k):
        f=open(infile,'r')
        sourceInLine=f.readlines()
        dataset=[]
        for line in sourceInLine:
            temp1=line.strip('\n')
            temp2=temp1.split(',')
            dataset.append(temp2)
        for i in range(1,len(dataset)):
            for j in range(k):
                dataset[i].append(float(dataset[i][j]))
            del(dataset[i][0:k])
        return dataset


    def poi_spider(self,infile):
        for i in range(len(infile)):

            BigRect = {
                'left': {'x': infile[i][0],
                         'y': infile[i][1]},
                'right': {'x': infile[i][2],
                          'y': infile[i][3]}
            }
            #开始爬取poi数据
            all_pois = []
            for index in range(int(WindowSize['xNum'] * WindowSize['yNum'])):
                smallRect = self.getSmallRect(BigRect, WindowSize, index)
                #print(smallRect)
                pois = self.requestBaiduApi(smallRect=smallRect)
                all_pois.extend(pois)
                time.sleep(1)
            self.poiwrite(all_pois)
        print('爬取完成')





if __name__ == '__main__': 
  #  main()
    #查询关键字，只支持单个
    spi = spider(KeyWord = u"美食")

    #划分细分窗口的数量，横向X * 纵向Y
    WindowSize = {
        'xNum': 2.0,
        'yNum': 2.0
    }

    #读取经纬度范围及count的.txt文件
    infile='data/location.txt'
    k=5
    fileout = spi.loadDatadet(infile,k)
    del(fileout[0]) #去掉表头

    spi.poi_spider(fileout) #爬取poi数据并保存
    print('程序结束')


