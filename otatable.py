# The definitions on the OTA observation table.

import copy
from ota import Timedword, ResetTimedword, is_valid_rtws, dRTWs_to_lRTWs, lRTWs_to_DTWs

class Element(object):
    """The definition of the element in OTA observation table.
    """
    def __init__(self, tws=[], value=[], suffixes_resets=[]):
        self.tws = tws or []
        self.value = value or []
        self.suffixes_resets = suffixes_resets or []
    
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
        return [tw.show() for tw in self.tws], self.value, self.suffixes_resets

table_id = 0

class OTATable(object):
    """The definition of OTA observation table.
    """
    def __init__(self, S = None, R = None, E=[], *, parent, reason):
        global table_id
        self.S = S
        self.R = R
        self.E = E #if E is empty, it means that there is an empty action in E.
        self.id = table_id
        table_id += 1
        self.parent = parent
        self.reason = reason

    def __lt__(self, other):
        return self.id < other.id

    def effective_len(self):
        count = 0
        for S in self.S:
            if S.value[0] != -1:
                count += 1
        for R in self.R:
            if R.value[0] != -1:
                count += 1
        return count

    def is_closed(self):
        """ 1. determine whether the table is closed.
               For each r in R there exists s in S such that row(s) = row(r).
            2. return four values, the first one is a flag to show closed or not, 
               the second one is the new S and the third one is the new R,
               the last one is the element moved from R to S.
        """
        new_S = [s for s in self.S]
        new_R = [r for r in self.R]
        new_S_rows = [s.row() for s in new_S]
        move = None
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
                    move = copy.deepcopy(r)
                    break
                    #new_S_rows = [s.row() for s in new_S]
        if len(new_S) > len(self.S):
            return False, new_S, new_R, move
        else:
            return True, new_S, new_R, move  

    def is_consistent(self):
        """Determine whether the table is consistent.
            (if tws1,tws2 in S U R, if a in sigma* tws1+a, tws2+a in S U R and row(tws1) = row(tws2), 
            then row(tws1+a) = row(tws2+a))
        """
        new_a = None
        new_e_index = None
        table_element = [s for s in self.S] + [r for r in self.R]
        for i in range(0, len(table_element)-1):
            for j in range(i+1, len(table_element)):
                if table_element[i].row() == table_element[j].row():
                    temp_elements1 = []
                    temp_elements2 = []
                    for element in table_element:
                        if len(element.tws) == len(table_element[i].tws) + 1 and \
                           element.tws[:-1] == table_element[i].tws:
                            new_element1 = Element([element.tws[-1]], [v for v in element.value], [])
                            temp_elements1.append(new_element1)
                        if len(element.tws) == len(table_element[j].tws) + 1 and \
                           element.tws[:-1] == table_element[j].tws:
                            new_element2 = Element([element.tws[-1]], [v for v in element.value], [])
                            temp_elements2.append(new_element2)
                    for e1 in temp_elements1:
                        for e2 in temp_elements2:
                            assert len(e1.tws) == 1 and len(e2.tws) == 1
                            if e1.tws[0].action == e2.tws[0].action and e1.tws[0].time == e2.tws[0].time:
                                if e1.row() != e2.row():
                                    new_a = e1.tws
                                    for k in range(0, len(e1.value)):
                                        if e1.value[k] != e2.value[k]:
                                            new_e_index = k
                                            reset_i = e1.tws[0].reset
                                            reset_j = e2.tws[0].reset
                                            return False, new_a, new_e_index, i, j, reset_i, reset_j

        return True, new_a, new_e_index, i, j, True, True

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
                        new_element = Element(new_tws,[]) #---------------todo------------------
                        new_added.append(new_element)
        if len(new_added) > 0:
            flag = False
        return flag, new_added

    def show(self):
        print("new_S:"+str(len(self.S)))
        for s in self.S:
            print(s.tws, s.row(), s.suffixes_resets)
        print("new_R:"+str(len(self.R)))
        for r in self.R:
            print(r.tws, r.row(), r.suffixes_resets)
        print("new_E:"+str(len(self.E)))
        for e in self.E:
            print(e)

def make_closed(new_S, new_R, move, table, sigma, ota):
    """Make table closed.
    """
    new_E = table.E
    closed_table = OTATable(new_S, new_R, new_E, parent=table.id, reason="makeclosed")
    table_tws = [s.tws for s in closed_table.S] + [r.tws for r in closed_table.R]
    temp_resets = [[]]
    for i in range(0,len(sigma)):
        dtws = lRTWs_to_DTWs(move.tws)
        res = ota.is_accepted_delay(dtws + [Timedword(sigma[i], 0)])
        if res == -1:
            guesses = [True]
        else:
            guesses = [True, False]

        new_situations = []
        for guess in guesses:
            new_rtw = ResetTimedword(sigma[i], 0, guess)
            for situation in temp_resets:
                temp = copy.deepcopy(situation) + [new_rtw]
                new_situations.append(temp)
        temp_resets = new_situations

    OTAtables = []
    for situation in temp_resets:
        new_rs = []
        for new_rtw in situation:
            new_r = [tw for tw in move.tws] + [new_rtw]
            if new_r not in table_tws:
                new_rs.append(Element(new_r,[],[]))
        temp_R = [r for r in new_R] + new_rs
        temp_table = OTATable(new_S, temp_R, new_E, parent=table.id, reason="makeclosed")
        OTAtables.append(temp_table)

    #guess the resets of suffixes for each prefix and fill
    OTAtables_after_guessing_resets = []
    for otatable in OTAtables:
        new_r_start_index = len(new_R)
        new_r_end_index = len(otatable.R)
        temp_otatables = [otatable]
        #print(new_r_start_index, new_r_end_index)
        for i in range(new_r_start_index, new_r_end_index):
            res = get_empty_E(otatable.R[i], ota)
            if res == -1:
                resets_situations = guess_resets_in_suffixes(otatable, to_guess=False)
            else:
                resets_situations = guess_resets_in_suffixes(otatable)
            resets_situations = guess_resets_in_suffixes(otatable)
            new_tables = []
            for j in range(0, len(resets_situations)):
                for temp_table in temp_otatables:
                    new_table = copy.deepcopy(temp_table)
                    temp_otatable = OTATable(new_table.S, new_table.R, new_table.E, parent=table.id, reason="makeclosed")
                    temp_otatable.R[i].suffixes_resets = resets_situations[j]
                    new_table = copy.deepcopy(temp_otatable)
                    if True == fill(new_table.R[i],new_table.E,ota):
                        new_tables.append(new_table)
            temp_otatables = [tb for tb in new_tables]
        OTAtables_after_guessing_resets = OTAtables_after_guessing_resets + temp_otatables
    return OTAtables_after_guessing_resets

def make_consistent(new_a, new_e_index, fix_reset_i, fix_reset_j, reset_i, reset_j, table, sigma, ota):
    """Make table consistent.
    """
    new_E = [tws for tws in table.E]
    new_e = [Timedword(tw.action,tw.time) for tw in new_a]
    if new_e_index > 0:
        e = table.E[new_e_index-1]
        new_e.extend(e)
    new_E.append(new_e)
    new_table = OTATable(table.S, table.R, new_E, parent=table.id, reason="makeconsistent")
    temp_suffixes_resets = guess_resets_in_newsuffix(new_table, fix_reset_i, fix_reset_j, reset_i, reset_j, ota)
    OTAtables = []
    for situation in temp_suffixes_resets:
        temp_situation = []
        for resets in situation:
            temp_situation.extend(resets)
        if temp_situation[fix_reset_i] in (None, reset_i) and temp_situation[fix_reset_j] in (None, reset_j):
            temp_table = copy.deepcopy(table)
            temp_table.E = copy.deepcopy(new_E)
            flag_valid = True
            for i in range(0,len(situation)):
                if i < len(table.S):
                    temp_table.S[i].suffixes_resets.append(situation[i])
                    if fill(temp_table.S[i],temp_table.E, ota) == False:
                        flag_valid = False
                        break
                else:
                    temp_table.R[i-len(temp_table.S)].suffixes_resets.append(situation[i])
                    if fill(temp_table.R[i-len(temp_table.S)],temp_table.E, ota) == False:
                        flag_valid = False
                        break
            if flag_valid:
                OTAtables.append(temp_table)
    return OTAtables

def prefixes(tws):
    """Return the prefixes of a timedwords. [tws1, tws2, tws3, ..., twsn]
    """
    prefixes = []
    for i in range(1, len(tws)+1):
        temp_tws = tws[:i]
        prefixes.append(temp_tws)
    return prefixes

def init_table_normal(sigma, ota):
    """Initial tables.
    """
    S = [Element([],[])]
    R = []
    E = []
    for s in S:
        if ota.initstate_name in ota.accept_names:
            s.value.append(1)
        else:
            s.value.append(0)
    tables = [OTATable(S, R, E, parent=-1, reason="init")]
    for i in range(0, len(sigma)):
        temp_tables = []
        for table in tables:
            new_tw = Timedword(sigma[i], 0)
            res = ota.is_accepted_delay([new_tw])
            if res == -1:
                # Now at sink
                guesses = [True]
            else:
                guesses = [True, False]

            for guess in guesses:
                new_rtw = ResetTimedword(new_tw.action, new_tw.time, guess)
                new_element = Element([new_rtw], [res])
                temp_R = table.R + [new_element]
                new_table = OTATable(S, temp_R, E, parent=-1, reason="init")
                temp_tables.append(new_table)

        tables = temp_tables
    return tables

def guess_resets_in_suffixes(table, to_guess=True):
    """Given a table T, before membership querying, we need to guess the reset in the suffixes.
    This method is for one element in S or R. 
    """
    temp_suffixes_resets = []
    cur_pos = 0
    end_pos = []
    for e in table.E:
       cur_pos += len(e)
       end_pos.append(cur_pos)
    length = cur_pos

    temp_resets = [[]]
    for i in range(length):
        temp = []
        for resets_situation in temp_resets:
            if i + 1 in end_pos or not to_guess:
                temp.append(resets_situation + [None])
            else:
                temp.append(resets_situation + [True])
                temp.append(resets_situation + [False])
        temp_resets = temp
    for resets_situation in temp_resets:
        index = 0
        suffixes_resets = []
        for e in table.E:
            e_resets = []
            for i in range(index, index+len(e)):
                e_resets.append(resets_situation[i])
            suffixes_resets.append(e_resets)
            index = index + len(e)
        temp_suffixes_resets.append(suffixes_resets)
    return temp_suffixes_resets

def guess_resets_in_newsuffix(table, fix_reset_i, fix_reset_j, reset_i, reset_j, ota):
    """When making consistent, guess the resets in the new suffix.
    """
    temp_suffixes_resets = []
    new_e = table.E[-1]
    new_e_length = len(new_e)
    S_U_R_length = len(table.S) + len(table.R)
    length = S_U_R_length * new_e_length

    guesses = []
    if new_e_length == 1:
        pass
    elif new_e_length == 2:
        for i in range(S_U_R_length):
            if i < len(table.S):
                to_sink = table.S[i].value[0]
            else:
                to_sink = table.R[i - len(table.S)].value[0]

            if i == fix_reset_i:
                guesses.append([reset_i])
            elif i == fix_reset_j:
                guesses.append([reset_j])
            elif to_sink == -1:
                guesses.append([True])
            else:
                if i < len(table.S):
                    prefix = table.S[i].tws
                else:
                    prefix = table.R[i - len(table.S)].tws
                
                ltwR = prefix + [ResetTimedword(new_e[0].action, new_e[0].time, True),
                                 ResetTimedword(new_e[1].action, new_e[1].time, None)]
                ltwN = prefix + [ResetTimedword(new_e[0].action, new_e[0].time, False),
                                 ResetTimedword(new_e[1].action, new_e[1].time, None)]
                dtwR = lRTWs_to_DTWs(ltwR)
                dtwN = lRTWs_to_DTWs(ltwN)
                res_R = ota.is_accepted_delay(dtwR)
                res_N = ota.is_accepted_delay(dtwN)
                if res_R == -2:
                    guesses.append([False])
                elif res_N == -2:
                    guesses.append([True])
                elif res_R == res_N:
                    guesses.append([True])
                else:
                    guesses.append([True, False])
    else:
        for i in range(S_U_R_length):
            guesses.append([True, False])

    temp_resets = [[]]
    for i in range(0, length):
        temp = []
        for resets_situation in temp_resets:
            if i // new_e_length < len(table.S):
                to_sink = table.S[i // new_e_length].value[0]
            else:
                to_sink = table.R[i // new_e_length - len(table.S)].value[0]
            if i % new_e_length == new_e_length - 1:
                temp.append(resets_situation + [None])
            else:
                guess = guesses[i // new_e_length]
                for g in guess:
                    temp.append(resets_situation + [g])
        temp_resets = temp
    for resets_situation in temp_resets:
        index = 0
        suffixes_resets = []
        for i in range(0, S_U_R_length):
            e_resets = resets_situation[index : index+new_e_length]
            suffixes_resets.append(e_resets)
            index = index + new_e_length
        temp_suffixes_resets.append(suffixes_resets)
    return temp_suffixes_resets

def guess_ctx_reset(dtws, ota):
    """When receiving a counterexample (delay timed word), guess all
    resets and return all reset delay timed words as ctx candidates.  
    
    """
    new_tws = [Timedword(tw.action,tw.time) for tw in dtws]
    ctxs = [[]]
    for i in range(len(new_tws)):
        templist = []
        res = ota.is_accepted_delay(dtws[:i+1])  # Whether the counterexample leads to the sink
        for rtws in ctxs:
            if res == -1:
                temp_r = rtws + [ResetTimedword(new_tws[i].action, new_tws[i].time, True)]
                templist.append(temp_r)
            else:
                temp_n = rtws + [ResetTimedword(new_tws[i].action, new_tws[i].time, False)] 
                temp_r = rtws + [ResetTimedword(new_tws[i].action, new_tws[i].time, True)]
                templist.append(temp_n)
                templist.append(temp_r)
        ctxs = templist
    return ctxs

def check_guessed_reset(lrtws, table):
    """Given a guessed normalized reset-logical(local)-timed-word, check the reset whether it is suitable to current table.
       If the action and the clock valuation are same to the Element in S U R, however, the resets are diferent, then return False to identicate
       the wrong guess.
    """
    S_U_R = [s for s in table.S] + [r for r in table.R]
    for element in S_U_R:
        for rtw, i in zip(lrtws, range(0, len(lrtws))):
            if i < len(element.tws):
                if rtw.action == element.tws[i].action and rtw.time == element.tws[i].time:
                    if rtw.reset != element.tws[i].reset:
                        return False
                else:
                    break
            else:
                break
    return True

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

def build_logical_resettimedwords(element, e, e_index):
    """build a logical reset timedwords based on an element in S,R and a suffix e in E.
    """
    lrtws = [tw for tw in element.tws]
    temp_suffixes_timedwords = [ResetTimedword(tw.action, tw.time, element.suffixes_resets[e_index][j])
                                for j, tw in enumerate(e)]
    lrtws = lrtws + temp_suffixes_timedwords
    # flag = is_valid_rtws(lrtws)
    # return lrtws, flag
    return lrtws, True

def get_empty_E(element, ota):
    """Return the result of running element on ota."""
    local_tws = element.tws
    delay_tws = lRTWs_to_DTWs(local_tws)
    return ota.is_accepted_delay(delay_tws)


def fill(element, E, ota):
    """Fill an element in S U R.
    """
    local_tws = element.tws
    delay_tws = lRTWs_to_DTWs(local_tws)
    if len(element.value) == 0:
        f = ota.is_accepted_delay(delay_tws)
        if f == -2:
            return False
        element.value.append(f)

    for i in range(len(element.value)-1, len(E)):
        lrtws, flag = build_logical_resettimedwords(element, E[i], i)
        if flag == True:
            delay_tws = lRTWs_to_DTWs(lrtws)
            f = ota.is_accepted_delay(delay_tws)
            if f == -2:
                return False
            element.value.append(f)
        else:
            return False
    return True

def add_ctx_normal(dtws, table, ota):
    """Given a counterexample ctx, guess the reset, check the reset,
    for each suitable one, add it and its prefixes to R (except those
    already present in S and R).

    """
    #print(ctx)
    #print(fix_resets(ctx,ota))
    #local_tws = dRTWs_to_lRTWs(fix_resets(ctx,ota))
    OTAtables = []
    ctxs = guess_ctx_reset(dtws, ota)
    for ctx in ctxs:
        local_tws = dRTWs_to_lRTWs(ctx)
        normalize(local_tws)
        if check_guessed_reset(local_tws, table) == True:
            #print(local_tws)
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
                    temp_element = Element(tws,[],[])
                    #fill(temp_element, new_E, ota)
                    new_R.append(temp_element)
            if len(new_R) > len(table.R):
                new_OTAtable = OTATable(new_S, new_R, new_E, parent=table.id, reason="addctx")
                OTAtables.append(new_OTAtable)
    #return OTAtables
    #guess the resets of suffixes for each prefix and fill
    OTAtables_after_guessing_resets = []

    for otatable in OTAtables:
        new_r_start_index = len(table.R)
        new_r_end_index = len(otatable.R)
        temp_otatables = [otatable]
        #print(new_r_start_index, new_r_end_index)
        for i in range(new_r_start_index, new_r_end_index):
            resets_situations = guess_resets_in_suffixes(otatable)
            #print(len(resets_situations))
            new_tables = []
            for j in range(0, len(resets_situations)):
                for temp_table in temp_otatables:
                    new_table = copy.deepcopy(temp_table)
                    temp_otatable = OTATable(new_table.S, new_table.R, new_table.E, parent=table.id, reason="addctx")
                    temp_otatable.R[i].suffixes_resets = resets_situations[j]
                    if True == fill(temp_otatable.R[i],temp_otatable.E,ota):
                        new_tables.append(temp_otatable)
            temp_otatables = [tb for tb in new_tables]
            #print("a", len(temp_otatables))
        OTAtables_after_guessing_resets = OTAtables_after_guessing_resets + temp_otatables
        #print("b", len(OTAtables_after_guessing_resets))

    return OTAtables_after_guessing_resets

