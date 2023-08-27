# library
import os.path
import glob
import re
import hashlib
from datetime import datetime
import Sanga

# Declare variable
DATA_DIR="/data"
APP_DIR="/app"

# Declare Class
class NewsListStruct:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.hash = self.__toHash(link)
    def __toHash(self, str):
        m = hashlib.md5()
        m.update(str.encode("utf-8"))
        return m.hexdigest()

class NewsBaseClass:
    # Constructure
    def __init__(self, news_name):
        self.__name = news_name
        self.__app_dir = APP_DIR
        self.__data_dir = DATA_DIR
        self.__news_dir = os.path.join(self.__data_dir, news_name)
        if not os.path.exists(self.__news_dir): os.makedirs(self.__news_dir)
        self.__list_dir = os.path.join(self.__news_dir, "list")
        if not os.path.exists(self.__list_dir): os.makedirs(self.__list_dir)
        self.__page_dir = os.path.join(self.__news_dir, "page")
        if not os.path.exists(self.__page_dir): os.makedirs(self.__page_dir)

    # Accessor
    def get_name(self):
        return self.__name
    def get_list_dir(self):
        return self.__list_dir
    def get_page_dir(self):
        return self.__page_dir
    def get_capture_day(self):
        return datetime.now().strftime("%Y-%m-%d")

    # Common method
    def capture(self, keyword_filename):
        with open(os.path.join(self.__app_dir, keyword_filename), 'r') as f:
            print("> {0} capture list".format(self.__name))
            for line in f:
                keyword = re.sub('\s+', '', line)
                print(">> capture keyword {1}".format(self.__name, keyword))
                r = self.list_capture(self.list_search_url(keyword))
                self.list2cache(r)
            print("> {0} capture pages".format(self.__name))
            for line in self.cache2list(self.get_capture_day()):
                self.page_capture(line.split(",")[1], line.split(",")[0])
    def list_search_url(self, keyword):
        return "{0}".format(keyword)
    def list_capture(self, url):
        return []
    def list2cache(self, res):
        ## Declare file
        filepath = os.path.join(self.get_list_dir(), self.get_capture_day())
        ## read all line in memory cache
        queries = ""
        if os.path.exists(filepath):
            f = open(filepath, "r+")
            queries = ",".join([l.strip() for l in f])
            f.close()
        ## open file for write new result
        f = open(filepath, "a+")
        for item in res:
            if item.hash not in queries:
                ## format string
                outstr = "{0},{1}".format(item.hash, item.link)
                #print(item.title)
                #print(outstr)
                ## write to file
                f.write("{0}\n".format(outstr))
                ## write to memory cache
                queries += ",{0}".format(outstr)
        f.close()
    def cache2list(self, time):
        ## Declare file
        filepath = os.path.join(self.get_list_dir(), self.get_capture_day())
        ## read all line from file
        result = []
        if os.path.exists(filepath):
            f = open(filepath, "r+")
            result = [l.strip() for l in f]
        return result
    def page_capture(self, link, hash):
        # Declare variable
        crawler = Sanga.create_crawler(media_name=self.__name)
        self.page2file(crawler, link, hash)
    def page2file(self, page_crawler, link, hash):
        os.chdir(self.get_page_dir())
        files = [ f.strip() for f in glob.glob("*-{0}.txt".format(hash)) ]
        # Capture page data
        if len(files) == 0:
            try:
                news = page_crawler.getInfo(link=link)
                filepath = os.path.join(self.get_page_dir(), "{0}-{1}-{2}.txt".format(news.datetime, news.title, hash))
                #filepath = os.path.join(self.get_page_dir(), hash)
                f = open(filepath, "w+")
                f.write("{0}-{1}\n".format(news.datetime, news.title))
                f.write("-----CONTENT-----\n")
                f.write(news.content)
                f.close()
                print("> {0}-{1}".format(news.datetime, news.title))
            except Exception:
                print("Page crawler error when capture link with {0}".format(link))
