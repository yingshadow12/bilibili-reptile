import re
import time
import requests
import schedule
import os
from lxml import etree
import json

# 设置每隔 多少 秒钟执行一次
s = 5

print("bilibili指定视频自动化收割机启动，收割时间间隔为",s,'s')
def Automatic_harvester():

    # 读取json文件
    # with open('data_mid.json') as f:
    #     up_ids = json.load(f)
    
    # 收藏夹fid处理
    with open('data_lst_id.json') as f:
        favorites_ids = json.load(f)
    
    # 读取headers
    with open('data_headers_.json', 'r') as f:
        headers_ = json.load(f)    

    # print('mid',up_ids)
    # print('收藏夹fid',favorites_ids)

    # 遍历每个uid和mid，拼接API URL并添加到urls数组中
    urls = []
    # 用户的mid调用api：：https://api.bilibili.com/x/space/wbi/arc/search?mid=1563751305&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=44eb867d57fdaa28154beb09954311ce&wts=1698298141
    # for mid in up_ids:
    #     url = "https://api.bilibili.com/x/space/wbi/arc/search?mid=" + mid + "&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=44eb867d57fdaa28154beb09954311ce&wts=1698298141"
    #     urls.append(url)

    # 收藏夹的fid调用api：：https://api.bilibili.com/x/v3/fav/resource/list?media_id=2542724062&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web
    for fid in favorites_ids:
        url = "https://api.bilibili.com/x/v3/fav/resource/list?media_id=" + fid + "&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web"
        urls.append(url)

        # 收藏夹列表地址: urls

        for api_url in urls:
            # 查看曾经下载过的视频
            with open('data_histo.json', 'r') as f:
                downloaded_bvids = json.load(f)
            # 输出
            print('已下载过的视频:', ', '.join(downloaded_bvids))

            # 请求收藏夹列表地址
            response_ = requests.get(api_url, headers=headers_)
            print('收藏夹列表地址:',api_url)

            # 内容
            text = response_.text

            # pattern = r'"bvid":"(.+?)"'，这个模式用于匹配形如 "bvid":"某个BV号" 的字符串，其中 .+? 是一个非贪婪匹配，它会匹配尽可能少的字符。
            pattern = r'"bvid":"(.+?)"'

            # 收藏夹里的所有视频bvid
            # 使用 pattern 定义的正则表达式模式，在 text 字符串中找到所有匹配的子串:'bvid'，并将这些子串存储在 bvid_match_data 列表中
            bvid_match_data = re.findall(pattern, text)
            # print("抓取到的松果位置：" + ", ".join(bvid_match_data))
            print("抓取到的视频：" + ", ".join(bvid_match_data))

            # 比较两组数据，输出不同的数据
            # 检测'现收藏夹'比'下载过的'多的视频
            diff = list(set(bvid_match_data) - set(downloaded_bvids))

            # print("新松果位置" + ", ".join(diff))
            print("新视频" + ", ".join(diff))
            print('='*100)
            data1 = downloaded_bvids + diff
            for bvid in diff:
                url = 'https://www.bilibili.com/video/' + bvid + '/?spm_id_from=333.999.0.0&vd_source=9c14dbce18e4fe2de7a5bb9fef5e8422'
                    
                ## 请求,转换
                bili_data = requests.get(url,headers=headers_)
                bili_data = bili_data.text

                ## 转换类型，获取视频名称
                html_obj = etree.HTML(bili_data)
                title_name = html_obj.xpath('//title/text()')[0]
                title_name = re.sub(r'[\\/*?:"<>| ]', '_', title_name)  #### 替换特殊字符
                # title_name = bvid + '_' + title_name  # 在文件名字前加上bvid
                # title_name = re.sub(r'[_哔哩哔哩_bilibili]', '', title_name)  #### 替换bilibili
                if title_name == '视频去哪了呢？_哔哩哔哩_bilibili':
                    print(bvid,"视频已删除")
                    with open(f"{bvid} 此视频已删除.txt","w") as f:
                        print(f"{bvid}此视频已删除\n{url}",file=f)
                    continue  


                ## 提取url，合成视频
                url_str = html_obj.xpath('//script[contains(text(),"window.__playinfo__")]/text()')[0]
                video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)"',url_str)[0]
                audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)"', url_str)[0]

                print('视频名是:',title_name)
                print('bvid是:',bvid)

                # 发送请求，开始下载
                print('开始获取.mp4')
                
                response_video = requests.get(video_url,headers=headers_)

                print('开始获取.mp3')
                response_audio = requests.get(audio_url,headers=headers_)

                data_video = response_video.content
                data_audio = response_audio.content


                with open('video.mp4', 'wb') as f:
                    f.write(data_video) 

                with open('audio.mp3', 'wb') as f:
                    f.write(data_audio)
                
                # 输入要保存的位置,默认当前目录
                output_dir = './'#####你想要的下载路径，自己设置

                # 构建输出文件的完整路径
                output_file = os.path.join(output_dir, f'{title_name}.mp4')

                print('\n','~'*100)
                print('开始合成视频')

                os.system(f'ffmpeg -i "video.mp4" -i "audio.mp3" -c copy "{output_file}"')

                # 删除临时视频
                os.remove("video.mp4")
                os.remove("audio.mp3")
            ###如果收藏夹删除了以前视频，data_histo不会缺失数据
            with open('data_histo.json', 'w') as f:
                json.dump(data1, f)


        print("采集过的位置列表已更新")
        print("任务完成，自动化收割机已休眠，5s后进行下一次采集")
        print('-'*100,"\n")
if __name__ == '__main__':
    # 设置定时任务，每隔 5 秒钟执行一次 Automatic_harvester 函数，需要的可以设为3600秒（一小时运行一次）
    schedule.every(s).seconds.do(Automatic_harvester)
    

    # 循环执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)
