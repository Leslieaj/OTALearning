#definitions of timed automata with one clock (OTA)
#read a json file to build an OTA

import sys
import json
from interval import Constraint

class Location(object):
    """
        The definition of location.
        "Name" for location name, "init" for indicating the initial state, "accept" for indicating accepting states.
    """
    def __init__(self, name="", init=False, accept=False):
        self.name = name
        self.init = init
        self.accept = accept

    def getName(self):
        return self.name

    def show(self):
        return self.name + ',' + str(self.init) + ',' + str(self.accept)

class State(object):
    """
        The definition of state. 
        A state is a pair (l, v) where l is a location and v is a clock valuation.
    """
    def __init__(self, location, v):
        self.location = location
        self.v = v

    def show(self):
        return "(" + self.location.getName() + "," + str(self.v) + ")"

class OTATran(object):
    """
        The definition of OTA transition.
        "source" for the source location name;
        "target" for the target location name;
        "label" for the action name;
        "reset" for indicating whether the clock resets or not;
        "constraints" for the timing constraints.
    """
    def __init__(self, id, source="", label="", constraints=None, reset=False, target=""):
        self.id = id
        self.source = source
        self.label = label
        self.constraints = constraints or []
        self.reset = reset
        self.target = target

    def show_constraints(self):
        length = len(self.constraints)
        if length ==0:
            return "[0,+)"
        else:
            temp = self.constraints[0].guard
            for i in range(1, length):
                temp = temp + 'U' + self.constraints[i].guard
            return temp

class OTA(object):
    """
        The definition of Timed Automata with one clock (OTA).
        "name" for the OTA name string;
        "sigma" for the labels list;
        "locations" for the locations list;
        "trans" for the transitions list;
        "initstate_name" for the initial location name;
        "accept_names" fot the list of accepting locations.
    """
    def __init__(self, name, sigma, locations, trans, init, accepts):
        self.name = name
        self.sigma = sigma or []
        self.locations = locations or []
        self.trans = trans or []
        self.initstate_name = init
        self.accept_names = accepts or []
    
    def max_time_value(self):
        """
            Get the max time value constant appearing in OTA.
            Return "max_time_value" for the max time value constant;
            Return "closed" for indicating whether we can reach the max time value constant.
        """
        max_time_value = 0
        closed_flag = True
        for tran in self.trans:
            for c in tran.constraints:
                if c.max_value == '+':
                    continue
                else:
                    temp_max_value = int(c.max_value)
                    temp_closed = c.closed_max
                    if max_time_value < temp_max_value:
                        max_time_value = temp_max_value
                        closed_flag = temp_closed
        return max_time_value, closed_flag

    def show(self):
        print("OTA name: ")
        print(self.name)
        print("sigma and length of sigma: ")
        print(self.sigma, len(self.sigma))
        print("Location (name, init, accept) :")
        for l in self.locations:
            print(l.name, l.init, l.accept)
        print("transitions (id, source_state, label, target_state, constraints, reset): ")
        for t in self.trans:
            print(t.id, t.source, t.label, t.target, t.show_constraints(), t.reset)
            print
        print("init state: ")
        print(self.initstate_name)
        print("accept states: ")
        print(self.accept_names)

def buildRTA(jsonfile):
    """
        build the teacher OTA from a json file.
    """
    data = json.load(open(jsonfile,'r'))
    name = data["name"]
    locations_list = [l for l in data["l"]]
    sigma = [s for s in data["sigma"]]
    trans_set = data["tran"]
    initstate = data["init"]
    accept_list = [l for l in data["accept"]]
    L = [Location(location) for location in locations_list]
    for l in L:
        if l.name == initstate:
            l.init = True
        if l.name in accept_list:
            l.accept = True
    trans = []
    for tran in trans_set:
        tran_id = int(tran)
        source = trans_set[tran][0]
        label = trans_set[tran][1]
        intervals_str = trans_set[tran][2]
        intervals_list = intervals_str.split('U')
        constraints_list = []
        for constraint in intervals_list:
            new_constraint = Constraint(constraint.strip())
            constraints_list.append(new_constraint)
        reset_temp = trans_set[tran][3]
        reset = False
        if reset_temp == "r":
            reset = True
        target = trans_set[tran][4]
        ota_tran = OTATran(tran_id, source, label, constraints_list, reset, target)
        trans += [ota_tran]
    return OTA(name, sigma, L, trans, initstate, accept_list), sigma

def main():
    L1 = Location("1", True, False)
    L2 = Location("2", False, False)
    L3 = Location("3", False, True)
    print(L1.show())
    print(type(L1.getName()))
    print(L2.show())
    print(L3.show())

    s1 = State(L1, 1.2)
    s2 = State(L3, 3.0)
    print(s1.show())
    print(s2.show())
    
    print("-----------------------------------")
    paras = sys.argv
    A,_ = buildRTA(paras[1])
    A.show()
    print("--------------max value---------------------")
    print(A.max_time_value())

if __name__=='__main__':
	main()
