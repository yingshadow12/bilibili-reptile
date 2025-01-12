import json
import re
import os
import requests
from lxml import etree

# 读取headers
with open('data_headers_.json', 'r') as f:
    headers_ = json.load(f)

# 读取历史文件
with open('data_old_video.json','r') as f:
    old_video = json.load(f)

# collected 我追的合集/收藏夹
# created 用户我创建的收藏夹

# 用户我创建的收藏夹
## 读取data_users_created_mid.json文件
### 获取用户mid
with open('data_users_created_mid.json', 'r') as f:
    users_created_mid_list = json.load(f)

## 检查用户mid是否为空
if not users_created_mid_list:
    print("data_users_created_mid.json文件为空")
else:
## for循环每个用户的收藏夹URL
## 为每个mid构建收藏夹URL
    for users_created_mid in users_created_mid_list:
        favorites_url = f"https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={users_created_mid}&web_location=333.1387"
        print(f"用户创建的收藏夹URL:", favorites_url)
        
        ## 请求'用户创建的收藏夹'列表
        data = requests.get(url=favorites_url,headers=headers_)
        data = json.loads(data.text)

        ## 获取'用户创建的收藏夹'中'收藏夹'列表
        favorites_list = data.get('data', {}).get('list', [])

        # 遍历列表并打印每个收藏夹的id,fid
        for favorite in favorites_list:
            print('收藏夹fid:',favorite.get('id'))
            favorite_id = str(favorite.get('id'))
            ### favorite_id也是收藏夹的fid

            ''' 收藏夹的fid调用api：：
            完整链接https://api.bilibili.com/x/v3/fav/resource/list?media_id=2542724062&pn=1&ps=40&keyword=&order=mtime&type=0&tid=0&platform=web
            花括号内为变量"<收藏夹fid,也是变量"favorite_id">"https://api.bilibili.com/x/v3/fav/resource/list?media_id={fid}&pn=1&ps=40&keyword=&order=mtime&type=0&tid=0&platform=web
            
            https://space.bilibili.com/<用户mid>/favlist?fid=<收藏夹fid,也是变量"favorite_id">&ftype=create
            '''

            # urls = []
            # urls.append(url)
            ## 拼接收藏夹网址
            favorite_url = "https://api.bilibili.com/x/v3/fav/resource/list?media_id=" + favorite_id + "&pn=1&ps=40&keyword=&order=mtime&type=0&tid=0&platform=web"
            
            ## 请求收藏夹列表地址
            favorite_data = requests.get(url=favorite_url,headers=headers_)

            ## 内容
            favorite_data = favorite_data.text

            ## pattern = r'"bvid":"(.+?)"'，这个模式用于匹配形如 "bvid":"某个BV号" 的字符串，其中 .+? 是一个非贪婪匹配，它会匹配尽可能少的字符。
            pattern = r'"bvid":"(.+?)"'

            # 找出收藏夹里的所有视频bvid
            ## 使用 pattern 定义的正则表达式模式，在 favorite_data 字符串中找到所有匹配的子串:'bvid'，并将这些子串存储在 bvid_match_data 列表中
            bvid_match_data = re.findall(pattern, favorite_data)
            print("抓取到的视频：" + ", ".join(bvid_match_data))
            print("抓取到的视频有",len(bvid_match_data),"个")

            # 算出新视频，需要下载的视频
            bvid_match_data = list(set(bvid_match_data) - set(old_video))
            print("新的的视频：" + ", ".join(bvid_match_data))
            print("新的的视频有",len(bvid_match_data),"个")

        # 获取b站视频内容
            # 遍历bvid,为每个bvid进行操作
            for bvid in bvid_match_data:
                ## 拼接b站网址
                url = 'https://www.bilibili.com/video/' + bvid + '/?spm_id_from=333.999.0.0&vd_source=9c14dbce18e4fe2de7a5bb9fef5e8422'
                
                ## 请求,转换
                bili_data = requests.get(url,headers=headers_)
                bili_data = bili_data.text

                ## 转换类型，获取视频名称
                html_obj = etree.HTML(bili_data)
                title_name = html_obj.xpath('//title/text()')[0]
                title_name = re.sub(r'[\\/*?:"<>| ]', '_', title_name)  #### 替换特殊字符
                # title_name = bvid + '_' + title_name  # 在文件名字前加上bvid
                if title_name == '视频去哪了呢？_哔哩哔哩_bilibili':
                    print(bvid,"视频已删除")
                    with open(f"{bvid} 此视频已删除.txt","w") as f:
                        print(f"{bvid}此视频已删除\n{url}",file=f)
                    continue  
                # title_name = re.sub(r'[_哔哩哔哩_bilibili]', '', title_name)  #### 替换bilibili


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
                            
            # 旧视频加新视频，已经下载过的视频
            old_video = old_video + bvid_match_data

            # 写入已下载的视频bvid
            with open('data_old_video.json', 'w') as f:
                json.dump(old_video, f)