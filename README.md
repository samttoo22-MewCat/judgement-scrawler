# Judgement Crawler

這是一個使用 Python 和 SeleniumBase 寫的網路爬蟲程式，用於自動從台灣司法院網站下載指定條件的判決書。

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
**法院名稱** 可以是: 司法院刑事補償法庭、
最高法院、臺灣高等法院、智慧財產及商業法院、臺灣高等法院 臺中分院、臺灣高等法院 臺南分院、臺灣高等法院 高雄分院、臺灣高等法院 花蓮分院、臺灣臺北地方法院、臺灣士林地方法院、臺灣新北地方法院、臺灣宜蘭地方法院、臺灣基隆地方法院、臺灣桃園地方法院、臺灣新竹地方法院、
臺灣苗栗地方法院、臺灣臺中地方法院、臺灣彰化地方法院、臺灣南投地方法院、臺灣雲林地方法院、臺灣嘉義地方法院、臺灣臺南地方法院、臺灣高雄地方法院、臺灣橋頭地方法院、臺灣花蓮地方法院、臺灣臺東地方法院、臺灣屏東地方法院、臺灣澎湖地方法院、福建高等法院金門分院、福建金門地方法院、福建連江地方法院。<br>法院名稱一次只能選一個，如果不填就是搜尋全部。<br><br>
**判決類型** 可以是: 憲法、民事、刑事、行政、懲戒。<br>判決類型可多選，類型間用空格隔開，如果不填則會搜尋全部。<br><br>
程式將自動下載符合條件的判決書並儲存在 judgement_docs 資料夾中。

## 注意事項
程式會開啟實體瀏覽器視窗進行操作，請勿關閉該視窗。</br>
下載大量判決書可能需要較長時間，請耐心等待。</br>

## 要求
* Python 3.x
* Seleniumbase
