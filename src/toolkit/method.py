import requests
from openAI import api, prompt_lib
from toolkit.lib import *
import json
import math

def remove_bad_keyword(query_string:str) -> str:
    for bad_word in BAD_KEYWORD_LIST:
        query_string = query_string.replace(bad_word, '')
    return query_string

def brand_decorator(query_string:str, query_info:dict) -> tuple[str, list[str]]:
    brand_rule_list = ['Other_Electronics', 'Phone_or_Pad']
    brand_list = query_info['brand']
    new_brand_list = []
    category = query_info['category']

    if(len(brand_list) == 1 and category in brand_rule_list):
        new_brand_list = BRAND_DB_MANAGER.get_aliases(brand_list[0])
        if(not new_brand_list):
            print('db none，重新生成')
            new_brand_list = json.loads(api.analysis_brand(prompt_lib, brand_list[0]))['brand']
            try:
                BRAND_DB_MANAGER.insert_brand(new_brand_list)
            except:
                print('DB error')
        brand_list = new_brand_list

    query_string = ' OR '.join(f'"{item}"' for item in brand_list)
    return f'({query_string})', brand_list

def concatenate_query_string(query_info: dict) -> tuple[str, dict]:
    main_product = query_info['main_product']
    brand_list = query_info['brand']
    category = query_info['category']
    query_string = ''

    # 生成新品牌條件:brand只有一個且類別為電子產品
    query_string, brand_list = brand_decorator(query_string, query_info)

    for brand in brand_list:
        main_product = main_product.replace(brand, '').strip()
    # main_product加雙引號
    if(category == 'Phone_or_Pad'):
        query_string += f' "{main_product}"'
    else:
        query_string += f' {main_product}'

    query_info['main_product'] = main_product
    query_info['brand'] = brand_list
    return query_string, query_info

def query_decorator(api_url:str, query_string:str) -> str:
    import urllib.parse
    query_string = urllib.parse.quote(query_string)
    url = f'{api_url}&q={query_string}'
    return url

def send_request(url: str) ->  dict:
    response = requests.get(url)
    if response.status_code >= 200 and response.status_code < 300 :
        res = response.json()
        return res
    else:
        print(response.status_code)

def new_main_product_decorator(total: int, query_string: str, query_info:dict) -> tuple[str, dict]:
    origin_main_product = query_info['main_product']
    if(int(total) <= 20 and len(origin_main_product) >= 10):
        new_main_product = json.loads(api.analysis_main_product(prompt_lib, origin_main_product))['main_product']
        query_info['main_product'] = new_main_product
        query_string = query_string.replace(origin_main_product, new_main_product)
    return query_string, query_info

def country_remove(query_string:str, query_info:dict) -> tuple[str, dict]:
    country = query_info['country']
    origin_main_product = query_info['main_product']
    if(query_info['category'] == 'Food' and country != ''):
        new_main_product = origin_main_product.replace(country, '')
        query_info['main_product'] = new_main_product
        query_string = query_string.replace(origin_main_product, new_main_product)
    return query_string, query_info

def specification_decorator(query_string:str, query_info:dict) -> str:
    number_list = []
    specification_rule_list = ['Other_Electronics', 'Phone_or_Pad']
    if(query_info['category'] in specification_rule_list):
        specification = query_info['specification']
        import re
        number_list = re.findall(r'(\d+)(?:[GgTt\+])', specification, re.IGNORECASE)
    if(len(number_list) > 0):
        for number in number_list:
            query_string += f' {str(number)}'
    return query_string

def generate_query_string(request: dict) -> tuple[QueryStringResponse, dict] | HTTPErrorResult:
    evalute_url = 'https://biggo.com.tw/api/search_products.php?m=def'
    try:
        json_post = json.dumps(request)
        json_post_list = json.loads(json_post)
        title = json_post_list.get('title')
    except Exception as e:
        print(e)
        return Errors.UNSUPPORTED_REQUEST_FORMAT

    try:
        # 移除title中會影響分析的字
        query_string = remove_bad_keyword(title)
        query_info = json.loads(api.get_new_query(prompt_lib, query_string))
        query_string, query_info = concatenate_query_string(query_info)
        first_url = query_decorator(evalute_url, query_string)
        result = send_request(first_url)

        # 二次分析main_product的條件：第一次搜尋總數小於20且main_product的長度大於10
        query_string, query_info = new_main_product_decorator(int(result['rtotal']), query_string, query_info)

        # 移除country的條件：category是food且country不為空值
        query_string, query_info = country_remove(query_string, query_info)
        
        # 添加specification的條件：category是Electronics且有G、GB、T、TB前的數字
        query_string = specification_decorator(query_string, query_info)
        query_info['query_string'] = query_string
        
        url = query_decorator(evalute_url, query_string)
        result = send_request(url)

        price_range = None
        if(result['result']):
            min_price = math.floor(result['result'][0]['price'] / 2)
            price_range = {"min_price":min_price}
            query_info['price_range'] = price_range

    except Exception as e:
        print(e)
        return Errors.GENERATE_QUERY_STRING_ERROR
    
    queryStringResponse = QueryStringResponse(query_string=query_string, price_range=price_range)
    return queryStringResponse, query_info

import sqlite3
class brand_DB_mgr:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.create_table()
        if(len(self.get_all_aliases()) <= 0):
            self.insert_init_brand()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS brand_aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias_list TEXT NOT NULL UNIQUE,
                length INT NOT NULL
            )
        ''')
        self.connection.commit()

    def insert_brand(self, alias_list):
        alias_list_str = ','.join(f'"{al}"' for al in alias_list)
        length = len(alias_list)
        self.cursor.execute('INSERT INTO brand_aliases (alias_list, length) VALUES (?, ?)', (alias_list_str, length))
        self.connection.commit()

    def insert_init_brand(self):
        for brand_aliases in BRAND_ALIASES:
            alias_list = ','.join(f'"{ba}"' for ba in brand_aliases)
            length = len(brand_aliases)
            self.cursor.execute('INSERT INTO brand_aliases (alias_list, length) VALUES (?, ?)', (alias_list, length))
        self.connection.commit()

    def get_aliases(self, query_name):
        self.cursor.execute('SELECT alias_list FROM brand_aliases WHERE alias_list LIKE ?', ('%"' + query_name + '"%',))
        row = self.cursor.fetchone()
        if row:
            alias_list_str = row[0]
            return json.loads(alias_list_str)
        else:
            return None

    def get_all_aliases(self):
        self.cursor.execute('SELECT alias_list, length FROM brand_aliases')
        rows = self.cursor.fetchall()
        alias_list = [(row[0].split(','), row[1]) for row in rows]
        return alias_list

    def close_connection(self):
        self.connection.close()

if(__name__ == 'toolkit.method'):
    print('[連接資料庫]')
    import os
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_filename = 'brand_database/brand.sqlite'
    BRAND_DB_MANAGER = brand_DB_mgr(os.path.join(root_path, db_filename))