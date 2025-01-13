import json
import re
import os
import requests
from lxml import etree

# 读取headers
with open('data_headers_.json', 'r') as f:
    headers_ = json.load(f)

# 输入bvid
bvids = input("请输入视频BVID,多个视频用英文逗号分割：")

# 将bvids字符串转换为列表
bvids = bvids.split(",")

for bvid in bvids:
    # 拼接url
    url_ = 'https://www.bilibili.com/video/' + bvid 

    # 发送请求
    response = requests.get(url=url_,headers=headers_)
    # 处理信息
    data_ = response.text

    ###转换类型，获取视频名称
    html_obj = etree.HTML(data_)
    title_name = html_obj.xpath('//title/text()')[0]
    # 替换特殊字符
    title_name = re.sub(r'[\\/*?:"<>| ]', '_', title_name)
    # title_name = bvid + '_' + title_name  # 在文件名字前加上bvid
    # 替换bilibili
    # title_name = re.sub(r'[_哔哩哔哩_bilibili]', '', title_name)  
    if title_name == '视频去哪了呢？_哔哩哔哩_bilibili':
        print(bvid,"视频已删除")
        with open(f"{bvid} 此视频已删除.txt","w") as f:
            print(f"{bvid}此视频已删除\n{url_}",file=f)
        exit()


    #提取url，合成视频
    url_str = html_obj.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"',url_str)[0]
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', url_str)[0]

    # 下载视频  
    print('视频名是:',title_name)

    print('开始获取.mp4')
    response_video = requests.get(video_url,headers=headers_)

    print('开始获取.mp3')
    response_audio = requests.get(audio_url,headers=headers_)

    # 提取视频数据
    data_video = response_video.content
    data_audio = response_audio.content

    # 保存视频和音频
    with open('video.mp4', 'wb') as f:
        f.write(data_video) 

    with open('audio.mp3', 'wb') as f:
        f.write(data_audio)

    # 输入要保存的位置,默认当前目录
    output_dir = './'
    output_file = os.path.join(output_dir, f'{title_name}.mp4')

    # 使用ffmpeg拼接视频和音频
    os.system(f'ffmpeg -i "video.mp4" -i "audio.mp3" -c copy "{output_file}"')

    # 删除临时视频
    os.remove("video.mp4")
    os.remove("audio.mp3")
