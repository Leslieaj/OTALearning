#Unit tests for otatable.py

import unittest
import sys
sys.path.append('../')
from otatable import *
from equivalence import *

A, _ = buildOTA('../example.json', 's')
AA = buildAssistantOTA(A, 's')  # Assist

rtw1 = ResetTimedword('a',0,True)
rtw2 = ResetTimedword('b',0,True)
rtw3 = ResetTimedword('a',1,False)
rtw4 = ResetTimedword('b',2,True)

rtws0 = [] # empty
rtws1 = [rtw1]
rtws2 = [rtw2]
rtws3 = [rtw3]
rtws4 = [rtw3,rtw4]

e0 = Element(rtws0,[0])
e1 = Element(rtws1,[0])
e2 = Element(rtws2,[0])
e3 = Element(rtws3,[0])
e4 = Element(rtws4,[1])

class EquivalenceTest(unittest.TestCase):
    def testResetTimedword(self):
        self.assertEqual(rtws0,[])
        self.assertEqual([rtw.show() for rtw in rtws1],["(a,0,R)"])
        self.assertEqual([rtw.show() for rtw in rtws2],["(b,0,R)"])
        self.assertEqual([rtw.show() for rtw in rtws3],["(a,1,N)"])
        self.assertEqual([rtw.show() for rtw in rtws4],["(a,1,N)","(b,2,R)"])

    def testOTATable_isclosed(self):
        S1 = [e0]
        R1 = [e1,e2]
        E1 = []
        T1 = OTATable(S1,R1,E1)
        #T1.show()
        flag_closed, new_S, new_R, move = T1.is_closed()
        self.assertEqual([flag_closed,new_S,new_R,move], [True,T1.S,T1.R,[]])

        ctx1 = Element([ResetTimedword('a',1,False)],[1])
        R2 = [e1,e2,ctx1]
        T2 = OTATable(S1,R2,E1)
        flag_closed, new_S, new_R, move = T2.is_closed()
        self.assertEqual(flag_closed,False)
        self.assertEqual(new_S, [e0,ctx1])
        self.assertEqual(new_R, [e1,e2])
        self.assertEqual(move,[ctx1])

    # def testMakeclosed(self):
    #     S1 = [e0]
    #     R1 = [e1,e2]
    #     E1 = []
    #     T1 = OTATable(S1,R1,E1)
    #     #T1.show()
    #     flag_closed, new_S, new_R, move = T1.is_closed()
    #     self.assertEqual([flag_closed,new_S,new_R,move], [True,T1.S,T1.R,[]])

    #     R2 = [e1,e2,e3,e4]
    #     T2 = OTATable(S1,R2,E1)
    #     flag_closed, new_S, new_R, move = T2.is_closed()
    #     T3 = make_closed(new_S, new_R, move, T2, AA.sigma, AA)
    #     T3.show()

if __name__ == "__main__":
    unittest.main()