import re
import os
import requests
from lxml import etree
import subprocess  # 导入subprocess模块

def down_func(url_1):
    headers_ = {
        'Cookie': '''按f12进入开发者模式后网络中web开头的文件下有cookie，替换这行文字，放在两端的三个点中间''',
        'Referer': 'https://search.bilibili.com/',
        'User-Agent': '按f12进入开发者模式后网络中web开头的文件下有User-Agent，替换这行文字，放在两端的三个点中间',
    }
    
# 获取b站视频内容
    response_ = requests.get(url_1,headers=headers_)
    data_ = response_.text

###转换类型，获取视频名称
    html_obj = etree.HTML(data_)
    title_name = html_obj.xpath('//title/text()')[0]
    title_name = re.sub(r'[\\/*?:"<>| ]', '_', title_name)  # 替换特殊字符
    # title_name = re.sub(r'[_哔哩哔哩_bilibili]', '', title_name)  # 替换bilibili

    #title_name = deal_special_words(title_name)##视频名称乱码下载不了，需要替换乱码

#提取url，合成视频
    url_str = html_obj.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"',url_str)[0]
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', url_str)[0]

    # headers = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    #     "referer": video_url
    # }

#发送请求，获取响应
    print('\n','~'*100)
    print('视频名是:',title_name)

    # print('开始获取.mp4')
    response_video = requests.get(video_url,headers=headers_)

    # print('开始获取.mp3')
    response_audio = requests.get(audio_url,headers=headers_)

#下载并重命名
    data_video = response_video.content
    data_audio = response_audio.content

    print('开始下载.mp4')
    with open('video.mp4', 'wb') as f:
        f.write(data_video) 
   
    print('开始下载.mp3')
    with open('audio.mp3', 'wb') as f:
        f.write(data_audio)

    print('~'*100)

#将下载路径转移到指定文件夹
    input_file = 'video.mp4'
    output_dir = r'E:\Program Files\project\my\my_bilibili-reptile'#####你想要的下载路径，自己设置

# 构建输出文件的完整路径
    output_file = os.path.join(output_dir, f'{title_name}.mp4')

    print('\n','~'*100)
    print('开始合成视频')

### 使用subprocess运行ffmpeg命令并捕获输出和错误
    # 运行ffmpeg命令
    command = f'ffmpeg -i "{input_file}" -i "audio.mp3" -c copy "{output_file}"'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 打印输出和错误
    print(result.stderr.decode())

    # 假设 ffmpeg_output 是你的 ffmpeg 命令的输出字符串
    ffmpeg_output = result.stderr.decode()# stddrr [out#

    # 检查输出中是否包含 "[out"
    if "[out" in ffmpeg_output:
        print("成功")
    else:
         print("失败")
    # 检查命令是否成功执行
    # if result.returncode == 0:
    #     print("FFmpeg 命令执行成功")
    # else:
    #     print("FFmpeg 命令执行失败，错误码:", result.returncode)

    print('结束合成视频')
    print('~'*50)

    # 删除临时视频
    os.remove("video.mp4")
    os.remove("audio.mp3")