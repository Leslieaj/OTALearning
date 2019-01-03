#Unit tests fot ota.py

import unittest
import sys
sys.path.append('../')
from equivalence import *

L1 = Location("1", True, False, 's')
L2 = Location("2", False, False, 's')
L3 = Location("3", False, True, 's')
L4 = Location("4", False, False, 's')
Q1 = Location("1", True, False, 'q')
Q2 = Location("2", False, True, 'q')
Q3 = Location("3", False, True, 'q')
Q4 = Location("4", False, False, 'q')

s1 = State(L1, 0.0)
s2 = State(L1, 0.3)

A, _ = buildOTA('../a.json', 's')
AA = buildAssistantOTA(A, 's')  # Assist

class EquivalenceTest(unittest.TestCase):
    def testLocation(self):
        self.assertEqual(L1.show(), "s_1,True,False")
        self.assertEqual(L1.get_name(), "1")
        self.assertEqual(type(L1.get_name()), str)
        self.assertEqual(L2.show(), "s_2,False,False")
        self.assertEqual(Q3.show(), "q_3,False,True")

    def testState(self):
        self.assertEqual(s1.show(), "(s_1,0.0)")
        self.assertEqual(s2.show(), "(s_1,0.3)")

    def testMaxTimeValue(self):
        self.assertEqual(AA.max_time_value(), 4)
    
    def testFindlocationbyname(self):
        temp = A.findlocationbyname("1")
        self.assertEqual(temp, L1)

    def testBuildOTA(self):
        tran0 = OTATran(0, L1.name, 'a', [Constraint("[1,3)")], False, L2.name, 's')
        tran1 = OTATran(1, L2.name, 'b', [Constraint("[2,4)")], True, L3.name, 's')
        tran2 = OTATran(2, L3.name, 'a', [Constraint("[1,2]")], True, L2.name, 's')
        self.assertEqual(A.name, "A")
        self.assertAlmostEqual(A.sigma, ['a','b'])
        self.assertAlmostEqual(len(A.sigma), 2)
        self.assertAlmostEqual(len(A.sigma), 2)
        self.assertAlmostEqual(A.locations, [L1,L2,L3])
        self.assertEqual(A.trans, [tran0, tran1, tran2])
        self.assertEqual(A.initstate_name, '1')
        self.assertEqual(A.accept_names,['3'])

    def testbuildAssistantOTA(self):
        L1 = AA.findlocationbyname("1")
        L2 = AA.findlocationbyname("2")
        L3 = AA.findlocationbyname("3")
        L4 = AA.findlocationbyname("4")
        tran0 = OTATran(0, L1.name, 'a', [Constraint("[1,3)")], False, L2.name, 's')
        tran1 = OTATran(1, L2.name, 'b', [Constraint("[2,4)")], True, L3.name, 's')
        tran2 = OTATran(2, L3.name, 'a', [Constraint("[1,2]")], True, L2.name, 's')
        tran3 = OTATran(3, L1.name, 'b', [Constraint("[0,+)")], True, L4.name, 's')
        tran4 = OTATran(4, L1.name, 'a', [Constraint("[0,1)")], True, L4.name, 's')
        tran5 = OTATran(5, L1.name, 'a', [Constraint("[3,+)")], True, L4.name, 's')
        tran6 = OTATran(6, L2.name, 'b', [Constraint("[0,2)")], True, L4.name, 's')
        tran7 = OTATran(7, L2.name, 'b', [Constraint("[4,+)")], True, L4.name, 's')
        tran8 = OTATran(8, L2.name, 'a', [Constraint("[0,+)")], True, L4.name, 's')
        tran9 = OTATran(9, L3.name, 'b', [Constraint("[0,+)")], True, L4.name, 's')
        tran10 = OTATran(10, L3.name, 'a', [Constraint("[0,1)")], True, L4.name, 's')
        tran11 = OTATran(11, L3.name, 'a', [Constraint("(2,+)")], True, L4.name, 's')
        tran12 = OTATran(12, L4.name, 'a', [Constraint("[0,+)")], True, L4.name, 's')
        tran13 = OTATran(13, L4.name, 'b', [Constraint("[0,+)")], True, L4.name, 's')        
        self.assertEqual(AA.name,"Assist_A")
        self.assertEqual(AA.sigma,['a','b'])
        self.assertEqual(len(AA.sigma),2)
        self.assertEqual(AA.locations,[L1,L2,L3,L4])
        self.assertEqual(set(AA.trans),set([tran0,tran1,tran2,tran3,tran4,tran5,tran6,tran7,tran8,tran9,tran10,tran11,tran12,tran13]))
        self.assertEqual(AA.initstate_name,'1')
        self.assertEqual(AA.accept_names,['3'])
    
    def testResetTimedword(self):
        tw1 = Timedword('a',2)
        rtw1 = ResetTimedword('b',3.1,True)
        self.assertEqual(tw1.show(), "(a,2)")
        self.assertEqual(rtw1.show(), "(b,3.1,R)")
        #print(rtw1)

if __name__ == "__main__":
    unittest.main()
