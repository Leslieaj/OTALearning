#Unit tests for otatable.py

import unittest
import sys
sys.path.append('../')
#from otatable import *
from equivalence import *
from hypothesis import *
from learnota import init_table

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

    # def testToFA(self):
    #     e0 = Element(rtws0,[0])
    #     e1 = Element(rtws1,[0])
    #     e2 = Element(rtws2,[0])
    #     e3 = Element(rtws3,[0])
    #     e4 = Element(rtws4,[1])
    #     S1 = [e0]
    #     R1 = [e1,e2]
    #     E1 = []
    #     T1 = OTATable(S1,R1,E1)
    #     #T1.show()
    #     flag_closed, new_S, new_R, move = T1.is_closed()
    #     self.assertEqual([flag_closed,new_S,new_R,move], [True,T1.S,T1.R,[]])

    #     ctx1 = Element([ResetTimedword('a',1,False)],[1])
    #     R2 = [e1,e2,ctx1]
    #     T2 = OTATable(S1,R2,E1)
    #     flag_closed, new_S, new_R, move = T2.is_closed()
    #     T3 = make_closed(new_S, new_R, move, T2, AA.sigma, AA)
    #     #T3.show()
    #     FA2 = to_fa(T3, 2)
    #     #FA2.show()

    # def testFAToOTA(self):
    #     e0 = Element(rtws0,[0])
    #     e1 = Element(rtws1,[0])
    #     e2 = Element(rtws2,[0])
    #     e3 = Element(rtws3,[0])
    #     e4 = Element(rtws4,[1])
    #     S1 = [e0]
    #     R1 = [e1,e2]
    #     E1 = []
    #     T1 = OTATable(S1,R1,E1)
    #     #T1.show()
    #     flag_closed, new_S, new_R, move = T1.is_closed()
    #     self.assertEqual([flag_closed,new_S,new_R,move], [True,T1.S,T1.R,[]])

    #     ctx1 = Element([ResetTimedword('a',1,False)],[1])
    #     R2 = [e1,e2,ctx1]
    #     T2 = OTATable(S1,R2,E1)
    #     flag_closed, new_S, new_R, move = T2.is_closed()
    #     T3 = make_closed(new_S, new_R, move, T2, AA.sigma, AA)
    #     #T3.show()
    #     FA2,_ = to_fa(T3, 2)
    #     H2 = fa_to_ota(FA2,"", AA.sigma, 2)
    #     #H2.show()

    def test1(self):
        A, _ = buildOTA('../example2.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        max_time_value = AA.max_time_value()
        sigma = AA.sigma

        T1 = init_table(sigma, AA)
        T1.show()
        print("--------------------------------------------------")
        flag_closed, new_S, new_R, move = T1.is_closed()
        #print(flag_closed)
        T2 = make_closed(new_S, new_R, move, T1, sigma, AA)
        T2.show()
        print("--------------------------------------------------")
        FA1,sink = to_fa(T2, 1)
        FA1.show()
        print("--------------------------------------------------")
        H1 = fa_to_ota(FA1,sink, AA.sigma, 1)
        H1.show()
        print("--------------------------------------------------")
        flag1, ctx1 = equivalence_query(max_time_value,AA,H1)
        print(flag1)
        print(ctx1.show())
        T3 = add_ctx(ctx1.tws,T2,AA)
        T3.show()
        print("--------------------------------------------------")
        flag_closed, new_S, new_R, move = T3.is_closed()
        #print(flag_closed)
        T4 = make_closed(new_S, new_R, move, T3, sigma, AA)
        T4.show()
        print("--------------------------------------------------")
        FA2,sink = to_fa(T4, 2)
        FA2.show()
        print("--------------------------------------------------")
        H2 = fa_to_ota(FA2,sink,sigma,2)
        H2.show()
        print("--------------------------------------------------")
        flag2, ctx2 = equivalence_query(max_time_value,AA,H2)
        print(flag2)
        print(ctx2.show())
        T5 = add_ctx(ctx2.tws,T4,AA)
        T5.show()
        print("--------------------------------------------------")
        flag_consistent, new_a, new_e_index = T5.is_consistent()
        print(flag_consistent)
        print(new_a)
        T6 = make_consistent(new_a,new_e_index,T5,AA.sigma,AA)
        T6.show()
        print("--------------------------------------------------")
        flag_evidence_closed, new_added = T6.is_evidence_closed(AA)
        print(flag_evidence_closed)
        T7 = make_evidence_closed(new_added, T6, sigma, AA)
        T7.show()
        print("--------------------------------------------------")
        flag_closed, new_S, new_R, move = T7.is_closed()
        T8 = make_closed(new_S, new_R, move, T7, sigma, AA)
        T8.show()
        flag_consistent, new_a, new_e_index = T8.is_consistent()
        print(flag_consistent)
        flag_evidence_closed, new_added = T8.is_evidence_closed(AA)
        print(flag_evidence_closed)
        print("--------------------------------------------------")
        FA3,sink = to_fa(T8, 3)
        FA3.show()
        print("--------------------------------------------------")
        H3 = fa_to_ota(FA3,sink,sigma,3)
        H3.show()
        print("--------------------------------------------------")
        flag3, ctx3 = equivalence_query(max_time_value,AA,H3)
        print(flag3)
        T9 = add_ctx(ctx3.tws,T8,AA)
        T9.show()
        prepared = T9.is_prepared(AA)
        print(prepared)
        print("--------------------------------------------------")
        FA4,sink = to_fa(T9, 4)
        H4 = fa_to_ota(FA4,sink,sigma,4)
        H4.show()
        print("--------------------------------------------------")
        flag4, ctx4 = equivalence_query(max_time_value,AA,H4)
        print(flag4)
        T10 = add_ctx(ctx4.tws,T9,AA)
        T10.show()
        prepared = T10.is_prepared(AA)
        print(prepared)
        print("--------------------------------------------------")
        FA5,sink = to_fa(T10, 5)
        FA5.show()
        print()
        H5 = fa_to_ota(FA5,sink,sigma,5)
        H5.show()
        print("--------------------------------------------------")
        flag5, ctx5 = equivalence_query(max_time_value,AA,H5)
        print(flag5)
        T11 = add_ctx(ctx5.tws,T10,AA)
        T11.show()
        print("--------------------------------------------------")
        prepared = T11.is_prepared(AA)
        print(prepared)
        FA6,sink = to_fa(T11, 6)
        H6 = fa_to_ota(FA6,sink,sigma,6)
        H6.show()
        print("--------------------------------------------------")
        flag6, ctx6 = equivalence_query(max_time_value,AA,H6)
        print(flag6)

if __name__ == "__main__":
    unittest.main()