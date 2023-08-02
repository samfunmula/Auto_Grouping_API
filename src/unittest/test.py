import unittest
import sys
import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from toolkit.method import remove_bad_keyword, query_decorator, country_remove, specification_decorator, concatenate_query_string
from toolkit.lib import BAD_KEYWORD_LIST

class TestQueryingString(unittest.TestCase):
    def test_remove_bad_keyword(self):
        test_string = "".join(BAD_KEYWORD_LIST)
        result = remove_bad_keyword(test_string)
        self.assertEqual(result, '')

    def test_query_decorator(self):
        result = query_decorator('api_url','query&"string"')
        ans = 'api_url&q=query%26%22string%22'
        self.assertEqual(result, ans)

    def test_country_remove(self):
        test_query_info = {
            'country':'泰國',
            'main_product':'泰國天婦羅海苔',
            'category':'Food'
        }
        query_string, query_info = country_remove('泰國天婦羅海苔', test_query_info)
        ans_query_info = {
            'country':'泰國',
            'main_product':'天婦羅海苔',
            'category':'Food'
        }
        self.assertTrue(query_string == '天婦羅海苔' and query_info == ans_query_info)
    
    def test_specification_decorator(self):
        test_query_info1 = {
            'category':'Other_Electronics',
            'specification':'1g 2G 3gb 4GB 5t 6T 7tb 8TB 9+'
        }
        test_query_info2 = {
            'category':'Phone_or_Pad',
            'specification':'1g 2G 3gb 4GB 5t 6T 7tb 8TB 9+'
        }
        ans = 'query_string 1 2 3 4 5 6 7 8 9'
        query_string1 = specification_decorator('query_string', test_query_info1)
        query_string2 = specification_decorator('query_string', test_query_info2)
        self.assertTrue(query_string1 == ans and query_string2 == ans)

class TestConcateQueryString(unittest.TestCase):
    def test_Phone_or_Pad(self):
        test_query_info = {
            'brand':['Apple','蘋果'],
            'main_product':'iphone 14',
            'category':'Phone_or_Pad'
        }
        query_string, query_info = concatenate_query_string(test_query_info)
        ans_query_string = '("Apple" OR "蘋果") "iphone 14"'
        self.assertEqual(query_string, ans_query_string)

    def test_Other_Electronics(self):
        test_query_info = {
            'brand':['Acer'],
            'main_product':'XV272U RV',
            'category':'Other_Electronics'
        }
        query_string, query_info = concatenate_query_string(test_query_info)
        ans_query_string = '("Acer" OR "宏碁") XV272U RV'
        self.assertEqual(query_string, ans_query_string)


if __name__ == '__main__':
    unittest.main(verbosity=2)
