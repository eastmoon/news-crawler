# Import library
import json
import logging
from bs4 import BeautifulSoup
from Sanga.media.base import BaseMediaNewsCrawler
from Sanga.struct import NewsStruct
from typing import Dict, Union, List

# Declare logger
logger = logging.getLogger(__name__)

# Declare Class
class MoneyUdn(BaseMediaNewsCrawler):
    """Web Crawler for MoneyUDN News"""

    def getInfo(self, link: str) -> NewsStruct:
        return super().getInfo(link)

    @staticmethod
    def _get_content(
        soup: BeautifulSoup,
    ) -> str:

        content_list = soup.find("section", id="article_body").find_all("p")
        content = "\n".join([c.text for c in content_list])
        logger.debug(f"CONTENT:\n {content}")
        return content
        #return "Test Content"

# Execute script
if __name__ == '__main__':
    c = MoneyUdn()
    n = c.getInfo(link="https://money.udn.com/money/story/7307/6494942")
    print(n)
