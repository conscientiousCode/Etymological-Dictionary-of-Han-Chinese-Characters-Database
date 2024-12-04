import unittest
import string_tools as ST

class StringToolsTest(unittest.TestCase):
    
    def testStringifyArray(self):
        arr = [1,2,3]
        arr_string = "[1, 2, 3]"
        self.assertEqual(arr_string, ST.StringifyArray(arr))
        
        arr = ["1", "2", "3"]
        arr_string = "[1, 2, 3]"
        self.assertEqual(arr_string, ST.StringifyArray(arr))
        
        arr = []
        arr_string = "[]"
        self.assertEqual(arr_string, ST.StringifyArray(arr))
        
    def testArrayifyString(self):
        arr = ["1", "2", "3"]
        arr_string = "[1, 2, 3]"
        self.assertEqual(arr, ST.ArrayifyString(arr_string))
        
        arr = []
        arr_string = "[]"
        self.assertEqual(arr, ST.ArrayifyString(arr_string))




if __name__ == '__main__':
    unittest.main()