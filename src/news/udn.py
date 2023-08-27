# 聯合報採用 WebAPI 取得資訓在前端渲染畫面；其 API 來源於下拉式展開內容的 API
# API : https://udn.com/api/more?page=1&id=search:<keyword>&channelId=2&type=searchword&last_page=50

# Import library
import re
import requests
from bs4 import BeautifulSoup
from news.base import NewsListStruct
from news.base import NewsBaseClass

# Declare Class
class Crawler(NewsBaseClass):
    def __init__(self):
        super(Crawler, self).__init__("udn")

    def list_search_url(self, keyword):
        return "https://udn.com/api/more?page=1&id=search:{0}&channelId=2&type=searchword&last_page=50".format(keyword)

    def list_capture(self, url):
        result=[]
        r = requests.get(
            url
        )
        if r.status_code == 200 and "application/json" in r.headers['content-type']:
            lists = r.json()["lists"]
            for item in lists:
                title = item["title"]
                link = re.sub('\?.*', '', item["titleLink"])
                result.append(NewsListStruct(title, link))
        return result

# Execute script
if __name__ == '__main__':
    c = Crawler()
    r = c.list_capture(c.list_search_url("台化"))
    c.list2cache(r)
    r = c.cache2list(c.get_capture_day())
    for line in r:
        t = line.split(",")
        c.page_capture(t[1], t[0])
