# Judgement Crawler

這是一個使用Python和Selenium寫的網路爬蟲程式,用於自動從台灣司法院網站下載指定條件的判決書。

## 功能

- 根據關鍵字、法院名稱和判決類型搜尋判決書
- 下載過去20年內符合條件的所有判決書
- 將下載的判決書以文字檔格式存儲在本地資料夾中

## 使用方式

1. 確保您的系統已安裝Python和必要的套件(`seleniumbase`)。
2. 呼叫`get_all_judgement_page`方法並提供搜尋關鍵字、法院名稱和判決類型作為參數。

## 用法範例
```python
JudgementScrawler = JudgementScrawler()
JudgementScrawler.get_all_judgement_page(search_str="關鍵字", court_name='法院名稱', judgement_type='判決類型')
```
程式將自動下載符合條件的判決書並儲存在judgement_docs資料夾中。

##注意事項
程式會開啟實體瀏覽器視窗進行操作,請勿關閉該視窗。
下載大量判決書可能需要較長時間,請耐心等待。
請確保您有權下載和使用這些判決書資料。

## 要求
* Python 3.x
* Seleniumbase
