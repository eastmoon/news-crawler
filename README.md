# 新聞網站內容擷取 ( news-crawler )

本專案是基於爬蟲 ( Crawler ) 工具對目標網站取得指定搜尋的資訊，其主要完成擷取功能如下：

+ 列表擷取
以目標網站的搜尋引擎抓取目標關鍵字列表中的網站內容清單。

+ 內文解析
基於內容清單中的新聞頁面擷取文字資訊並轉成

由於專案內文解析使用 [Sanga](https://github.com/allenyummy/Sanga/blob/master/README.md)，但並非所有網站皆可使用，對此以 Template 設計模式撰寫 [NewsBaseClass](./src/news/base.py)，並提供諸如 ```list_search_url```、```list_capture```、```page_capture``` 等函數供繼承物件替換各自的執行細節，主程式則會宣告繼承物件後執行 ```capture``` 函數來進行內容擷取。

此外，基於對象網站本身設計方式不同，對於搜尋列表與解析內容方式各額外處理如下：

| 新聞網 | 列表擷取 | 內文解析 |
| -- | -- | -- |
| [自由時報 (ltn)](./src/news/ltn.py) | Crawler | Sanga |
| [中國時報 (chinatimes)](./src/news/chinatimes.py) | Crawler | Sanga |
| [工商時報 (ctee)](./src/news/ctee.py) | API | Sanga |
| [聯合報 (udn)](./src/news/udn.py) | API | Sanga |
| [經濟日報 (moneyudn)](./src/news/moneyudn.py) | API | [Customization](./src/news/pages/moneyudn.py) |

## 擷取操作

+ 修改搜尋關鍵字

請至專案目錄 ```src/keyword``` 文件內輸入欲搜尋的關鍵字

+ 新聞擷取

```
capture.bat
```

若執行時出現文字描述 ```Page crawler error when capture link with https://<news_address>```，則表示該則新聞的內容現有內文解析無法處理，需要額外撰寫客制化模塊。

## 開發模式

+ 進入環境

```
dev.bat
```

+ 模組單元測試

```
PYTHONPATH=. python news/<module>
```
> [How to import local modules with Python](https://fortierq.github.io/python-import/)，由於 Python 執行時的路徑規範，若使用 PYTHONPATH 將無法正確指向模組所在位置

+ 執行爬蟲主程式

```
python main.py
```

## Reference

+ [Request](https://requests.readthedocs.io/en/latest/)
+ [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
+ [Sanga](https://github.com/allenyummy/Sanga/blob/master/README.md)
