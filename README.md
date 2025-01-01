# bili-reptile

**bili-reptile** 是一个Python编写的Bilibili收藏夹爬虫工具，旨在帮助用户自动下载收藏夹中的视频，避免因视频失效而丢失内容。该工具支持定时启动，确保用户不错过任何想要下载的视频。

## 功能特点

- **自动下载**：自动检测收藏夹中的视频，并下载到本地。
- **定时任务**：支持设置定时任务，定期检查和下载视频。
- **视频合成**：下载的视频和音频将被合并为一个完整的视频文件。

## 环境要求

- Python环境：需要Python解释器。
- 依赖库：以下是项目所需的Python依赖库及其具体版本。

## 安装指南

1. **安装Python**：确保您的系统已安装Python。
2. **安装依赖库**：通过运行以下命令安装所需的Python库：
   ```bash
   pip install -r requirements.txt
   ```

   以及其他项目依赖。

3. **安装FFmpeg**：FFmpeg是一个强大的多媒体框架，用于处理视频和音频文件。请根据您的操作系统安装FFmpeg，并确保它在系统的PATH变量中。

## 使用方法

1. **配置文件**：确保`data_mid.json`和`data_lst_id.json`文件包含正确的B站作者ID和收藏夹ID。
2. **运行程序**：运行`main.py`文件启动爬虫。
3. **定时任务**：程序默认每5秒检查一次新视频，您可以根据需要调整时间间隔。

## 文件说明

- `download_main.py`：负责下载视频和音频，并使用FFmpeg合成视频。
- `main.py`：主程序，负责定时检查新视频并调用`download_main.py`下载。
- `data_mid.json`：存储B站作者ID的JSON文件。
- `data_lst_id.json`：存储收藏夹ID的JSON文件。
- `data_histo.json`：存储已下载视频的BV号的JSON文件。

## 贡献与反馈

如果您有任何问题或建议，请通过GitHub Issues反馈。也非常欢迎贡献代码，共同改进这个项目。


