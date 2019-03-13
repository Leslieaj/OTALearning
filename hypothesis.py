from fa import *
from otatable import *


def to_fa(otatable, n):
    """Given an ota table, build a finite automaton.
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
                    if a not in tran.label:
                        tran.label.append(a)
                break
        if need_newtran == True:
            temp_tran = FATran(trans_number, source, target, [a])
            trans.append(temp_tran)
            trans_number = trans_number + 1
    fa = FA("FA_"+str(n),rtw_alphabet,states,trans,initstate_name,accept_names)
    return fa

def fa_to_ota(fa, sigma, n):
    """Transform the finite automaton to an one-clock timed automaton as a hypothesis.
    """
    new_name = "H_" + str(n)
    #sigma = [action for action in sigma]
    states = [Location(state.name,state.init,state.accept,'q') for state in fa.states]
    initstate_name = fa.initstate_name
    accept_names = [name for name in fa.accept_names]
    ### generate the transitions
    trans = []
    for s in fa.states:
        s_dict = {}
        for key in sigma:
            s_dict[key] = []
        for tran in fa.trans:
            if tran.source == s.name:
                s_dict[tran.label[0].action].extend([rtw.time for rtw in tran.label])
        for tran in fa.trans:
            if tran.source == s.name:
                timepoints = [time for time in s_dict[tran.label[0].action]]
                timepoints.sort()
                for rtw in tran.label:
                    index = timepoints.index(rtw.time)
                    temp_constraint = None
                    ## By now, we assuem that the timepoints are interger numbers.
                    if index + 1 < len(timepoints):
                        temp_constraint = Constraint("[" + str(rtw.time) + "," + str(timepoints[index+1]) + ")")
                    else:
                        temp_constraint = Constraint("[" + str(rtw.time) + "," + "+" + ")")
                    temp_tran = OTATran(len(trans), tran.source, tran.label[0].action, [temp_constraint], rtw.reset, tran.target, 'q')
                    trans.append(temp_tran)
    ota = OTA(new_name,sigma,states,trans,initstate_name,accept_names)
    return ota