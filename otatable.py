# The definitions on the OTA observation table.

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
    
    def is_prepared(self):
        flag_closed, new_S, new_R, move = self.is_closed()
        flag_consistent, new_a, new_e_index = self.is_consistent()
        flag_evid_closed, new_added = self.is_evidence_closed()
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
            (if tws1,tws2 \in S U R, if a \in sigma* tws1+a, tws2+a \in S U R and row(tws1) = row(tws2), 
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
                            if len(e1.tws) == 1 and len(e2.tws) == 1 and e1.tws == e2.tws:
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
    
    def is_evidence_closed(self):
        """Determine whether the table is evidence-closed.
        """
        flag = True
        table_tws = [s.tws for s in self.S] + [r.tws for r in self.R]
        #new_R = [r for r in self.R]
        new_added = []
        for s in self.S:
            for e in self.E:
                temp_se = [tw for tw in s.tws] + [tw for tw in e]
                if temp_se not in table_tws:
                    table_tws.append(temp_se)
                    new_tws = temp_se
                    new_element = Element(new_tws,[])
                    #new_R.append(new_element)
                    new_added.append(new_element)
        if len(new_added) > 0:
            flag = False
        return flag, new_added

    def show(self):
        print("new_S:"+str(len(self.S)))
        for s in self.S:
            print([tw.show() for tw in s.tws], s.row())
        print("new_R:"+str(len(self.R)))
        for r in self.R:
            print([tw.show() for tw in r.tws], r.row())
        print("new_E:"+str(len(self.E)))
        for e in self.E:
            print([tw.show() for tw in e])

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