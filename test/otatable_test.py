#Unit tests for otatable.py

import unittest
import sys
sys.path.append('../')
#from otatable import *
from equivalence import *
from hypothesis import *

A, _ = buildOTA('../example.json', 's')
AA = buildAssistantOTA(A, 's')  # Assist
max_time_value = AA.max_time_value()

rtw1 = ResetTimedword('a',0,True)
rtw2 = ResetTimedword('b',0,True)
rtw3 = ResetTimedword('a',1,False)
rtw4 = ResetTimedword('b',2,True)

rtws0 = [] # empty
rtws1 = [rtw1]
rtws2 = [rtw2]
rtws3 = [rtw3]
rtws4 = [rtw3,rtw4]

# e0 = Element(rtws0,[0])
# e1 = Element(rtws1,[0])
# e2 = Element(rtws2,[0])
# e3 = Element(rtws3,[0])
# e4 = Element(rtws4,[1])

class EquivalenceTest(unittest.TestCase):
    def testResetTimedword(self):
        self.assertEqual(rtws0,[])
        self.assertEqual([rtw.show() for rtw in rtws1],["(a,0,R)"])
        self.assertEqual([rtw.show() for rtw in rtws2],["(b,0,R)"])
        self.assertEqual([rtw.show() for rtw in rtws3],["(a,1,N)"])
        self.assertEqual([rtw.show() for rtw in rtws4],["(a,1,N)","(b,2,R)"])

    def testOTATable_isclosed(self):
        e0 = Element(rtws0,[0])
        e1 = Element(rtws1,[0])
        e2 = Element(rtws2,[0])
        e3 = Element(rtws3,[0])
        e4 = Element(rtws4,[1])

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

    def testMakeclosed(self):
        e0 = Element(rtws0,[0])
        e1 = Element(rtws1,[0])
        e2 = Element(rtws2,[0])
        e3 = Element(rtws3,[0])
        e4 = Element(rtws4,[1])
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
        T3 = make_closed(new_S, new_R, move, T2, AA.sigma, AA)
        #T3.show()

    def testToFA(self):
        e0 = Element(rtws0,[0])
        e1 = Element(rtws1,[0])
        e2 = Element(rtws2,[0])
        e3 = Element(rtws3,[0])
        e4 = Element(rtws4,[1])
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
        T3 = make_closed(new_S, new_R, move, T2, AA.sigma, AA)
        #T3.show()
        FA2 = to_fa(T3, 2)
        #FA2.show()

    def testFAToOTA(self):
        e0 = Element(rtws0,[0])
        e1 = Element(rtws1,[0])
        e2 = Element(rtws2,[0])
        e3 = Element(rtws3,[0])
        e4 = Element(rtws4,[1])
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
        T3 = make_closed(new_S, new_R, move, T2, AA.sigma, AA)
        #T3.show()
        FA2 = to_fa(T3, 2)
        H2 = fa_to_ota(FA2, AA.sigma, 2)
        #H2.show()

    def test1(self):
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

        S1 = [e0]
        R1 = [e1,e2]
        E1 = []
        T1 = OTATable(S1,R1,E1)
        FA1 = to_fa(T1, 1)
        H1 = fa_to_ota(FA1, AA.sigma, 1)
        #H1.show()
        flag1, w1 = ota_inclusion(max_time_value, H1, AA)
        self.assertEqual(flag1, False)
        rtws1 = findDelayRTWs(w1, 's', AA)
        self.assertEqual(rtws1, [ResetTimedword('a',1,False)])
        ctx1 = Element(rtws1, [1])
        self.assertEqual(ctx1, Element([ResetTimedword('a',1,False)],[1]))
        T2 = add_ctx(rtws1,T1,AA)
        #T2.show()
        flag_closed, new_S, new_R, move = T2.is_closed()
        self.assertEqual(flag_closed, False)
        T3 = make_closed(new_S, new_R, move, T2, AA.sigma, AA)
        flag_evidence_closed, new_added = T3.is_evidence_closed(AA)
        self.assertEqual(flag_evidence_closed, True)
        #T3.show()
        FA2 = to_fa(T3, 2)
        #FA2.show()
        H2 = fa_to_ota(FA2, AA.sigma, 2)
        #H2.show()

        flag2, w2 = ota_inclusion(max_time_value, AA, H2)
        self.assertEqual(flag2, False)
        rtws2 = findDelayRTWs(w2, 's', AA)
        #print(rtws2)
        T4 = add_ctx(rtws2,T3,AA)
        #T4.show()
        flag_closed, new_S, new_R, move = T4.is_closed()
        self.assertEqual(flag_closed, True)
        flag_consistent, new_a, new_e_index = T4.is_consistent()
        self.assertEqual(flag_consistent, True)
        flag_evidence_closed, new_added = T4.is_evidence_closed(AA)
        self.assertEqual(flag_evidence_closed, True)
        FA3 = to_fa(T4, 3)
        #FA3.show()
        H3 = fa_to_ota(FA3, AA.sigma, 3)
        #H3.show()
        flag3, w3 = ota_inclusion(max_time_value, H3, AA)
        self.assertEqual(flag3, False)
        rtws3 = findDelayRTWs(w3, 's', AA)
        #print(rtws3)
        T5 = add_ctx(rtws3,T4,AA)
        #T5.show()
        flag_closed, new_S, new_R, move = T5.is_closed()
        self.assertEqual(flag_closed, True)
        flag_consistent, new_a, new_e_index = T5.is_consistent()
        self.assertEqual(flag_consistent, True)
        flag_evidence_closed, new_added = T5.is_evidence_closed(AA)
        self.assertEqual(flag_evidence_closed, True)
        FA4 = to_fa(T5, 4)
        #FA4.show()
        H4 = fa_to_ota(FA4, AA.sigma, 4)
        #H4.show()
        flag4, w4 = ota_inclusion(max_time_value, AA, H4)
        self.assertEqual(flag4, False)
        rtws4 = findDelayRTWs(w4, 's', AA)
        #print(rtws4)
        T6 = add_ctx(rtws4,T5,AA)
        #T6.show()
        flag_closed, new_S, new_R, move = T6.is_closed()
        self.assertEqual(flag_closed, True)
        flag_consistent, new_a, new_e_index = T6.is_consistent()
        self.assertEqual(flag_consistent, False)
        #print(new_a)
        #print(new_e_index)
        # print()
        T7 = make_consistent(new_a,new_e_index,T6,AA.sigma,AA)
        #T7.show()
        flag_closed, new_S, new_R, move = T6.is_closed()
        self.assertEqual(flag_closed, False)
        T8 = make_closed(new_S, new_R, move, T7, AA.sigma, AA)
        #T8.show()
        #print()
        flag_consistent, new_a, new_e_index = T8.is_consistent()
        self.assertEqual(flag_consistent, True)
        flag_evidence_closed, new_added = T8.is_evidence_closed(AA)
        self.assertEqual(flag_evidence_closed, False)
        for e in new_added:
            print(e.tws,e.value)
        T9 = make_evidence_closed(new_added, T8, AA.sigma, AA)
        #T9.show()
        #print()
        FA5 = to_fa(T9, 5)
        FA5.show()
        print()
        H5 = fa_to_ota(FA5,AA.sigma,5)
        H5.show()
        print()
        flag5, w5 = ota_inclusion(max_time_value, AA, H5)
        self.assertEqual(flag5, False)
        rtws5 = findDelayRTWs(w5, 's', AA)
        #print(rtws5)
        T10 = add_ctx(rtws5,T9,AA)
        #T9.show()
        #print()
        flag_closed, new_S, new_R, move = T10.is_closed()
        self.assertEqual(flag_closed, True)
        flag_consistent, new_a, new_e_index = T10.is_consistent()
        self.assertEqual(flag_consistent, True)
        flag_evidence_closed, new_added = T10.is_evidence_closed(AA)
        self.assertEqual(flag_evidence_closed, True)
        FA6 = to_fa(T10, 6)
        H6 = fa_to_ota(FA6, AA.sigma, 6)
        H6.show()
        # flag6, w6 = ota_inclusion(max_time_value, AA, H6)
        # self.assertEqual(flag6, True)
        # flag7, w7 = ota_inclusion(max_time_value, H6, AA)
        # self.assertEqual(flag7, True)
        flag_equivalent, _ = equivalence_query(max_time_value,AA,H6)
        self.assertEqual(flag_equivalent, True)


if __name__ == "__main__":
    unittest.main()