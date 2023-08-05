import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.hmm import HyperParams
class test_hmm(unittest.TestCase):
    def test_(self):
        self.assertAlmostEquals(1,1)
    def test_save_to_json(self):
        hmm = HyperParams(a=2,d=[1,2,3])
        hmm.save_to_json('test.json')
    def test_load_from_json(self):
        hmm = HyperParams.load_from_json('test.json')
        self.assertAlmostEquals(hmm["a"],2)
        self.assertAlmostEquals(hmm["d"][0],1)
        self.assertAlmostEquals(hmm["d"][1],2)
        self.assertAlmostEquals(hmm["d"][2],3)
    
if __name__ == '__main__':
    unittest.main()