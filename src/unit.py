import time
import re
import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import subprocess
import requests
from urllib.parse import unquote

# 设置 WebDriver
service = Service('./chromedriver-mac-arm64/chromedriver')  # 替换为实际的 chromedriver 路径
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

def add_network_listener(driver,Url=None):
    url = 'https://www.douyin.com/video/7390630835755453715'
    if Url:
        url = Url
    driver.get(url)
    time.sleep(45)
    requests = driver.requests
    video_requests = [r for r in requests if r.method == 'GET' and r.response and 'Content-Type' in r.response.headers and r.response.headers['Content-Type'] == 'video/mp4' and not r.path.endswith('.mp4')]
    video_urls = [r.url for r in video_requests]
    return video_urls

# add_network_listener(driver)

def download_video(video_url):
    url = 'https://www.douyin.com/video/7390630835755453715'
    if video_url:
        url = video_url
    decoded_url = unquote(url)
    
    output_file = "output_video_test.mp4"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://v3-web.douyinvod.com/8c82b308c317ee45190ca7e7299ff295/66d19e72/video/tos/cn/tos-cn-vd-0026/o8fmo09EANDkBhzErfFl4RAvAwABAgBwM3ADWA/media-video-hvc1/?a=6383&ch=0&cr=8&dr=0&er=1&lr=default&cd=0%7C0%7C0%7C3&cv=1&br=892&bt=892&cs=4&ds=6&mime_type=video_mp4&qs=11&rc=ZjM6M2Q6Omg1NTY4aTY0PEBpM3U2anI5cnhmdDMzNGkzM0BfX142YF9eX2AxXy0zLl8yYSNwaDEyMmQ0ZjVgLS1kLTBzcw%3D%3D&btag=c0000e00030000&cquery=100o_100w&dy_q=1724926640&l=2024082918172043A6705995FB8407EC10',  # 替换为实际的 Referer
    'Connection': 'keep-alive',
    'sec-ch-ua-platform':"macOS"
    }
    ffmpeg_command = [
    'ffmpeg',
    '-headers', ';'.join(headers),
    '-i', decoded_url,
    '-c', 'copy',
    output_file
]
    response_mp4 = requests.get(url=decoded_url, headers=headers).content
    with open('test.mp4', mode='wb') as f:
        f.write(response_mp4)
    # subprocess.run(ffmpeg_command)
    print(f"视频已保存到 {output_file}")

video = 'https://v3-web.douyinvod.com/8c82b308c317ee45190ca7e7299ff295/66d19e72/video/tos/cn/tos-cn-vd-0026/o8fmo09EANDkBhzErfFl4RAvAwABAgBwM3ADWA/media-video-hvc1/?a=6383&ch=0&cr=8&dr=0&er=1&lr=default&cd=0%7C0%7C0%7C3&cv=1&br=892&bt=892&cs=4&ds=6&mime_type=video_mp4&qs=11&rc=ZjM6M2Q6Omg1NTY4aTY0PEBpM3U2anI5cnhmdDMzNGkzM0BfX142YF9eX2AxXy0zLl8yYSNwaDEyMmQ0ZjVgLS1kLTBzcw%3D%3D&btag=c0000e00030000&cquery=100o_100w&dy_q=1724926640&l=2024082918172043A6705995FB8407EC10'
download_video(video)