import requests
import time
import json
from pyquery import PyQuery as pq




# 设置头部
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.bilibili.com',
    'Referer': 'https://www.bilibili.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    
}


# 返回视频相关信息
def get_data(aid):
    try:
        url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + str(aid)
        req = requests.get(url)
        if req.status_code == 200:
            return req.json()
    except requests.ConnectionError as e:
        print('Error', e.args)



# 返回视频标题
def get_title(aid):
    url = 'https://www.bilibili.com/video/av' + str(aid)
    try:
        req = requests.get(url, headers=headers).text
        q = pq(req)
        title = q('#viewbox_report h1 span').text()
        return title
    except:
        pass


# 解析数据并保存到本地
def parse_get_data(html, title):
    if html:
        try:
            print('解析数据')
            data = html['data']
            if data['view'] != "--" and data['aid'] != 0:
                video = [{
                    'aid':      data['aid'],            # 视频编号
                    'view':     data['view'],           # 播放量
                    'danmaku':  data['danmaku'],        # 弹幕数
                    'reply':    data['reply'],          # 评论数
                    'favorite': data['favorite'],       # 收藏数
                    'coin':     data['coin'],           # 硬币数
                    'share':    data['share'],          # 分享数
                    'title':    title                   # 视频标题名称
                }]
                if video:
                    print('保存数据中~')
                    with open('bili_video_spider\\video.json', 'a', encoding='utf-8') as fi:
                        fi.write(json.dumps(video, indent=2, ensure_ascii=False))
                        fi.close()
                        print('保存成功')
                
        except:
            pass

def main(aid):
    # 获取data
    html = get_data(aid)    
    print(html)
    time.sleep(1)       # 延迟
    # 获取视频标题
    title = get_title(aid)
    print(title)
    # 传递数据进行解析
    parse_get_data(html, title)


if __name__ == '__main__':
    for i in range(1, 2018):
        begin = 10000 * i
        for j in range(begin, begin + 10000):
            main(j)
            time.sleep(1)
