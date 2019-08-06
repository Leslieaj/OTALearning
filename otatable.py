# The definitions on the OTA observation table.

import copy
from ota import Timedword, ResetTimedword, is_valid_rtws, dRTWs_to_lRTWs
#from fa import *

class Element(object):
    """The definition of the element in OTA observation table.
    """
    def __init__(self, tws=[], value=[]):
        self.tws = tws or []
        self.value = value or []
    
    def __eq__(self, element):
        if self.tws == element.tws and self.value == element.value:
            return True
        else:
            return False

    def get_tws_e(self, e):
        tws_e = [tw for tw in self.tws]
        if len(e) == 0:
            return tws_e
        else:
            for tw in e:
                tws_e.append(tw)
            return tws_e

    def row(self):
        return self.value
    
    def whichstate(self):
        state_name = ""
        for v in self.value:
            state_name = state_name+str(v)
        return state_name

    def show(self):
        return [tw.show() for tw in self.tws], self.value

class OTATable(object):
    """The definition of OTA observation table.
    """
    def __init__(self, S = None, R = None, E=[]):
        self.S = S
        self.R = R
        self.E = E #if E is empty, it means that there is an empty action in E.
    
    def is_prepared(self, ota):
        flag_closed, new_S, new_R, move = self.is_closed()
        flag_consistent, new_a, new_e_index = self.is_consistent()
        flag_evid_closed, new_added = self.is_evidence_closed(ota)
        #if flag_closed == True and flag_consistent == True: #and flag_evid_closed == True:
        if flag_closed == True and flag_consistent == True and flag_evid_closed == True:
            return True
        else:
            return False

    def is_closed(self):
        """ 1. determine whether the table is closed.
               For each r \in R there exists s \in S such that row(s) = row(r).
            2. return four values, the first one is a flag to show closed or not, 
               the second one is the new S and the third one is the new R,
               the last one is the list of elements moved from R to S.
        """
        new_S = [s for s in self.S]
        new_R = [r for r in self.R]
        new_S_rows = [s.row() for s in new_S]
        move = []
        for r in self.R:
            flag = False
            for s in self.S:
                if r.row() == s.row():
                    flag = True
                    break
            if flag == False:
                if r.row() not in new_S_rows:
                    new_S.append(r)
                    new_R.remove(r)
                    move.append(r)
                    new_S_rows = [s.row() for s in new_S]
        if len(new_S) > len(self.S):
            return False, new_S, new_R, move
        else:
            return True, new_S, new_R, move      

    def is_consistent(self):
        """Determine whether the table is consistent.
            (if tws1,tws2 in S U R, if a in sigma* tws1+a, tws2+a in S U R and row(tws1) = row(tws2), 
            then row(tws1+a) = row(tws2+a))
        """
        flag = True
        new_a = None
        new_e_index = None
        table_element = [s for s in self.S] + [r for r in self.R]
        for i in range(0, len(table_element)-1):
            for j in range(i+1, len(table_element)):
                if table_element[i].row() == table_element[j].row():
                    temp_elements1 = []
                    temp_elements2 = []
                    #print len(table_element[2].tws), [tw.show() for tw in table_element[2].tws]
                    for element in table_element:
                        #print "element", [tw.show() for tw in element.tws]
                        if is_prefix(element.tws, table_element[i].tws):
                            new_element1 = Element(delete_prefix(element.tws, table_element[i].tws), [v for v in element.value])
                            temp_elements1.append(new_element1)
                        if is_prefix(element.tws, table_element[j].tws):
                            #print "e2", [tw.show() for tw in element.tws]
                            new_element2 = Element(delete_prefix(element.tws, table_element[j].tws), [v for v in element.value])
                            temp_elements2.append(new_element2)
                    for e1 in temp_elements1:
                        for e2 in temp_elements2:
                            #print [tw.show() for tw in e1.tws], [tw.show() for tw in e2.tws]
                            #if len(e1.tws) == 1 and len(e2.tws) == 1 and e1.tws == e2.tws:
                            if len(e1.tws) == 1 and len(e2.tws) == 1 and e1.tws[0].action == e2.tws[0].action and e1.tws[0].time == e2.tws[0].time:
                                if e1.row() == e2.row():
                                    pass
                                else:
                                    flag = False
                                    new_a = e1.tws
                                    for i in range(0, len(e1.value)):
                                        if e1.value[i] != e2.value[i]:
                                            new_e_index = i
                                            return flag, new_a, new_e_index
        return flag, new_a, new_e_index
    
    def is_evidence_closed(self, ota):
        """Determine whether the table is evidence-closed.
        """
        flag = True
        table_tws = [s.tws for s in self.S] + [r.tws for r in self.R]
        new_added = []
        for s in self.S:
            #local_s = dRTWs_to_lRTWs(s.tws)
            local_s = s.tws
            current_location_name = ota.run_resettimedwords(local_s)
            for e in self.E:
                temp_e = []
                current_location = copy.deepcopy(current_location_name)
                reset = True
                clock_valuation = 0
                if len(s.tws) > 0:
                    reset = local_s[len(local_s)-1].reset
                    clock_valuation = local_s[len(local_s)-1].time
                for tw in e:
                    new_timedword = Timedword(tw.action,tw.time)
                    if reset == False and new_timedword.time < clock_valuation:
                        temp_e.append(ResetTimedword(tw.action,tw.time,True))
                        current_location = ota.sink_name
                        clock_valuation = 0
                        break
                    else:
                        for otatran in ota.trans:
                            if otatran.source == current_location and otatran.is_pass(new_timedword):
                                new_resettimedword = ResetTimedword(tw.action,tw.time,otatran.reset)
                                temp_e.append(new_resettimedword)
                                clock_valuation = new_timedword.time
                                reset = otatran.reset
                                if reset == True:
                                    clock_valuation = 0
                                current_location = otatran.target
                                break
                temp_se = [rtw for rtw in s.tws] + [rtw for rtw in temp_e]
                prefs = prefixes(temp_se)
                for pref in prefs:
                    if pref not in table_tws:
                        table_tws.append(pref)
                        #table_tws = [tws for tws in table_tws] + [pref]
                        new_tws = [tws for tws in pref]
                        new_element = Element(new_tws,[])
                        new_added.append(new_element)
        if len(new_added) > 0:
            flag = False
        return flag, new_added

    def show(self):
        print("new_S:"+str(len(self.S)))
        for s in self.S:
            print(s.tws, s.row())
        print("new_R:"+str(len(self.R)))
        for r in self.R:
            print(r.tws, r.row())
        print("new_E:"+str(len(self.E)))
        for e in self.E:
            print(e)

def make_closed(new_S, new_R, move, table, sigma, ota):
    """The function makes the table closed, if the table is not closed.
    """
    #flag, new_S, new_R, move = table.is_closed()
    new_E = table.E
    closed_table = OTATable(new_S, new_R, new_E)
    table_tws = [s.tws for s in closed_table.S] + [r.tws for r in closed_table.R]
    for s in move:
        s_tws = [tw for tw in s.tws]
        for action in sigma:
            #new_tw = get_TW_delay_zero(s_tws, action, ota)
            new_tw, value = new_rtw_in_closed(s_tws,action,ota)
            temp_tws = s_tws+[new_tw]
            if temp_tws not in table_tws:
                temp_element = Element(temp_tws,[value])
                fill(temp_element, closed_table.E, ota)
                closed_table.R.append(temp_element)
                table_tws = [s.tws for s in closed_table.S] + [r.tws for r in closed_table.R]
    return closed_table

def make_consistent(new_a, new_e_index, table, sigma, ota):
    #flag, new_a, new_e_index = table.is_consistent()
    #print flag
    new_E = [tws for tws in table.E]
    #new_E = copy.deepcopy(table.E)
    new_e = [Timedword(tw.action,tw.time) for tw in new_a]
    if new_e_index > 0:
        e = table.E[new_e_index-1]
        new_e.extend(e)
    new_E.append(new_e)
    new_S = [s for s in table.S]
    new_R = [r for r in table.R]
    for i in range(0, len(new_S)):
        fill(new_S[i], new_E, ota)
    for j in range(0, len(new_R)):
        fill(new_R[j], new_E, ota)
    consistent_table = OTATable(new_S, new_R, new_E)
    return consistent_table

def make_evidence_closed(new_added, table, sigma, ota):
    for i in range(0,len(new_added)):
        fill(new_added[i], table.E, ota)
    new_E = [e for e in table.E]
    new_R = [r for r in table.R] + [nr for nr in new_added]
    new_S = [s for s in table.S]
    evidence_closed_table = OTATable(new_S, new_R, new_E)
    return evidence_closed_table

def get_TW_delay_zero(tws, action, ota):
    """When move a timedwords tws from R to S, generate the new delay timedwords with reset information with delay 0.
    """
    new_timedword = None
    #local_tws = dRTWs_to_lRTWs(tws)
    local_tws = tws
    if tws[len(local_tws)-1].reset == False:
        new_timedword = Timedword(action,tws[len(local_tws)-1].time)
    else:
        new_timedword = Timedword(action,0)
    source_location_name = ota.run_resettimedwords(local_tws)
    new_resettimedword = None
    for otatran in ota.trans:
        if otatran.source == source_location_name and otatran.is_pass(new_timedword):
            new_resettimedword = ResetTimedword(action,new_timedword.time,otatran.reset)
            # return the delay timed words with reset information
            #new_resettimedword = ResetTimedword(action,0,otatran.reset)
            break
    return new_resettimedword

def new_rtw_in_closed(tws, action, ota):
    if is_valid_rtws(tws) == False:
        return ResetTimedword(action,0,True), -1
    else:
        current_statename = ota.run_resettimedwords(tws)
        current_clock_valuation = 0
        reset = True
        if len(tws) > 0:
            current_clock_valuation = tws[-1].time
            reset = tws[-1].reset
        if current_statename == ota.sink_name:
            return ResetTimedword(action,0,True), -1
        if reset == False and current_clock_valuation > 0:
            return ResetTimedword(action,0,True), -1
        else:
            flag = False
            for tran in ota.trans:
                if tran.source == current_statename and tran.is_pass(Timedword(action,0)):
                    flag = True
                    current_statename = tran.target
                    new_rtw = ResetTimedword(action,0,tran.reset)
                    if current_statename == ota.sink_name:
                        return new_rtw, -1
                    elif current_statename in ota.accept_names:
                        return new_rtw, 1
                    else:
                        return new_rtw, 0
            if flag == False:
                raise NotImplementedError("new_rtw_in_closed: an unhandle timedword "+Timedword(action,0).show())

def fill(element, E, ota):
    """Fill an element in S U R.
    """
    #local_tws = dRTWs_to_lRTWs(element.tws)
    local_tws = element.tws
    current_location_name = ota.run_resettimedwords(local_tws)
    if len(element.value) == 0:
        f = ota.is_accepted_reset(local_tws)
        element.value.append(f)
    if current_location_name == ota.sink_name:
        for i in range(len(element.value)-1, len(E)):
            element.value.append(-1)
    else:
        for i in range(len(element.value)-1, len(E)):
            current_location = copy.deepcopy(current_location_name)
            reset = True
            clock_valuation = 0
            if len(element.tws) > 0:
                reset = local_tws[len(local_tws)-1].reset
                clock_valuation = local_tws[len(local_tws)-1].time
                if reset == True:
                    clock_valuation = 0
            for tw in E[i]:
                if reset == False and tw.time < clock_valuation:
                    #element.value.append(-1)
                    current_location = ota.sink_name
                    clock_valuation = 0
                    reset = True
                    break
                else:
                    flag = False
                    for otatran in ota.trans:
                        if otatran.source == current_location and otatran.is_pass(tw):
                            reset = otatran.reset
                            clock_valuation = tw.time
                            if reset == True:
                                clock_valuation = 0
                            current_location = otatran.target
                            flag = True
                            break
                    if flag == False:
                        raise NotImplementedError("fill")
                    else:
                        pass
            if current_location in ota.accept_names:
                element.value.append(1)
            elif current_location == ota.sink_name:
                element.value.append(-1)
            else:
                element.value.append(0)

# def fill(element, E, ota):
#     if len(element.value) == 0:
#         f = ota.is_accepted_reset(element.tws)
#         element.value.append(f)
#     #print len(element.value)-1, len(E)
#     for i in range(len(element.value)-1, len(E)):
#         temp_tws = element.tws + E[i]
#         f = ota.is_accepted_reset(temp_tws)
#         element.value.append(f)


def prefixes(tws):
    """Return the prefixes of a timedwords. [tws1, tws2, tws3, ..., twsn]
    """
    prefixes = []
    for i in range(1, len(tws)+1):
        temp_tws = tws[:i]
        prefixes.append(temp_tws)
    return prefixes

def is_prefix(tws, pref):
    """Determine whether the pref is a prefix of the timedwords tws
    """
    if len(pref) == 0:
        return True
    else:
        if len(tws) < len(pref):
            return False
        else:
            for i in range(0, len(pref)):
                if tws[i] == pref[i]:
                    pass
                else:
                    return False
            return True

def delete_prefix(tws, pref):
    """Delete a prefix of timedwords tws, and return the new tws
    """
    if len(pref) == 0:
        return [tw for tw in tws]
    else:
        new_tws = tws[len(pref):]
        return new_tws

def fix_resets(ctx, ota):
    #print(ctx)
    new_tws = [Timedword(rtw.action,rtw.time) for rtw in ctx]
    #print(new_tws)
    dRTWs = []
    current_location = ota.initstate_name
    current_clock_valuation = 0
    reset = True
    for tw in new_tws:
        if reset == False:
            current_clock_valuation = current_clock_valuation + tw.time
        else:
            current_clock_valuation = tw.time
        for tran in ota.trans:
            if tran.source == current_location and tran.is_pass(Timedword(tw.action,current_clock_valuation)):
                dRTWs.append(ResetTimedword(tw.action,tw.time,tran.reset))
                current_location = tran.target
                reset = tran.reset
                break
    return dRTWs

def add_ctx(ctx, table, ota):
    """Given a counterexample ctx, add it and its prefixes to R (except those already present in S and R)
    """
    #print(ctx)
    #print(fix_resets(ctx,ota))
    #local_tws = dRTWs_to_lRTWs(fix_resets(ctx,ota))
    local_tws = dRTWs_to_lRTWs(ctx)
    normalize(local_tws)
    print(local_tws)
    #local_tws = dRTWs_to_lRTWs(ctx)
    pref = prefixes(local_tws)
    S_tws = [s.tws for s in table.S]
    S_R_tws = [s.tws for s in table.S] + [r.tws for r in table.R]
    new_S = [s for s in table.S]
    new_R = [r for r in table.R]
    new_E = [e for e in table.E]
    for tws in pref:
        need_add = True
        for stws in S_R_tws:
        #for stws in S_tws:
            #if tws_equal(tws, stws):
            if tws == stws:
                need_add = False
                break
        if need_add == True:
            temp_element = Element(tws,[])
            fill(temp_element, new_E, ota)
            new_R.append(temp_element)
    return OTATable(new_S, new_R, new_E)

def normalize(tws):
    """Normalize the ctx.
    """
    for rtw in tws:
        if isinstance(rtw.time, int) == True:
            pass
        else:
            integer, frac = str(rtw.time).split('.')
            if frac == '0':
                rtw.time = int(integer)
            else:
                rtw.time = float(integer + '.1')

def init_table(sigma, ota):
    S = [Element([],[])]
    R = []
    E = []
    for s in S:
        if ota.initstate_name in ota.accept_names:
            s.value.append(1)
        else:
            s.value.append(0)
    for action in sigma:
        new_tw = Timedword(action, 0)
        new_element = None
        for tran in ota.trans:
            if tran.source == ota.initstate_name and tran.is_pass(new_tw):
                new_rtw = ResetTimedword(new_tw.action,new_tw.time,tran.reset)
                new_value = []
                if tran.target in ota.accept_names:
                    new_value = [1]
                elif tran.target == ota.sink_name:
                    new_value = [-1]
                else:
                    new_value = [0]
                new_element = Element([new_rtw], new_value)
                R.append(new_element)
                break
    T = OTATable(S, R, E)
    return T


def guess_ctx_reset(dtws):
    """When receiving a counterexample (delay timed word), guess all resets and return all reset delay timed words as ctx candidates.  
    """
    #ctxs = []
    new_tws = [Timedword(tw.action,tw.time) for tw in dtws]
    ctxs = [[ResetTimedword(new_tws[0].action, new_tws[0].time, False)], [ResetTimedword(new_tws[0].action, new_tws[0].time, True)]]
    for i in range(1, len(new_tws)):
        templist = []
        for rtws in ctxs:
            temp_n = rtws + [ResetTimedword(new_tws[i].action, new_tws[i].time, False)] 
            temp_r = rtws + [ResetTimedword(new_tws[i].action, new_tws[i].time, True)]
            templist.append(temp_n)
            templist.append(temp_r)
        #ctxs = copy.deepcopy(templist)
        ctxs = templist
    return ctxs

def check_guessed_reset(lrtws, table):
    """Given a guessed normalized reset-logical(local)-timed-word, check the reset whether it is suitable to current table.
       If the action and the clock valuation are same to the Element in S U R, however, the resets are diferent, then return False to identicate
       the wrong guess.
    """
    S_U_R = [s for s in table.S] + [r for r in table.R]
    for element in S_U_R:
        for rtw, i in zip(lrtws, range(0,lrtws)):
            if i < len(element.tws):
                if rtw.action == element.tws[i].action and rtw.time == element.tws[i].time:
                    if rtw.reset != element.tws[i].reset:
                        return False
            else:
                break
    return True

def add_ctx_normal(dtws, table, ota):
    """Given a counterexample ctx, guess the reset, check the reset, for each suitable one, add it and its prefixes to R (except those already present in S and R)
    """
    #print(ctx)
    #print(fix_resets(ctx,ota))
    #local_tws = dRTWs_to_lRTWs(fix_resets(ctx,ota))
    OTAtables = []
    ctxs = guess_ctx_reset(dtws)
    for ctx in ctxs:
        local_tws = dRTWs_to_lRTWs(ctx)
        normalize(local_tws)
        if check_guessed_reset(local_tws, table) == True:
            print(local_tws)
            pref = prefixes(local_tws)
            S_tws = [s.tws for s in table.S]
            S_R_tws = [s.tws for s in table.S] + [r.tws for r in table.R]
            new_S = [s for s in table.S]
            new_R = [r for r in table.R]
            new_E = [e for e in table.E]
            for tws in pref:
                need_add = True
                for stws in S_R_tws:
                #for stws in S_tws:
                    #if tws_equal(tws, stws):
                    if tws == stws:
                        need_add = False
                        break
                if need_add == True:
                    temp_element = Element(tws,[])
                    fill(temp_element, new_E, ota)
                    new_R.append(temp_element)
            new_OTAtable = OTATable(new_S, new_R, new_E)
            OTAtables.append(new_OTAtable)
    return OTAtables
