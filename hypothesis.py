from fa import *
from otatable import *


def to_fa(otatable, n):
    """Given an ota table, transform it to a finite automaton.
    """
    ### First, need to transform the resettimedwords of the elements in S_U_R 
    ### to clock valuation timedwords with reset informations.
    S_U_R = [s for s in otatable.S] + [r for r in otatable.R]
    table_elements = [Element(dRTWs_to_lRTWs(e.tws), e.value) for e in S_U_R]
    ### build a finite automaton
    ## FAStates
    rtw_alphabet = []
    states = []
    initstate_name = ""
    accept_names = []
    value_name_dict = {}
    for s,i in zip(otatable.S, range(1, len(otatable.S)+1)):
        name = str(i)
        value_name_dict[s.whichstate()] = name
        init = False
        accept = False
        if s.tws == []:
            init = True
            initstate_name = name
        if s.value[0] == 1:
            accept = True
            accept_names.append(name)
        temp_state = FAState(name, init, accept)
        states.append(temp_state)
    ## FATrans
    trans_number = 0
    trans = []
    for r in table_elements:
        if r.tws == []:
            continue
        resettimedwords = [tw for tw in r.tws]
        w = resettimedwords[:-1]
        a = resettimedwords[len(resettimedwords)-1]
        if a not in rtw_alphabet:
            rtw_alphabet.append(a)
        source = ""
        target = ""
        #label = [a]
        for element in table_elements:
            if w == element.tws:
                source = value_name_dict[element.whichstate()]
            if resettimedwords == element.tws:
                target = value_name_dict[element.whichstate()]
        need_newtran = True
        for tran in trans:
            if source == tran.source and target == tran.target:
                if a.action == tran.label[0].action and a.reset == tran.label[0].resset:
                    need_newtran == False
                    tran.label.append(a)
                break
        if need_newtran == True:
            temp_tran = FATran(trans_number, source, target, [a])
            trans.append(temp_tran)
            trans_number = trans_number + 1
    fa = FA("FA_"+str(n),rtw_alphabet,states,trans,initstate_name,accept_names)
    return fa

