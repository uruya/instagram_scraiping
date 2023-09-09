import configparser
import os
import errno
from distutils.util import strtobool
import csv
from search_account import SearchAccount

def search_results_write(file_path, results: set):
    # csv書き込み
    if os.path.exists(file_path):
        # 追記
        pass
    else:
        # 新規作成
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['取得URL'])
            for result in results:
                writer.writerow([result])


if __name__ == '__main__':
    # 設定ファイル読み込み
    config_ini = configparser.ConfigParser()
    config_ini_path = 'config.ini'
    if not os.path.exists(config_ini_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
    config_ini.read(config_ini_path, encoding='utf-8')
    default_info = config_ini['Default']
    # キーワード検索
    search_info = config_ini['SearchAccount']
    if  strtobool(search_info.get('exec')):
        search_account = SearchAccount()
        search_word = search_info.get('word')
        # search_word = search_word.replace('|', ' OR ')
        # search_word = search_word.replace('&', ' AND ')
        search_word = search_word.split('|')
        driver = search_account.chrome_driver()
        results = set()
        for search in search_word:
            result = search_account.get_url(search, driver)
            results = results.union(result)
        driver.quit()
        # csv書き込み
        search_results_write(default_info.get('input_file'), results)