# 中國時報搜尋網站並無 API，採用 SRE 後端渲染搜尋結果頁面
# 網址：https://www.chinatimes.com/search/<keyword>

# Import library
import re
import requests
from bs4 import BeautifulSoup
from news.base import NewsListStruct
from news.base import NewsBaseClass

# Declare Class
class Crawler(NewsBaseClass):
    def __init__(self):
        super(Crawler, self).__init__("chinatimes")

    def list_search_url(self, keyword):
        return "https://www.chinatimes.com/search/{0}".format(keyword)

    def list_capture(self, url):
        result=[]
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                " AppleWebKit/605.1.15"
                " (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            },
        )

        if r.status_code == 200 and "text/html" in r.headers['content-type']:
            soup = BeautifulSoup(r.text, 'html.parser')
            lists = soup.find("section", attrs={'class':'search-result'}).find("div", attrs={'class':'item-list'})
            if lists != None:
                for item in lists.find_all("h3", attrs={'class':'title'}):
                    title = item.a.string
                    link = re.sub('\?.*', '', item.a["href"])
                    result.append(NewsListStruct(title, link))
            else:
                print("[Error] lists body not exist.")
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
