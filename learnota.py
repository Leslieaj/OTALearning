#The main file
import sys
import time
import copy

from ota import buildOTA, buildAssistantOTA
from otatable import init_table, add_ctx, make_closed, make_consistent, make_evidence_closed
from hypothesis import to_fa, fa_to_ota, remove_sinklocation
from equivalence import equivalence_query

def main():
    #print("------------------A-----------------")
    paras = sys.argv
    A,_ = buildOTA(paras[1], 's')
    #A,_ = buildOTA("example.json", 's')
    #A.show()
    #print("------------------Assist-----------------")
    AA = buildAssistantOTA(A, 's')
    #AA.show()
    #print("--------------max value---------------------")
    max_time_value = A.max_time_value()
    #print(max_time_value)
    #print("--------------all regions---------------------")
    #regions = get_regions(max_time_value)
    # for r in regions:
    #     print(r.show())
    print("**************Start to learn ...*******************")
    print("---------------initial table-------------------")
    sigma = AA.sigma
    T1 = init_table(sigma, AA)
    t_number = 1
    print("Table " + str(t_number) + " is as follow.")
    T1.show()
    print("-----------------------------------------------")
    start = time.time()
    equivalent = False
    table = copy.deepcopy(T1)
    eq_number = 0
    target = None
    while equivalent == False:
        prepared = table.is_prepared(AA)
        while prepared == False:
            flag_closed, new_S, new_R, move = table.is_closed()
            if flag_closed == False:
                temp = make_closed(new_S, new_R, move, table, sigma, AA)
                table = temp
                t_number = t_number + 1
                print("Table " + str(t_number) + " is as follow.")
                table.show()
                print("--------------------------------------------------")
            flag_consistent, new_a, new_e_index = table.is_consistent()
            if flag_consistent == False:
                temp = make_consistent(new_a, new_e_index, table, sigma, AA)
                table = temp
                t_number = t_number + 1
                print("Table " + str(t_number) + " is as follow.")
                table.show()
                print("--------------------------------------------------")
            flag_evi_closed, new_added = table.is_evidence_closed(AA)
            if flag_evi_closed == False:
                temp = make_evidence_closed(new_added, table, sigma, AA)
                table = temp
                t_number = t_number + 1
                print("Table " + str(t_number) + " is as follow.")
                table.show()
                print("--------------------------------------------------")
            prepared = table.is_prepared(AA)
        fa, sink_name = to_fa(table, t_number)
        #print("---------------------------------------------")
        #fa.show()
        #print("---------------------------------------------")
        h = fa_to_ota(fa, sink_name, sigma, t_number)
        #h.show()
        #print("---------------------------------------------")
        target = copy.deepcopy(h)
        equivalent, ctx = equivalence_query(max_time_value,AA,h)
        #print(ctx.show())
        eq_number = eq_number + 1
        if equivalent == False:
            temp = add_ctx(ctx.tws,table,AA)
            table = temp
            t_number = t_number + 1
            print("Table " + str(t_number) + " is as follow.")
            table.show()
            print("--------------------------------------------------")
    end_learning = time.time()
    if target is None:
        print("Error! Learning Failed.")
        print("*******************Failed .***********************")
    else:
        print("Succeed! The learned OTA is as follows.")
        print("---------------------------------------------------")
        target.show()
        print("---------------------------------------------------")
        # print("Total time of learning: " + str(end-start))
        # print("---------------------------------------------------")
        # print("Time intervals simplification...")
        # print()
        print("Removing the sink location...")
        print()
        print("The learned One-clock Timed Automtaton: ")
        print()
        target_without_sink = remove_sinklocation(target)
        end_removesink = time.time()
        target_without_sink.show()
        print("---------------------------------------------------")
        print("Total time of learning: " + str(end_learning-start))
        print("---------------------------------------------------")
        print("Total time of learning + simplifing: " + str(end_removesink-start))
        print("---------------------------------------------------")
        print("The element number of S in the last table: " + str(len(table.S)))
        print("The element number of R in the last table: " + str(len(table.R)))
        print("The element number of E in the last table (excluding the empty-word): " + str(len(table.E)))
        print("Total number of observation table: " + str(t_number))
        print("Total number of membership query: " + str((len(table.S)+len(table.R))*(len(table.E)+1)))
        print("Total number of equivalence query: " + str(eq_number))
        print("*******************Successful !***********************")

if __name__=='__main__':
	main()
