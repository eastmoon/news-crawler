# Declare import library
from news import ctee
from news import ltn
from news import moneyudn

# Execute script
if __name__ == '__main__':
    crawler_arr = []
    crawler_arr.append(ctee.Crawler())
    crawler_arr.append(ltn.Crawler())
    crawler_arr.append(moneyudn.Crawler())
    keyword_filename="keyword"
    for crawler in crawler_arr:
        crawler.capture(keyword_filename)
