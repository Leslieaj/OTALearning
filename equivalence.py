#OTA equivalence

import sys
from ota import *
from copy import deepcopy

def get_regions(max_time_value):
    """
        Partition R into a finite collection of one-dimensional regions depending on the appearing max time value.
    """
    regions = []
    bound = 2*max_time_value+1
    for i in range(0, bound+1):
        if i % 2 == 0:
            temp = i//2
            r = Constraint('[' + str(temp) + ',' + str(temp) + ']')
            regions.append(r)
        else:
            temp = (i-1)//2
            if temp < max_time_value:
                r = Constraint('(' + str(temp) + ',' + str(temp+1) + ')')
                regions.append(r)
            else:
                r = Constraint('(' + str(temp) + ',' + '+' + ')')
                regions.append(r)
    return regions

def state_to_letter(state, max_time_value):
    region = None
    integer = int(state.v)
    _, fraction_str = str(state.v).split('.')
    fraction = float('0.'+fraction_str)
    if fraction > 0.0:
        if integer < max_time_value:
            region = Constraint('(' + str(integer) + ',' + str(integer+1) + ')')
        else:
            region = Constraint('(' + str(integer) + ',' + '+' + ')')
    else:
        region = Constraint('[' + str(integer) + ',' + str(integer) + ']')
    return fraction, region

class Letter(object):
    """
        The definition of letter. A letter is a pair (location, region).
        "location" for indicating the location
        "constraint" for the region
    """
    def __init__(self, location, constraint):
        self.location = location
        self.constraint = constraint

class ABConfiguration(object):
    """
        The definition of A/B-configuration.
    """
    def __init__(self, Ac, Bstate):
        self.Aconfig = copy.deepcopy(Ac)
        self.Bstate = copy.deepcopy(Bstate)

    def configuration_to_letterword(config):
        """
            Transform an A/B-configuration to a letterword.
        """  
        return 0

def main():
    L1 = Location("1", True, False)
    L2 = Location("2", False, False)
    L3 = Location("3", False, True)
    print(L1.show())
    print(type(L1.get_name()))
    print(L2.show())
    print(L3.show())
    s1 = State(L1, 1.2)
    s2 = State(L3, 3.0)
    print(s1.show())
    print(s2.show())
    print("---------------A------------------")
    paras = sys.argv
    A,_ = buildOTA(paras[1])
    A.show()
    print("------------------Assist-----------------")
    AA = buildAssistantOTA(A, 's')
    AA.show()
    print("--------------max value---------------------")
    max_time_value = AA.max_time_value()
    print(max_time_value)
    print("--------------all regions---------------------")
    regions = get_regions(max_time_value)
    for r in regions:
        print(r.show())
    print("-------------------------------------")
    fr1, re1 = state_to_letter(s1, max_time_value)
    fr2, re2 = state_to_letter(s2, max_time_value)
    print(s1.show(), fr1, re1.show())
    print(s2.show(), fr2, re2.show())

if __name__=='__main__':
	main()
