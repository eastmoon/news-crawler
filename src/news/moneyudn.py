# 經濟日報採用 WebAPI 取得資訓在前端渲染畫面；但其渲染內容已經由後端完成並由 WebAPI 回傳
# 網址：https://money.udn.com/search/ajax_result/1001/<keyword>/1/

# Import library
import re
import requests
from bs4 import BeautifulSoup
from news.base import NewsListStruct
from news.base import NewsBaseClass
from news.pages.moneyudn import MoneyUdn

# Declare Class
class Crawler(NewsBaseClass):
    def __init__(self):
        super(Crawler, self).__init__("moneyudn")

    def list_search_url(self, keyword):
        return "https://money.udn.com/search/ajax_result/1001/{0}/1/".format(keyword)

    def list_capture(self, url):
        result=[]
        r = requests.get(
            url
        )
        if r.status_code == 200 and "application/json" in r.headers['content-type']:
            soup = BeautifulSoup(r.json()["news_list"], 'html.parser')
            for item in soup.find_all("div", attrs={'class':'story__content'}):
                title = item.h3.get_text().replace('<[*> ', '')
                link = re.sub('\?.*', '', item.a["href"])
                result.append(NewsListStruct(title, link))
        return result
    # Use customer page crawler
    def page_capture(self, link, hash):
        # Declare variable
        crawler = MoneyUdn()
        self.page2file(crawler, link, hash)

# Execute script
if __name__ == '__main__':
    c = Crawler()
    r = c.list_capture(c.list_search_url("台化"))
    c.list2cache(r)
    r = c.cache2list(c.get_capture_day())
    for line in r:
        t = line.split(",")
        c.page_capture(t[1], t[0])
