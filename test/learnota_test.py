# Unit test for learnota

from pstats import Stats
import cProfile
import unittest
import sys, os
sys.path.append('../')
from learnota import learn_ota, learn_ota_idfs

class LearnOTATest(unittest.TestCase):
    def setUp(self):
        # self.pr = cProfile.Profile()
        # self.pr.enable()
        pass

    def tearDown(self):
        # p = Stats(self.pr)
        # p.strip_dirs()
        # p.sort_stats('cumtime')
        # p.print_stats()
        pass

    def testB(self):
        # learn_ota(os.getcwd() + '/example3.json', debug_flag=False)
        learn_ota(os.getcwd() + '/../experiments/4_4_20/4_4_20-3.json', debug_flag=False)

# example6.json
# Total number of tables explored: 1550
# Total number of tables to explore: 6587
# Total time of learning: 322.55636858940125

# Total number of tables explored: 614
# Total number of tables to explore: 451
# Total time of learning: 52.88415598869324

# Total number of tables explored: 2286
# Total number of tables to explore: 2519
# Total time of learning: 47.44211554527283

if __name__ == "__main__":
    unittest.main()
