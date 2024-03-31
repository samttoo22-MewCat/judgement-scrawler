import asyncio
import os
from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import sys
import datetime
import re

class JudgementScrawler:
    def __init__(self):
        self.browser_executable_path = ""
        self.driver = Driver(disable_gpu=False,
                             agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36',
                             incognito=True,
                             #headless=True,
                             browser='chrome',
                             uc=True
                             )
        self.lock = asyncio.Lock()
        self.browser_executable_path = ""
        self.browser_executable_path = os.path.abspath("chromedriver.exe")
        self.wait = WebDriverWait(self.driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        
        self.driver.get('https://judgment.judicial.gov.tw/FJUD/default.aspx')
    
    def get_judgement_links_count(self, search_str, court_name):
        submit_button = self.driver.find_element(By.XPATH, '//input[@id="btnSimpleQry"]')
        search_input = self.driver.find_element(By.XPATH, '//input[@id="txtKW"]')
        search_input.send_keys(search_str)
        submit_button.click()
        
        list_href = self.driver.find_elements(By.XPATH, "//div[@id='collapseGrpCourt']/div[@class='panel-body']/ul/li")
       
        frame = self.driver.find_element(By.ID, "iframe-data")
        self.driver.switch_to.frame(frame)

        # 所有法院
        if(court_name == ''):
            pages = self.driver.find_element(By.ID, "plPager")
            pages = pages.get_attribute("textContent").split(" . ")[0].strip().split(" ")[1]
            return pages
        # 指定法院
        else:
            type = list_href.find_element(By.TAG_NAME, "a").get_attribute("textContent")
            print(type)
            if(court_name in type):
                list_href = list_href.find_element(By.TAG_NAME, "a").get_attribute("href")
        
        links_count = 0

        if(EC.visibility_of_element_located((By.XPATH, "//div[@id='plPager']"))):
            links = self.driver.find_element(By.XPATH, "//div[@id='plPager']/span").get_attribute("textContent")
            links = links.split(" . ")[0]
            links = links.split(" ")[1]
            return links
        else:
            links = self.driver.find_element(By.XPATH, "//table[@id='jud']/tbody/tr[@class='summery]")
            links = len(links)
            links_count += links
        return links_count
    
    def get_judgement_links(self, search_str, court_name, judgement_type):
        def get_month_days(year, month):
            normal_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            special_month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            year += 1911
            if(year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)):
                return special_month_days[month - 1]
            else:
                return normal_month_days[month - 1]
        
        def get_year_months(year):
            today = datetime.date.today()
            year_now = today.year - 1911
            month_now = today.month

            if(year == year_now):
                return month_now
            else:
                return 12
        
        def reset_input():
            self.driver.get('https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx')
            reset_button = self.driver.find_element(By.XPATH, '//button[@id="btnReset"]')
            reset_button.click()
            
        self.driver.get('https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx')
        judgement_links = []
        today = datetime.date.today()
        year_now = today.year - 1911
        month_now = today.month
        day_now = today.day
        
        #搜尋二十年
        month_break_count = 0
        for searching_year in range(year_now, year_now - 21, -1):
            #搜尋一整年中每個月的案件
            searching_months = get_year_months(searching_year)
            
            if(month_break_count > 12):
                month_break_count = 0
                break
            for searching_month in range(searching_months, 0, -1):
                print(f"開始抓取 {searching_year} 年度 {searching_month} 月的案件")
                self.wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@class="search-table"]/tbody/tr/td/label[@id="vtype_C"]')))
                submit_button = self.driver.find_element(By.XPATH, '//input[@id="btnQry"]')
                search_input = self.driver.find_element(By.XPATH, '//input[@id="jud_kw"]') 
                if(judgement_type != ''):
                    judgement_type = judgement_type.split(" ")
                    for j in judgement_type:
                        type_check = self.driver.find_element(By.XPATH, f'//table[@class="search-table"]/tbody/tr/td/label[text()="{j}"]')
                        type_check = type_check.find_element(By.TAG_NAME, 'input')
                        type_check.click()
                    
                #輸入搜尋條件
                from_year_input = self.driver.find_element(By.XPATH, '//input[@id="dy1"]')
                from_month_input = self.driver.find_element(By.XPATH, '//input[@id="dm1"]')
                from_day_input = self.driver.find_element(By.XPATH, '//input[@id="dd1"]')
                to_year_input = self.driver.find_element(By.XPATH, '//input[@id="dy2"]')
                to_month_input = self.driver.find_element(By.XPATH, '//input[@id="dm2"]')
                to_day_input = self.driver.find_element(By.XPATH, '//input[@id="dd2"]')
                
                month_days = get_month_days(searching_year, searching_month)
                
                from_year_input.send_keys(searching_year)
                to_year_input.send_keys(searching_year)
                
                from_month_input.send_keys(searching_month)
                to_month_input.send_keys(searching_month)
                
                from_day_input.send_keys(1)
                to_day_input.send_keys(month_days)
                
                search_input.send_keys(search_str)
                submit_button.click()
                
                result_count = self.driver.find_element(By.XPATH, "//div[@id='result-count']/ul/li/a/span")

                result_count = int(result_count.get_attribute("textContent"))
                if(result_count == 0):
                    print(f"沒有搜尋到 {searching_year} 年度 {searching_month} 月的案件。")
                    month_break_count += 1
                    reset_input()
                    continue
                else:
                    month_break_count = 0
                
                list_href = self.driver.find_elements(By.XPATH, "//div[@id='collapseGrpCourt']/div[@class='panel-body']/ul/li")
                
                
                # 所有法院
                if(court_name == ''):
                    list_href = self.driver.find_element(By.XPATH, "//*[@id='result-count']/ul/li/a").get_attribute("href")
                # 指定法院
                else:
                    type = list_href.find_element(By.TAG_NAME, "a").get_attribute("textContent")
                    if(court_name in type):
                        list_href = list_href.find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                #如果沒有這個法院的搜尋結果，就跳下一個月
                if(isinstance(list_href, list)):
                    reset_input()
                    break
                
                self.driver.get(list_href)
                
                #試圖抓取
                
                try:
                    pages = self.driver.find_element(By.XPATH, "//div[@id='plPager']/span").get_attribute("textContent")
                    pages = pages.split(" / ")[1].split(" ")[0]
                except:
                    pages = 1
                
                #在搜尋結果頁面中 拿到每個案件的連結
                for i in range(0, int(pages)):           
                    judgement_list = self.driver.find_elements(By.XPATH, "//table[@id='jud']/tbody/tr/td/a")
                    for j in judgement_list:
                        judgement_links.append(j.get_attribute("href"))
                    
                    #如果有下一頁就跳轉
                    #self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='plPager']")))
                    try:
                        next_page_button = self.driver.find_element(By.XPATH, "//div[@id='plPager']/span/a[@id='hlNext']")
                        next_page_button.click()
                    except:
                        break
                reset_input()
                print(f"已抓取案件總數: {len(judgement_links)}")
        print(f"案件連結抓取完畢，總共 {len(judgement_links)} 件，開始下載案件內容。")
        return judgement_links

    def get_all_judgement_page(self, search_str, court_name, judgement_type):
        links = self.get_judgement_links_count(search_str, court_name)
        if(judgement_type == ''):
            print(f"總共 {links} 件")
        os.makedirs('judgement_docs', exist_ok=True)
        judgement_links = self.get_judgement_links(search_str, court_name, judgement_type)   
        def get_judgement_page(link):
            link_id = link.split('&id=')[1].split('&ot=')[0]
            pure_page_link = 'https://judgment.judicial.gov.tw/EXPORTFILE/reformat.aspx?type=JD' + '&id=' + link_id
            self.driver.get(pure_page_link)
            
            html = self.driver.page_source
            text = re.sub(r'<[^>]+>', '\n', html)
            try:
                text = text.split('裁判字號：')[1].split('資料解析中...請稍後')[0].replace('&nbsp;', ' ').strip('\n')
            except:
                print(pure_page_link)
                sys.exit()
            title = text.split('\n')[0]
            if(title == '\\t系統訊息'  or title == '系統訊息'):
                return 0
            with open('judgement_docs/' + title + '.txt', 'w', encoding='utf-8') as f:
                f.write(text)
                print(title + '.txt 儲存完成')
        
        count = 0
        for link in judgement_links:
            get_judgement_page(link)
            count += 1
            print(f"已儲存案件數: {count}/{len(judgement_links)}")
        print("案件全數抓取完成，程式結束。")
                
JudgementScrawler = JudgementScrawler()
JudgementScrawler.get_all_judgement_page(search_str="性別平等教育法", court_name='', judgement_type='')