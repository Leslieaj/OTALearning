#The definition of the finite automaton

class FAState(object):
    def __init__(self, name="", init=False, accept=False):
        self.name = name
        self.init = init
        self.accept = accept

    def __eq__(self, fastate):
        if self.name == fastate.name and self.init == fastate.init and self.accept == fastate.accept:
            return True
        else:
            return False
            
    def __hash__(self):
        return hash(("FASTATE", self.name, self.init, self.accept))

    def get_name(self):
        return self.name

    def show(self):
        return self.get_name() + ',' + str(self.init) + ',' + str(self.accept)

class FATran(object):
    def __init__(self, id, source="", target="", label=None):
        self.id = id
        self.source = source
        self.target = target
        self.label = label

class FA:
    def __init__(self, name="", rtw_alphabet = [], states = None, trans = [], initstate_name = "", accept_names = []):
        self.name = name
        self.rtw_alphabet = rtw_alphabet
        self.states = states
        self.trans = trans
        self.initstate_name = initstate_name
        self.accept_names = accept_names

    def show(self):
        print("FA name: ")
        print(self.name)
        print("alphabet:")
        for term in self.rtw_alphabet:
            print(term)
        print("State (name, init, accept)")
        for s in self.states:
            print(s.name, s.init, s.accept)
        print("transitions: (id, source, target, timedword): ")
        for t in self.trans:
            print(t.id, t.source, t.target, t.label)
            #t.resettimedword.show()
            #print
        print("init state: ")
        print(self.initstate_name)
        print("accept states: ")
        print(self.accept_names) 