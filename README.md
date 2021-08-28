# 91Pro视频下载的Python脚本

利用Python3，爬取网站上视频，整合成自用版本。
***
- 爬虫脚本在@guobaby <https://github.com/guobaby/91pron_python> 的基础上进行了修改，特此感谢。
- m3u8视频通过@anwenzen <https://github.com/anwenzen/M3u8Download> 的脚本直接下载，特此感谢.   
***  

* 支持m3u8格式与mp4格式视频下载.  
* 可过滤本地已有视频文件.  
* 生成的视频文件默认保留为：视频名_作者.mp4。
* 生成的视频文件按照日期进行分文件夹保存。
***

1. 安装python环境
2. 安装requests,bs4,tqdm包
3. 安装ffmpeg程序
4. 运行`download.py`
***
### 1. 安装Python依赖包
```
    pip install requests==2.20.0   
    pip install bs4
    pip install tqdm
```
### 2. 安装ffmpeg程序
&emsp;[Windows下安装使用ffmpeg](https://zhuanlan.zhihu.com/p/118362010)   
&emsp;[CentOS7安装ffmpeg](https://blog.csdn.net/qq_41494464/article/details/88654227)

### 3. 运行 `download.py`
##### &emsp;因访问91网站不翻墙速度较慢，请先将两个文件中的代理地址替换成本地代理地址。
```
proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'} # 代理地址`
```
##### &emsp;然后运行python文件。
```
    python dowmload.py
```
当输出以下文字时，视频已经保存在同级文件夹down中啦。
```
Start Working
############################################
[上月最热]第1页数据,共24条帖子 =>>>> 正在下载第1个帖子_abcdefghijklmn_xyz
[*************************](20/20)
############################################
```