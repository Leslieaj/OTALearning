#definitions of timed automata with one clock (OTA)
#read a json file to build an OTA

import sys
import json
from interval import Constraint, complement_intervals

class Location(object):
    """
        The definition of location.
        "Name" for location name;
        "init" for indicating the initial state;
        "accept" for indicating accepting states;
        "flag" for indicating the OTA
    """
    def __init__(self, name="", init=False, accept=False, flag='s'):
        self.name = name
        self.init = init
        self.accept = accept
        self.flag = flag

    def __eq__(self, location):
        if self.name == location.name and self.init == location.init and self.accept == location.accept and self.flag == location.flag:
            return True
        else:
            return False
            
    def __hash__(self):
        return hash(("LOCATION", self.name, self.init, self.accept, self.flag))

    def get_name(self):
        return self.name

    def get_flagname(self):
        return self.flag+'_'+self.name

    def show(self):
        return self.get_flagname() + ',' + str(self.init) + ',' + str(self.accept)

class State(object):
    """
        The definition of state. 
        A state is a pair (l, v) where l is a location and v is a clock valuation.
    """
    def __init__(self, location, v):
        self.location = location
        self.v = v
    
    def get_fraction(self):
        _, fraction_str = str(self.v).split('.')
        fraction = float('0.'+fraction_str)
        return fraction

    def show(self):
        return "(" + self.location.get_flagname() + "," + str(self.v) + ")"

class OTATran(object):
    """
        The definition of OTA transition.
        "source" for the source location name;
        "target" for the target location name;
        "label" for the action name;
        "reset" for indicating whether the clock resets or not;
        "constraints" for the timing constraints.
        "flag" for indicating the OTA
    """
    def __init__(self, id, source="", label="", constraints=None, reset=False, target="", flag=""):
        self.id = id
        self.source = source
        self.label = label
        self.constraints = constraints or []
        self.reset = reset
        self.target = target
        self.flag = flag
    def __eq__(self, otatran):
        if self.source == otatran.source and self.label == otatran.label and self.constraints == otatran.constraints and self.reset == otatran.reset and self.target == otatran.target and self.flag == otatran.flag:
            return True
        else:
            return False
    def __hash__(self):
        return hash(("OTATRAN", self.source, self.label,self.constraints[0], self.reset, self.target, self.flag))
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
            #Return "closed" for indicating whether we can reach the max time value constant.
        """
        max_time_value = 0
        #closed_flag = True
        for tran in self.trans:
            for c in tran.constraints:
                temp_max_value = 0
                #temp_closed = True
                if c.max_value == '+':
                    temp_max_value = int(c.min_value)
                    #temp_closed = c.closed_min
                else:
                    temp_max_value = int(c.max_value)
                    #temp_closed = c.closed_max
                if max_time_value < temp_max_value:
                    max_time_value = temp_max_value
                    #closed_flag = temp_closed
                #elif max_time_value == temp_max_value:
                    #closed_flag = closed_flag or temp_closed
                #else:
                    #pass
        return max_time_value
    
    def findlocationbyname(self, lname):
        for l in self.locations:
            if l.name == lname:
                return l
        return None

    def show(self):
        print("OTA name: ")
        print(self.name)
        print("sigma and length of sigma: ")
        print(self.sigma, len(self.sigma))
        print("Location (name, init, accept) :")
        for l in self.locations:
            print(l.show())
        print("transitions (id, source_state, label, target_state, constraints, reset): ")
        for t in self.trans:
            print(t.id, t.flag+'_'+t.source, t.label, t.flag+'_'+t.target, t.show_constraints(), t.reset)
            print
        print("init state: ")
        print(self.initstate_name)
        print("accept states: ")
        print(self.accept_names)

class Timedword(object):
    """The definition of timedword without resetting information.
    """
    def __init__(self, action, time):
        self.action = action
        self.time = time
    def __eq__(self, tw):
        if self.action == tw.action and self.time == tw.time:
            return True
        else:
            return False

    def show(self):
        return '(' + self.action + ',' + str(self.time) + ')'
    
    def __str__(self):
        return self.show()
    
    def __repr__(self):
        return self.show()

class ResetTimedword(Timedword):
    """The definition of timedword with resetting information.
    """
    def __init__(self, action, time, reset):
        self.action = action
        self.time = time
        self.reset = reset
    
    def resetflag(self):
        if self.reset == True:
            return 'R'
        else:
            return 'N'

    def show(self):
        return '(' + self.action + ',' + str(self.time) + ',' + self.resetflag() + ')'
    
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()

def buildOTA(jsonfile, otaflag):
    """
        build the teacher OTA from a json file.
    """
    #otaflag = 's'
    data = json.load(open(jsonfile,'r'))
    name = data["name"]
    locations_list = [l for l in data["l"]]
    sigma = [s for s in data["sigma"]]
    trans_set = data["tran"]
    initstate = data["init"]
    accept_list = [l for l in data["accept"]]
    L = [Location(location, False, False, otaflag) for location in locations_list]
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
        ota_tran = OTATran(tran_id, source, label, constraints_list, reset, target, otaflag)
        trans += [ota_tran]
    trans.sort(key=lambda x: x.id)
    return OTA(name, sigma, L, trans, initstate, accept_list), sigma

def buildAssistantOTA(ota, otaflag):
    """
        build an assistant OTA which has the partitions at every node.
        The acceptance language is equal to teacher.
    """
    location_number = len(ota.locations)
    tran_number = len(ota.trans)
    new_location = Location(str(location_number+1), False, False, otaflag)
    #flag = False
    new_trans = []
    for l in ota.locations:
        l_dict = {}
        for key in ota.sigma:
            l_dict[key] = []
        for tran in ota.trans:
            if tran.source == l.name:
                for label in ota.sigma:
                    if tran.label == label:
                        for constraint in tran.constraints:
                            l_dict[label].append(constraint)
        for key in l_dict:
            cuintervals = []
            if len(l_dict[key]) > 0:
                cuintervals = complement_intervals(l_dict[key])
            else:
                cuintervals = [Constraint("[0,+)")]
            if len(cuintervals) > 0:
                for c in cuintervals:
                    reset = True
                    temp_tran = OTATran(tran_number, l.name, key, [c], reset, new_location.name, otaflag)
                    tran_number = tran_number+1
                    new_trans.append(temp_tran)
    assist_name = "Assist_"+ota.name
    assist_locations = [location for location in ota.locations]
    assist_trans = [tran for tran in ota.trans]
    assist_init = ota.initstate_name
    assist_accepts = [sn for sn in ota.accept_names]
    if len(new_trans) > 0:
        assist_locations.append(new_location)
        for tran in new_trans:
            assist_trans.append(tran)
        for label in ota.sigma:
            constraints = [Constraint("[0,+)")]
            reset = True
            temp_tran = OTATran(tran_number, new_location.name, label, constraints, reset, new_location.name, otaflag)
            tran_number = tran_number+1
            assist_trans.append(temp_tran)
    return OTA(assist_name, ota.sigma, assist_locations, assist_trans, assist_init, assist_accepts)

# def main():
#     print("------------------A-----------------")
#     paras = sys.argv
#     A,_ = buildOTA(paras[1], 's')
#     A.show()
#     print("------------------Assist-----------------")
#     AA = buildAssistantOTA(A, 's')
#     AA.show()
#     print("--------------max value---------------------")
#     print(AA.max_time_value())

# if __name__=='__main__':
# 	main()
