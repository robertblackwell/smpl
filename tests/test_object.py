import unittest
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,os.path.join(parentdir)) 

print(sys.path)

import smpl.object as Object

class test_object_test(unittest.TestCase):

    def test_merge(self):
        d_defaults = {
            "a": "aaaaaa",
            "b": "bbbbbb",
            "c": "cccccc",
            "d": "dddddd",
            "e": "eeeeee",
            "f": None,
            "g": None,
            "h": None,
            "k": None,
            "m": None
        }
        d_values = {
            "b": "BBBBBBBB",
            "k": "KKKKKKKK"
        }
        values = Object.parse_to_object(d_values)
        default_values = Object.parse_to_object(d_defaults)

        active_values = Object.merge_objects(values, default_values)

        expected = {
            "a": "aaaaaa",
            "b": "BBBBBBBB",
            "c": "cccccc",
            "d": "dddddd",
            "e": "eeeeee",
            "f": None,
            "g": None,
            "h": None,
            "k": "KKKKKKKK",
            "m": None
        }
        self.assertEqual(len(expected), len(active_values.__dict__))
        for k in active_values.__dict__:
            self.assertEqual(active_values.__dict__[k], expected[k])
        
        print(active_values)

class test_merge_test(unittest.TestCase):

    def test_parse(self) :
        d = {
            "one":'1111', 
            "ar":[
                {"a":"aaaa"},
                {"b":"bbbb"}
            ],
            "ar2":[
                1,2,3,4,5
            ],
            "d2": {
                "d3":{
                    "a":"11111111111111",
                    "b":"2222222222222"
                }
            }
        }
        ob = Object.parse_to_object(d)
        self.assertEqual(ob.one, '1111')
        self.assertEqual(ob.ar[0].a, 'aaaa')
        self.assertEqual(ob.ar2[1], 2)
        self.assertEqual(ob.d2.d3.b, "2222222222222")
        print(ob)

def mainx():
    t = test_object_test()
    t.test_parse()

if __name__ == '__main__':
    unittest.main()