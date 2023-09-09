"""基本的に連続で行うと途中でロボットかの確認が発生するので、手動作業発生するのでchrome表示
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By


class SearchAccount:
    def __init__(self) -> None:
        pass

    def chrome_driver(self):
        # 自動で最新バージョンをダウンロード
        driver_path = ChromeDriverManager().install()
        driver = webdriver.Chrome(service=Service(executable_path=driver_path))
        return driver
    
    def get_url(self, search_word, driver:webdriver.Chrome):
        results = set()
        # メモ：今回検索する単語
        # 代表取締役 OR CEO OR 経営者
        # 検索URL
        driver.get("https://bitwave.showcase-tv.com/instagram-multiple-hashtag/")
        time.sleep(5)
        # 検索欄入力
        search = driver.find_element(By.NAME, "search")
        search.send_keys(Keys.ENTER)
        search.send_keys(search_word)
        # 検索ボタンクリック
        button = driver.find_element(By.CLASS_NAME, "gsc-search-button")
        button.click()
        time.sleep(5)

        # 全ページ取得
        pages = driver.find_elements(By.CLASS_NAME, "gsc-cursor-page")
        page_count = 1
        for _ in range(len(pages)):
            # ページ以降
            if page_count != 1:
                pages = driver.find_elements(By.CLASS_NAME, "gsc-cursor-page")
                for page in pages:
                    try:
                        if page.get_attribute('aria-label') == f'ページ {page_count}':
                            page.click()
                            break
                    except Exception as e:
                        print(f'次ページ以降失敗: {e}')
            # ロボットかの確認はいるため、手動で回避できるように長めにスリープ
            time.sleep(5)
            # 表示されたページのURLを取得
            get_links = driver.find_elements(By.CLASS_NAME, "gs-title")
            for link in get_links:
                user_link = link.get_attribute('href')
                if user_link and not '/explore/' in user_link and not '/tags/' in user_link and not '/p/' in user_link:
                    # ?以降の文字削除
                    user_link = user_link.split('/?')[0]
                    # /_uを削除
                    user_link = user_link.replace('/_u/', '/')
                    results.add(user_link)
            page_count += 1
        return results
        

