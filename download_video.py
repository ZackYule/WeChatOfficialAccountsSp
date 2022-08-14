from asyncio.log import logger
import requests
import hashlib
import os
import csv
from loguru import logger
import sys

LOGGER_LEVEL = 'INFO'

logger.remove()
handler_id = logger.add(sys.stderr, level=LOGGER_LEVEL)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Host": "mpvideo.qpic.cn",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

def download_video(url, name, path=""):
    hl = hashlib.md5()
    try:
        logger.debug('准备下载视频:'+url)
        response=requests.get(url,headers=headers)
        data=response.content
        if not path:
            path = os.getcwd()
        if data:
            file_path='{}/{}.{}'.format(path, name, 'mp4')
            logger.info('文件为:'+file_path)
            if not os.path.exists(file_path):
                with open(file_path,'wb')as f:
                    f.write(data)
                    f.close()
                    print('视频下载成功:'+url)
    except Exception:
        logger.warning('视频下载失败')
        logger.warning(Exception)

def get_content_info_from_csv(title:str, content_type:str)->list[dict]:
    base_dir = '结果文件' + os.sep + title
    file_path = base_dir + os.sep + title + content_type + '.csv'

    if not (os.path.isdir(base_dir) |  os.path.isfile(file_path)):
        return []
    
    items = []
    with open(file_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)
    return items

if __name__ == "__main__":
    items = get_content_info_from_csv('视频合集', 'url')
    path = '/Volumes/vvv/video'
    for i, item in enumerate(items):
        logger.info(f'第{i+1}个视频下载中......')
        download_video(item['url'], item['title']+str(i), path)
    # download_video("http://mpvideo.qpic.cn/0bf2yiaakaaawmamrmmeanqfbqwdaxbaabia.f10002.mp4?dis_k=2577673c4ba14662c55aafb1f4a1f480&dis_t=1660448010&vid=wxv_1840860069756796938&format_id=10002&support_redirect=0&mmversion=false")