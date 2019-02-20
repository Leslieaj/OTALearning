#unit test for equivalence.py

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
s3 = State(L1, 1.2)
s4 = State(L2, 0.4)
s5 = State(L2, 1.0)
q1 = State(Q3, 0.8)
q2 = State(Q3, 1.3)


Ac = [s1,s2,s3,s4,s5]
Bstate = q2
Ac2 = [s1,s2,s4]

A, _ = buildOTA('../a.json', 's')
AA = buildAssistantOTA(A, 's')  # Assist
max_time_value = AA.max_time_value()
regions = get_regions(max_time_value)

letter1 = state_to_letter(s1, max_time_value)  # s_1,[0,0]
letter2 = state_to_letter(s2, max_time_value)  # s_1,(0,1)
letter3 = state_to_letter(s3, max_time_value)  # s_1,(1,2)
letter5 = state_to_letter(s5, max_time_value)  # s_2,[1,1]

B, _ = buildOTA('../b.json', 'q')
BB = buildAssistantOTA(B, 'q')
C, _ = buildOTA('../c.json', 'q')
CC = buildAssistantOTA(C, 'q')
D, _ = buildOTA('../d.json', 'q')
DD = buildAssistantOTA(D, 'q')
E, _ = buildOTA('../e.json', 'q')
EE = buildAssistantOTA(E, 'q')

class EquivalenceTest(unittest.TestCase):
    def testRegions(self):
        self.assertEqual(len(regions), 10)
        self.assertEqual(regions[0].show(), "[0,0]")
        self.assertEqual(regions[1].show(), "(0,1)")
        self.assertEqual(regions[9].show(), "(4,+)")
        
    def testLetters(self):
        self.assertEqual(letter1.show(), "s_1,[0,0]")
        self.assertEqual(letter2.show(), "s_1,(0,1)")
        self.assertEqual(letter3.show(), "s_1,(1,2)")
        self.assertEqual(letter5.show(), "s_2,[1,1]")

    def testABConfiguration(self):
        ABConfig = ABConfiguration(Ac, Bstate)
        letterword = ABConfig.configuration_to_letterword(max_time_value)
        res = [
            {Letter(L1, "[0,0]"), Letter(L2, "[1,1]")},
            {Letter(L1, "(1,2)")},
            {Letter(L1, "(0,1)"), Letter(Q3, "(1,2)")},
            {Letter(L2, "(0,1)")},
        ]
        self.assertEqual(letterword, res)

    def testLetterSubset(self):
        test_data = [
            ({letter1, letter5}, {letter3}, False),
            ({letter5, letter1}, {letter1, letter5}, True),
            ({letter1}, {letter1, letter5}, True),
        ]
        for l1, l2, res in test_data:
            self.assertEqual(l1.issubset(l2), res)

    def testLetterwordDominated(self):
        ABConfig = ABConfiguration(Ac, Bstate)
        letterword = ABConfig.configuration_to_letterword(max_time_value)
        ABConfig2 = ABConfiguration(Ac2, Bstate)
        letterword2 = ABConfig2.configuration_to_letterword(max_time_value)
        res = [
            {Letter(L1, "[0,0]")},
            {Letter(L1, "(0,1)"), Letter(Q3, "(1,2)")},
            {Letter(L2, "(0,1)")},
        ]
        self.assertEqual(letterword2, res)
        self.assertEqual(letterword_dominated(Letterword(letterword2),Letterword(letterword)), True)

    def testNextRegion(self):
        test_data = [
            (regions[2], regions[3]),
            (regions[8], regions[9]),
            (regions[9], regions[9]),
            (regions[5], regions[6]),
        ]
        for region, next in test_data:
            self.assertEqual(next_region(region, max_time_value), next)
    
    def testMinnumInRegion(self):
        r1 = Constraint("[5,9]")
        r2 = Constraint("(4,+)")
        r3 = Constraint("(0,8)")
        self.assertEqual(minnum_in_region(r1),5)
        self.assertAlmostEqual(minnum_in_region(r2),4.1)
        self.assertAlmostEqual(minnum_in_region(r3),0.1)

    def testComputeWsucc(self):
        w = [{Letter(L1, regions[0]), Letter(Q1, regions[0])}]
        wsucc,_ = compute_wsucc(Letterword(w,None,''), max_time_value, A, B)
        #for letterword in wsucc:
            #print(letterword)
        #print()
        res = [
            Letterword([{Letter(L1, '[0,0]'), Letter(Q1, '[0,0]')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '(0,1)'), Letter(Q1, '(0,1)')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '[1,1]'), Letter(Q1, '[1,1]')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '(1,2)'), Letter(Q1, '(1,2)')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '[2,2]'), Letter(Q1, '[2,2]')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '(2,3)'), Letter(Q1, '(2,3)')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '[3,3]'), Letter(Q1, '[3,3]')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '(3,4)'), Letter(Q1, '(3,4)')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '[4,4]'), Letter(Q1, '[4,4]')}],Letterword(w,None,''),"DELAY"),
            Letterword([{Letter(L1, '(4,+)'), Letter(Q1, '(4,+)')}],Letterword(w,None,''),"DELAY"),        
        ]
        self.assertEqual(wsucc, res)
        
        w = [{Letter(L1, regions[5]), Letter(Q2, regions[9])}]
        wsucc,_ = compute_wsucc(Letterword(w,None,'a'), max_time_value, A, B)
        #for letterword in wsucc:
            #print(letterword)
        #print()
        res = [
            Letterword([{Letter(L1, '(2,3)'), Letter(Q2, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '[3,3]'), Letter(Q2, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '(3,4)'), Letter(Q2, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '[4,4]'), Letter(Q2, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '(4,+)'), Letter(Q2, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
        ]
        self.assertEqual(wsucc, res)
        
        w = [{Letter(L1, regions[0])}, {Letter(Q2, regions[1])}]
        wsucc,_ = compute_wsucc(Letterword(w,None,'a'), max_time_value, A, B)
        #for letterword in wsucc:
            #print(letterword)
        #print()
        res = [
            Letterword([{Letter(L1, '[0,0]')}, {Letter(Q2, '(0,1)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '(0,1)')}, {Letter(Q2, '(0,1)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '[1,1]')}, {Letter(L1, '(0,1)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '(1,2)')}, {Letter(L1, '(0,1)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '[1,1]')}, {Letter(Q2, '(1,2)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '(1,2)')}, {Letter(Q2, '(1,2)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '[2,2]')}, {Letter(L1, '(1,2)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '(2,3)')}, {Letter(L1, '(1,2)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '[2,2]')}, {Letter(Q2, '(2,3)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '(2,3)')}, {Letter(Q2, '(2,3)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '[3,3]')}, {Letter(L1, '(2,3)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '(3,4)')}, {Letter(L1, '(2,3)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '[3,3]')}, {Letter(Q2, '(3,4)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '(3,4)')}, {Letter(Q2, '(3,4)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '[4,4]')}, {Letter(L1, '(3,4)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '(4,+)')}, {Letter(L1, '(3,4)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '[4,4]')}, {Letter(Q2, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(L1, '(4,+)')}, {Letter(Q2, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
            Letterword([{Letter(Q2, '(4,+)')}, {Letter(L1, '(4,+)')}],Letterword(w,None,'a'),"DELAY"),
        ]
        self.assertEqual(wsucc, res)
        
        w = [{Letter(L1, regions[1])}, {Letter(Q3, regions[5])}]
        wsucc,_ = compute_wsucc(Letterword(w,None,'b'), max_time_value, A, B)
        #for letterword in wsucc:
            #print(letterword.lw, letterword.action)
        #print()
        res = [
            Letterword([{Letter(L1, '(0,1)')}, {Letter(Q3, '(2,3)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(Q3, '[3,3]')}, {Letter(L1, '(0,1)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(Q3, '(3,4)')}, {Letter(L1, '(0,1)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '[1,1]')}, {Letter(Q3, '(3,4)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '(1,2)')}, {Letter(Q3, '(3,4)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(Q3, '[4,4]')}, {Letter(L1, '(1,2)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(Q3, '(4,+)')}, {Letter(L1, '(1,2)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '[2,2]')}, {Letter(Q3, '(4,+)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '(2,3)')}, {Letter(Q3, '(4,+)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(Q3, '(4,+)')}, {Letter(L1, '(2,3)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '[3,3]')}, {Letter(Q3, '(4,+)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '(3,4)')}, {Letter(Q3, '(4,+)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(Q3, '(4,+)')}, {Letter(L1, '(3,4)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '[4,4]')}, {Letter(Q3, '(4,+)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(L1, '(4,+)')}, {Letter(Q3, '(4,+)')}],Letterword(w,None,'b'),"DELAY"),
            Letterword([{Letter(Q3, '(4,+)')}, {Letter(L1, '(4,+)')}],Letterword(w,None,'b'),"DELAY"),
        ]
        self.assertEqual(wsucc, res)

    def testImmediateASucc(self):
        L1 = A.findlocationbyname("1")
        L2 = A.findlocationbyname("2")
        L3 = A.findlocationbyname("3")
        Q1 = B.findlocationbyname("1")
        Q2 = B.findlocationbyname("2")
        w0 = [{Letter(L1, "[0,0]"), Letter(Q1, "[0,0]")}]
        lw1 = Letterword(w0, Letterword(w0,None,''), "DELAY")
        wsucc1, next1 = compute_wsucc(lw1, max_time_value, A, B)
        # for letterword in wsucc1:
        #     print(letterword.lw, letterword.action)
        # print()
        # for letterword in next1:
        #     print(letterword.lw, letterword.prelw.lw)
        res1 = [
            Letterword([{Letter(Q2,'[0,0]')}, {Letter(L2,'(1,2)')}], Letterword([{Letter(Q1,"(1,2)"), Letter(L1,"(1,2)")}],lw1,"DELAY"),'a'),
            Letterword([{Letter(L2,'[2,2]'), Letter(Q2,'[0,0]')}], Letterword([{Letter(L1,"[2,2]"), Letter(Q1,"[2,2]")}],lw1,"DELAY"),'a'),
            Letterword([{Letter(Q2,'[0,0]')}, {Letter(L2,'(2,3)')}], Letterword([{Letter(Q1,"(2,3)"), Letter(L1,"(2,3)")}],lw1,"DELAY"),'a'),
        ]
        self.assertEqual(next1, res1)
        
        w1 = next1[0]
        wsucc2, next2 = compute_wsucc(w1, max_time_value, A, B)
        # for letterword in next2:
        #     print(letterword.lw, letterword.action, letterword.prelw.lw, letterword.prelw.prelw.lw)
        res2 = [
            Letterword([{Letter(L3,'[0,0]'), Letter(Q1,'[0,0]')}], Letterword([{Letter(Q2,"[2,2]")}, {Letter(L2,"(3,4)")}], w1, "DELAY"), 'b'),
        ]
        #self.assertEqual(next2, res2)
        
        w2 = next1[1]
        wsucc3, next3 = compute_wsucc(w2, max_time_value, A, B)
        self.assertEqual(next3, [])
        
        w3 = next1[2]
        wsucc4, next4 = compute_wsucc(w3, max_time_value, A, B)
        self.assertEqual(next4, [])
        
        D1 = DD.findlocationbyname("1")
        w4 = [{Letter(D1, '[0,0]'), Letter(L1, '[0,0]')}]
        wsucc5, next5 = compute_wsucc(Letterword(w4,None,''), max_time_value, DD, AA)
        # for letterword in wsucc5:
        #     print(letterword.lw, letterword.action)
        # print()
        # for letterword in next5:
            # print(letterword.lw, letterword.action)
        # print()
        D2 = DD.findlocationbyname("2")
        D3 = DD.findlocationbyname("3")
        D4 = DD.findlocationbyname("4")
        res5 = [
            [{Letter(L4, '[0,0]'), Letter(D4, '[0,0]')}],
            [{Letter(L2, '[1,1]'), Letter(D2, '[1,1]')}],
            [{Letter(L2, '(1,2)'), Letter(D2, '(1,2)')}],
            [{Letter(L2, '[2,2]'), Letter(D4, '[0,0]')}],
            [{Letter(D4, '[0,0]')}, {Letter(L2, '(2,3)')}],
        ]
        #self.assertEqual(next5, res5)

    #     w5 = next5[4]
    #     # print(w5)
    #     wsucc6, next6 = compute_wsucc(w5, max_time_value, DD, AA)
    #     # for letterword in wsucc6:
    #     #     print(letterword)
    #     # print()
    #     # for letterword in next6:
    #     #     print(letterword)
    #     # print()
    #     res6 = [
    #         [{Letter(D4, '[0,0]'), Letter(L4, '[0,0]')}],
    #         [{Letter(L3, '[0,0]'), Letter(D4, '[0,0]')}],
    #     ]
    #     self.assertEqual(next6, res6)
    #     #print(is_bad_letterword(next6[1], DD, AA))
        
    def testIsBadLetterword(self):
        letterword1 = [{Letter(L1, '(1,2)'), Letter(Q1, '(3,4)')}]
        letterword2 = [{Letter(Q2, '[0,0]')}, {Letter(L2, '(2,3)')}]
        letterword3 = [{Letter(L3, '[0,0]')}, {Letter(Q1, '(1,2)')}]
        letterword4 = [{Letter(L3, '[0,0]'), Letter(Q2, '[0,0]')}]
        self.assertEqual(is_bad_letterword(letterword1, A, B), False)
        self.assertEqual(is_bad_letterword(letterword2, A, B), True)
        self.assertEqual(is_bad_letterword(letterword3, A, B), False)
        self.assertEqual(is_bad_letterword(letterword4, A, B), False)

    def testOTAInclusion(self):
        self.assertEqual(ota_inclusion(max_time_value, AA, BB)[0], False)
        self.assertEqual(ota_inclusion(max_time_value, AA, CC)[0], True)
        self.assertEqual(ota_inclusion(max_time_value, CC, AA)[0], True)
        self.assertEqual(ota_inclusion(max_time_value, DD, AA)[0], True)
        self.assertEqual(ota_inclusion(max_time_value, AA, DD)[0], False)
        self.assertEqual(ota_inclusion(max_time_value, EE, AA)[0], True)
        self.assertEqual(ota_inclusion(max_time_value, AA, EE)[0], False)
    
    def testFindDelayTimedwords(self):
        flag, w = ota_inclusion(max_time_value, AA, EE)
        delay_timedwords = findDelayTimedwords(w, 'q', EE.sigma)
        self.assertEqual(delay_timedwords, [Timedword('a',1),Timedword('b',1),Timedword('a',0),Timedword('b',2)])

    def testFindGlobalTimedwords(self):
        flag, w = ota_inclusion(max_time_value, AA, EE)
        global_timedwords = findGlobalTimedwords(w, 'q', EE.sigma)
        self.assertEqual(global_timedwords, [Timedword('a',1),Timedword('b',2),Timedword('a',2),Timedword('b',4)])

    def testdelayTWs_to_globalTWs(self):
        flag, w = ota_inclusion(max_time_value, AA, EE)
        delay_timedwords = findDelayTimedwords(w, 'q', EE.sigma)
        global_timedwords = delayTWs_to_globalTWs(delay_timedwords)
        self.assertEqual(global_timedwords, [Timedword('a',1),Timedword('b',2),Timedword('a',2),Timedword('b',4)])

    def testFindDelayRTWs(self):
        flag, w = ota_inclusion(max_time_value, AA, EE)
        delay_resettimedwords = findDelayRTWs(w, 'q', EE)
        # for drtw in delay_resettimedwords:
        #     print(drtw.show())
        self.assertEqual(delay_resettimedwords, [ResetTimedword('a',1,False),ResetTimedword('b',1,True),ResetTimedword('a',0,True),ResetTimedword('b',2,True)])

if __name__ == "__main__":
    unittest.main()
