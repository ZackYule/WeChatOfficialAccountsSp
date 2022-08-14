from playwright.sync_api import sync_playwright
import csv
import os
from loguru import logger
import sys

HEAD_V = True
SLOW_MO_V = 0
LOGGER_LEVEL = 'INFO'

logger.remove()
handler_id = logger.add(sys.stderr, level=LOGGER_LEVEL)

def csv_pipeline(item:dict, keyword:str, content_type:str, header:list[str]):
    base_dir = '结果文件' + os.sep + keyword
    file_path = base_dir + os.sep + keyword + content_type + '.csv'

    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
    if not os.path.isfile(file_path):
        is_first_write = 1
    else:
        is_first_write = 0
        
    if item:
        with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if is_first_write:
                if header:
                    writer.writerow(header)
            writer.writerow([item[key] for key in item.keys()])

def process():
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch(headless=HEAD_V, slow_mo = SLOW_MO_V)
        context = browser.new_context(viewport={ 'width': 1440, 'height': 860 })
        page = context.new_page()
        page.goto("https://mp.weixin.qq.com/s/Ka-qRV7q4UI5BMqDWUoOag")

        a_loc_list = page.locator("//div[@id='js_content']//section[@data-id]//a")

        for i in range(a_loc_list.count()):
            logger.debug(a_loc_list.nth(i).get_attribute('href'))
            logger.debug(a_loc_list.nth(i).inner_text())
            # item = {"title":a_loc_list.nth(i).inner_text(),"url":a_loc_list.nth(i).get_attribute('href')}
            # csv_pipeline(item, '首届全国高校思想政治理论课教学展示活动获奖教学视频汇编', '入口链接', item.keys())
            page_video = context.new_page()
            page_video.goto(a_loc_list.nth(i).get_attribute('href'))
            logger.info('开始新的一页🌶🌶🌶🌶🌶🌶🌶🌶')
            # button_list = page_video.locator("//button[@class='mid_play_box reset_btn']")
            # for i in range(button_list.count()):
            #     button_list.nth(i).click()
            
            # button_list = page_video.locator("//div[@class='poster_cover']")
            # for i in range(button_list.count()):
            #     item = {"url":button_list.nth(i).get_attribute('style')}
            #     csv_pipeline(item, '视频合集', 'url', item.keys())
            video_list = page_video.locator("//video")
            for i in range(video_list.count()):
                item = {"title":a_loc_list.nth(i).inner_text(), "url":video_list.nth(i).get_attribute('src')}
                logger.info('爬取成功！！！！！！！！！')
                csv_pipeline(item, '视频合集', 'url', item.keys())


# //div[@id='js_content']//section[@data-id]//a
if __name__ == "__main__":
    process()