import unittest
import sys
sys.path.append('../')
from equivalence import *

L1 = Location("1", True, False, 's')
L2 = Location("2", False, False, 's')
L3 = Location("3", False, True, 's')
Q1 = Location("1", True, False, 'q')
Q2 = Location("2", False, True, 'q')
Q3 = Location("3", False, True, 'q')

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



class EquivalenceTest(unittest.TestCase):
    def testLocation(self):
        self.assertEqual(L1.show(), "s_1,True,False")
        self.assertEqual(L1.get_name(), "1")
        self.assertEqual(L2.show(), "s_2,False,False")
        self.assertEqual(Q3.show(), "q_3,False,True")

    def testState(self):
        self.assertEqual(s1.show(), "(s_1,0.0)")
        self.assertEqual(s2.show(), "(s_1,0.3)")

    def testMaxTimeValue(self):
        self.assertEqual(AA.max_time_value(), 4)

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
        self.assertEqual(letterword_dominated(letterword2,letterword), True)

    def testNextRegion(self):
        test_data = [
            (regions[2], regions[3]),
            (regions[8], regions[9]),
            (regions[9], None),
            (regions[5], regions[6]),
        ]
        for region, next in test_data:
            self.assertEqual(next_region(region, max_time_value), next)
            
    def testImmediateASucc(self):
        L1 = A.findlocationbyname("1")
        L2 = A.findlocationbyname("2")
        L3 = A.findlocationbyname("3")
        Q1 = B.findlocationbyname("1")
        Q2 = B.findlocationbyname("2")
        w0 = [{Letter(L1, "[0,0]"), Letter(Q1, "[0,0]")}]
        wsucc1, next1 = compute_wsucc(w0, max_time_value, A, B)
        res1 = [
            [{Letter(Q2,'[0,0]')}, {Letter(L2,'(1,2)')}],
            [{Letter(L2,'[2,2]'), Letter(Q2,'[0,0]')}],
            [{Letter(Q2,'[0,0]')}, {Letter(L2,'(2,3)')}],
        ]
        self.assertEqual(next1, res1)
        
        w1 = next1[0]
        wsucc2, next2 = compute_wsucc(w1, max_time_value, A, B)
        res2 = [
            [{Letter(L3,'[0,0]'), Letter(Q1,'[0,0]')}],
            #[{Letter(L3,'[0,0]'), Letter(Q1,'[0,0]')}],
        ]
        self.assertEqual(next2, res2)
        
        w2 = next1[1]
        wsucc3, next3 = compute_wsucc(w2, max_time_value, A, B)
        self.assertEqual(next3, [])
        
        w3 = next1[2]
        wsucc4, next4 = compute_wsucc(w3, max_time_value, A, B)
        self.assertEqual(next4, [])
        
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
        L1 = A.findlocationbyname("1")
        Q1 = B.findlocationbyname("1")
        self.assertEqual(ota_inclusion(B, A), [{Letter(L1, "[0,0]"), Letter(Q1, "[0,0]")}])

if __name__ == "__main__":
    unittest.main()
