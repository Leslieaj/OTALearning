#Unit tests for otatable.py

import unittest
import sys,os
sys.path.append('../')
from ota import buildAssistantOTA, buildOTA, ResetTimedword, Timedword, dRTWs_to_lRTWs
from otatable import OTATable, init_table_normal, Element, guess_resets_in_suffixes, guess_resets_in_newsuffix, normalize, prefixes, add_ctx_normal, make_closed, make_consistent
from equivalence import equivalence_query_normal, guess_ctx_reset

class EquivalenceTest(unittest.TestCase):
    def test_init_table_normal(self):
        A = buildOTA('example6.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        #max_time_value = AA.max_time_value()
        sigma = AA.sigma

        tables = init_table_normal(sigma, AA)
        self.assertEqual(len(tables), 1)
        # for table, i in zip(tables, range(1, len(tables)+1)):
        #     print("------------"+ str(i)+"-----------------------")
        #     table.show()
    
    def test_is_closed(self):
        A = buildOTA('example6.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        #max_time_value = AA.max_time_value()
        sigma = AA.sigma

        T1_tables = init_table_normal(sigma, AA)
        self.assertEqual(len(T1_tables), 1)
        #print("--------------------------------------------------")
        flag_closed, new_S, new_R, move = T1_tables[0].is_closed()
        self.assertEqual(flag_closed, False)
        self.assertEqual(new_S, [Element([],[0],[]), Element([ResetTimedword('a',0,True)],[-1],[])])
        self.assertEqual(new_R, [Element([ResetTimedword('b',0,True)],[-1],[]), Element([ResetTimedword('c',0,True)],[-1],[])])
        self.assertEqual(move, Element([ResetTimedword('a',0,True)],[-1],[]))

    def test_make_closed(self):
        A = buildOTA('f.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        #max_time_value = AA.max_time_value()
        sigma = AA.sigma

        T1_tables = init_table_normal(sigma, AA)
        self.assertEqual(len(T1_tables), 2)
        #print("--------------------------------------------------")
        flag_closed, new_S, new_R, move = T1_tables[0].is_closed()
        self.assertEqual(flag_closed, False)
        tables = make_closed(new_S, new_R, move, T1_tables[0], sigma, AA)
        print("--------------make closed---------------------")
        self.assertEqual(len(tables),2)
        # print(len(tables))
        # for table in tables:
        #     table.show()
        #     print("--------------------------")
    
    def test_is_consistent(self):
        A = buildOTA('example2.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        max_time_value = AA.max_time_value()
        sigma = AA.sigma

        s1 = Element([],[0],[])
        s2 = Element([ResetTimedword('a',0,True)],[-1],[])
        s3 = Element([ResetTimedword('a',1,False),ResetTimedword('b',2,True)],[1],[])

        r1 = Element([ResetTimedword('b',0,True)],[-1],[])
        r2 = Element([ResetTimedword('a',0,True),ResetTimedword('a',0,True)],[-1],[])
        r3 = Element([ResetTimedword('a',0,True),ResetTimedword('b',0,True)],[-1],[])
        r4 = Element([ResetTimedword('a',1,False)],[0],[])
        r5 = Element([ResetTimedword('a',1,False),ResetTimedword('b',2,True),ResetTimedword('a',0,False)],[0],[])
        r6 = Element([ResetTimedword('a',1,False),ResetTimedword('b',2,True),ResetTimedword('b',0,True)],[-1],[])
        r7 = Element([ResetTimedword('b',2,True)],[-1],[])

        new_S = [s1,s2,s3]
        new_R = [r1,r2,r3,r4,r5,r6,r7]
        for s in new_S:
            self.assertEqual(AA.is_accepted_delay(dRTWs_to_lRTWs(s.tws)),s.value[0])
        for r in new_R:
            self.assertEqual(AA.is_accepted_delay(dRTWs_to_lRTWs(r.tws)),r.value[0])
        new_E = []
        T5 = OTATable(new_S,new_R,new_E,parent=-1,reason="test")
        # T5.show()
        print("-----------is consistent----------------")
        flag, new_a, new_e_index, i, j, reset_i, reset_j = T5.is_consistent()
        self.assertEqual(flag, False)
        self.assertEqual(new_a, [ResetTimedword('b',2,True)])
        self.assertEqual(new_e_index,0)
        self.assertEqual(i,0)
        self.assertEqual(j,6)
        self.assertEqual(reset_i, True)
        #print(flag, new_a, new_e_index, i, j, reset)

    def test_make_consistent(self):
        A = buildOTA('example2.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        max_time_value = AA.max_time_value()
        sigma = AA.sigma

        s1 = Element([],[0],[])
        s2 = Element([ResetTimedword('a',0,True)],[-1],[])
        s3 = Element([ResetTimedword('a',1,False),ResetTimedword('b',2,True)],[1],[])

        r1 = Element([ResetTimedword('b',0,True)],[-1],[])
        r2 = Element([ResetTimedword('a',0,True),ResetTimedword('a',0,True)],[-1],[])
        r3 = Element([ResetTimedword('a',0,True),ResetTimedword('b',0,True)],[-1],[])
        r4 = Element([ResetTimedword('a',1,False)],[0],[])
        r5 = Element([ResetTimedword('a',1,False),ResetTimedword('b',2,True),ResetTimedword('a',0,False)],[0],[])
        r6 = Element([ResetTimedword('a',1,False),ResetTimedword('b',2,True),ResetTimedword('b',0,True)],[-1],[])
        r7 = Element([ResetTimedword('b',2,True)],[-1],[])

        new_S = [s1,s2,s3]
        new_R = [r1,r2,r3,r4,r5,r6,r7]
        new_E = []
        T5 = OTATable(new_S,new_R,new_E,parent=-1,reason="test")
        # T5.show()
        print("-----------make consistent----------------")
        flag, new_a, new_e_index, i, j, reset_i, reset_j = T5.is_consistent()
        self.assertEqual(flag, False)
        tables = make_consistent(new_a, new_e_index, i, j, reset_i, reset_j, T5, sigma, AA)
        for tb in tables:
            S_U_R = [s for s in tb.S] + [r for r in tb.R]
            self.assertEqual(S_U_R[i].suffixes_resets[-1], [None])
            self.assertEqual(S_U_R[j].suffixes_resets[-1], [None])
        # print(len(tables))
        # tables[0].show()
        # print("-----------")
        # tables[1].show()
        # print("-----------")
        # tables[2].show()
        # print("-----------")
        # tables[100].show()

    def test_guess_resets_in_suffixes(self):
        A = buildOTA('example6.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        #max_time_value = AA.max_time_value()
        sigma = AA.sigma

        T1_tables = init_table_normal(sigma, AA)
        T1_table_0 = T1_tables[0]
        test_E = [[Timedword('a',2),Timedword('b',3),Timedword('a',1)],[Timedword('b',2),Timedword('a',4)],[Timedword('a',5)]]
        T1_table_0.E = test_E
        suffixes_resets = guess_resets_in_suffixes(T1_table_0)
        self.assertEqual(len(suffixes_resets), 8)
        self.assertEqual(len(suffixes_resets[5]), 3)
        # for resets_situtation in suffixes_resets:
        #     print(resets_situtation)

    def test_guess_resets_in_newsuffix(self):
        A = buildOTA('example6.json', 's')
        AA = buildAssistantOTA(A, 's')  # Assist
        #max_time_value = AA.max_time_value()
        sigma = AA.sigma

        T1_tables = init_table_normal(sigma, AA)
        T1_table_0 = T1_tables[0]
        test_E = [[Timedword('a',2),Timedword('b',3),Timedword('a',1)],[Timedword('b',2),Timedword('a',4)]]
        T1_table_0.E = test_E
        suffixes_resets = guess_resets_in_newsuffix(T1_table_0, 0, 0, True, True, AA)
        self.assertEqual(len(suffixes_resets),1)
        self.assertEqual(len(suffixes_resets[0]), 4)
        self.assertEqual(suffixes_resets[0],[[True,None],[True,None],[True,None],[True,None]])

        test_E = [[Timedword('a',2),Timedword('b',3),Timedword('a',1)]]
        T1_table_0.E = test_E
        suffixes_resets = guess_resets_in_newsuffix(T1_table_0, 0, 0, True, True, AA)
        self.assertEqual(len(suffixes_resets),256)
        self.assertEqual(len(suffixes_resets[34]), 4)
        self.assertEqual(suffixes_resets[1],[[True,True,None],[True,True,None],[True,True,None],[True,False,None]])

    def test_add_ctx_normal(self):
        experiments_path = os.path.dirname(os.getcwd())+"/experiments/"
        A = buildOTA(experiments_path+'example3.json', 's')
        AA = buildAssistantOTA(A, 's')
        sigma = AA.sigma
        max_time_value = AA.max_time_value()

        H = buildOTA(experiments_path+'example3_1.json', 'q')
        HH = buildAssistantOTA(H, 'q')

        # AA.show()
        # print("------------------------------")
        # HH.show()
        # print("------------------------------")
        # H.show()
        flag, ctx = equivalence_query_normal(max_time_value,AA,HH)
        # print("-------------ctx-----------------")
        # print(ctx.tws)
        ctxs = guess_ctx_reset(ctx.tws,AA)
        # print(len(ctxs))
        # for rtws in ctxs:
        #     print(rtws)
        # print("-------------local tws-----------------")
        for ctx in ctxs:
            local_tws = dRTWs_to_lRTWs(ctx)
            normalize(local_tws)
        #     #if check_guessed_reset(local_tws, table) == True:
        #     print(ctx)
        #     print(local_tws)
        #     pref = prefixes(local_tws)
        #     for tws in pref:
        #         print(tws)
        #     print("-------------------")
        
        T1_tables = init_table_normal(sigma, AA)
        T1_table_0 = T1_tables[0]
        test_E = [[Timedword('b',2),Timedword('a',4)],[Timedword('a',5)]]
        T1_table_0.E = test_E
        # T1_table_0.show()
        # print("----------------------------------------")
        # tables = add_ctx_normal(ctx, T1_table_0, AA)
        #self.assertEqual(len(tables),65536)
        # tables[0].show()
        # tables[1].show()
        # tables[2].show()
        # tables[100].show()
        # tables[4095].show()
        # for table in tables:
        #     table.show()
        #     print("---------------------")

        T1_tables = init_table_normal(sigma, AA)
        T1_table_0 = T1_tables[0]
        test_E = [[Timedword('b',2),Timedword('a',4)]]
        T1_table_0.E = test_E
        # T1_table_0.show()
        # print("----------------------------------------")
        tables = add_ctx_normal(ctx, T1_table_0, AA)
        self.assertEqual(len(tables),128)
        # print(len(tables))
        # tables[0].show()
        # tables[1].show()
        # tables[2].show()
        # tables[100].show()

if __name__ == "__main__":
    unittest.main()
