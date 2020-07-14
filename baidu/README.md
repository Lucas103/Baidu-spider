这是一个可以爬取百度指定经纬度范围内，指定关键字的POI数据。

## 相关网站
- 百度地图开放平台：http://lbsyun.baidu.com/
- 百度地图开放平台-POI地点检索接口文档：http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi

## 代码目录介绍
#### baidu
百度地图POI数据爬取

- poispider.py 程序入口文件
- data 存放爬取的POI数据目录
- new_titile.txt是爬取数据的title,这个可以根据自己需要修改
- location.txt是存放经纬度范围的地方,可以存放多个经纬度
- poi.txt就是爬取到的poi数据

##### 修改配置
需要修改的是AK密匙，poi类型，以及location.txt文件中的经纬度范围，还有划分区域的x和y大小，这个要根据经纬度
范围的大小来调整。AK密匙在http://lbsyun.baidu.com/上申请

##### 优势
能避免请求API时请求失败时得不到数据
可以避免key请求数量用尽之后断掉的问题（代码会判断key的请求数量是否用完，用完之后会使用下一个key）


##### 启动
执行命令`python poispider.py` 即可开始爬取数据，或者直接debug  













   