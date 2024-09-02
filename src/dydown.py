#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
import hashlib
import requests
import time # 时间模块
import os 
import re

#浏览器对象
path = os.path.abspath('./chromedriver-mac-arm64/chromedriver')
# driver = webdriver.Chrome(executable_path=path)
# driver2 = webdriver.Chrome()
options = webdriver.ChromeOptions()

# 启动 Selenium Wire Chrome 浏览器
service = Service(path)  # 替换为实际的 chromedriver 路径
driver = webdriver.Chrome(service=service, options=options)

# 基本信息
# 视频存放路径
catalog_mp4 = r"./mp4"
# 视频描述
describe = "裸眼3D看蜘蛛侠 #搞笑 #电影 #视觉震撼"

path_mp4=None

#已经下载的记录
is_down_listfile="is_down_list.txt"
#已经发布
#md5记录重复
def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

# 写文件保存记录
def saveFile(file_name, info):
    with open(file_name, 'a', encoding="utf-8") as f:
        f.write(str(info) + "\n")
        print('保存成功：', info)

#获取单个抖音视频并下载
def getDuyin(urlX,titlex,img):
    url = 'https://www.douyin.com/video/6881953434883329293'
    if urlX:
        url=urlX

    with open(is_down_listfile,'r',encoding='utf-8') as f:
        if get_md5_value(titlex.encode("utf-8")) in f.read():
            print("此视频已经下载过，不重复下载:"+titlex)
            return

    
    add_network_listener(driver,url)
    # video_url = requests.utils.unquote(html_data).replace('":"', 'https:')
    # print(video_url)
    # title=None
    # if titlex:
    #     title=titlex
    # else:
    #     title = re.findall('<title data-react-helmet="true">(.*?)</title>', response.text)[0]
    # #下载视频
    # video_content = requests.get(url=video_url).content
    # new_title = re.sub(r'[\/:*?"<>|]', '', title).replace('dou',"").replace('抖音','')
    # with open(catalog_mp4+'\\'+new_title  + '.mp4', mode='wb') as f:
    #     f.write(video_content)

    # #下载封面
    # imgx = requests.get(url=img).content
    # with open(catalog_mp4+'\\'+new_title  + '.jpg', mode='wb') as f:
    #     f.write(imgx)

    # # 保存记录
    # saveFile(is_down_listfile, get_md5_value(title.encode("utf-8")) + "|")
    # print(title,'下载完成')
def add_network_listener(driver,url):
   # 开启 JavaScript XHR 监听
    driver.get(url)
    time.sleep(3)  # 等待 5 秒或更长时间，具体取决于网页加载时间
    fetch_requests = []
    xhr_requests = []
    # 获取页面源代码
    requests = driver.requests

    # 过滤出包含 `video/mp4` 的请求
    video_requests = [r for r in requests if r.response and 'Content-Type' in r.response.headers and r.response.headers['Content-Type'] == 'video/mp4']


    # 使用正则表达式匹配 media 资源
    html_data = re.findall(r'src="(.*?)"%3Fa%3D', response_text)
    html_data=html_data[1]
    video_url = requests.utils.unquote(html_data).replace('":"', 'https:')
    print(video_url)
    # htparray = driver.requests

    # for request in htparray:
    #     if request.response:
    #         # 检查请求的方法
    #         if len(request.headers._headers) >0:
    #             type = request.headers._headers[1]
    #             if type == ('Content-Type', 'video/mp4'):
    #                 xhr_requests.append(request.response.url)
            
    #         # 检查请求的类型
    return fetch_requests, xhr_requests
#自动下拉加载网页
def drop_down():
    #执行页面滚动的操作""” # javascript
    for x in range(1, 30, 4):#1 3 5 79 在你不断的下拉过程中，页面高度也会变的
        time.sleep(1)
        j =x / 9 #1/9 3/9 5/9 9/9
        # document.documentElement.scrollTop 指定滚动条的位置
        # document.documentElement.scrollHeight获取浏览器页面的最大高度
        js ='document.documentElement.scrollTop = document.documentElement.scrollHeight * %f'% j
        driver.execute_script(js)

#批量下载抖音号主页视频
def batch_download_v(is_drop_down,user_url='https://www.douyin.com/user/MS4wLjABAAAABQapryGPhkxqcOLpt8Al9fvLvJ2KOyFYsotXOBHwR2I?from_tab_name=main&vid=7408072298860743971'):
    driver.get(user_url)
    #是否滑动 获取当前用户全部
    if is_drop_down:
        drop_down()
    time.sleep(5)
    pathes = '#root > div#dark > div#douyin-right-container>div.parent-route-container.route-scroll-container.LhqxgEn_>div.QHvwHWDO.userNewUi>div.QHvwHWDO>div._VjKwvvf.pJdBcpMy.Wv23DMGi>div.m6kxDS2G > div.U2wOk1TN > div > div.dqHKDiay > div.ng0pvUVS > div.cBiJe2DK > ul '
    # pathes = '#root > div#dark > div#douyin-right-container>div.QHvwHWDO.userNewUi>div.QHvwHWDO>div._VjKwvvf.pJdBcpMy.Wv23DMGi>div.m6kxDS2G > div.U2wOk1TN > div > div.dqHKDiay > div.ng0pvUVS > div.cBiJe2DK > ul '
    lis = driver.find_elements_by_css_selector(pathes)
    # lis = driver.find_elements_by_css_selector('#root > div#dark > div#douyin-right-container.rc4Wp8Tf.cVpuhzPi.oyPORRAm>div#parent-route-container> div.QHvwHWD0.userNewUi > div.QHvwHWDO> div._VjKwvvf.pJdBcpMy.Wv23DMGi > div.m6kxDS2G > div.U2wOk1TN.v1v4QuDY > div > div.dqHKDiay.v1v4QuDY > div.ng0pvUVS > div.cBiJe2DK > ul ')
    print(lis)
    for li in lis:
        href = li.find_element_by_css_selector('a').get_attribute('href')
        img=li.find_element_by_css_selector('img')
        imgsrc=img.get_attribute("src")
        title=img.get_attribute('alt')
        print(href,title,imgsrc)
        #单个视频采集
        getDuyin(href,title,imgsrc)


#获取当前日期
def get_now_time():
    """
    获取当前日期时间
    :return:当前日期时间
    """
    now =  time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    return now_time


#单元测试
#src = '百坭老黄：这算不算损友😂？@抖音小助手 #我太难了😂 #搞笑 #幽默搞笑 #农村搞笑段子 #意不意外 #搞笑视频'
#result_md5_value = get_md5_value(src.encode("utf-8"))
#result_sha1_value = get_sha1_value(src.encode("utf-8"))
#print(result_md5_value)
#print(result_sha1_value)

#x='e:\Desktop\视频发布\M灵梦🍋：#不眨眼vlog #美女 #cosplay #二次元 .mp4'
#print(x.split("\\")[-1])
#open('push_log.txt', mode ='a+',encoding="utf-8").write(str(get_now_time()+" 成功上传 "+"我爱你.mp4\n"))
#file_handle = open('push_log.txt', mode ='a+',encoding="utf-8").write(str(get_now_time()+" 成功上传 "+"我爱你.mp4"))
#time.sleep(222)

batch_download_v(False)
#batch_download_v(True,'https://www.douyin.com/user/MS4wLjABAAAAOb1v4Y9IgeRdrVAlDgBSsLtCsuZX36gstiXststnLqo')


