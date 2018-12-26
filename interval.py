#some defines about intervals

import copy
from enum import IntEnum

global MAXVALUE
MAXVALUE = 1000000000

class Bracket(IntEnum):
    """
    Left Open, Left Closed, Right Open, Right Closed.
    """
    RO = 1
    LC = 2
    RC = 3
    LO = 4

class BracketNum:
    def __init__(self, value="", bracket=0):
        self.value = value
        self.bracket = bracket
    def __eq__(self, bn):
        if self.value == bn.value and self.bracket == bn.bracket:
            return True
        else:
            return False
    def __lt__(self, bn):
        if self.value == '+':
            return False
        if bn.value == '+':
            return True
        if int(self.value) > int(bn.value):
            return False
        elif int(self.value) < int(bn.value):
            return True
        else:
            if self.bracket < bn.bracket:
                return True
            else:
                return False
    def __gt__(self, bn):
        if self.value == '+':
            if bn.value == '+':
                return False
            else:
                return True
        if bn.value == '+':
            return False
        if int(self.value) > int(bn.value):
            return True
        elif int(self.value) < int(bn.value):
            return False
        else:
            if self.bracket > bn.bracket:
                return True
            else:
                return False
    def __ge__(self, bn):
        return not self.__lt__(bn)
    def __le__(self, bn):
        return not self.__gt__(bn)
    def complement(self):
        if self.value == '+':
            return BracketNum('+', Bracket.RO)  #ceil
        if self.value == '0' and self.bracket == Bracket.LC:
            return BracketNum('0', Bracket.LC)  #floor
        temp_value = self.value
        temp_bracket = None
        if self.bracket == Bracket.LC:
            temp_bracket = Bracket.RO
        if self.bracket == Bracket.RC:
            temp_bracket = Bracket.LO
        if self.bracket == Bracket.LO:
            temp_bracket = Bracket.RC
        if self.bracket == Bracket.RO:
            temp_bracket = Bracket.LC
        return BracketNum(temp_value, temp_bracket)
    def getIntvalue(self):
        if self.value == '+':
            return MAXVALUE
        else:
            return int(self.value)
    def getbn(self):
        if self.bracket == Bracket.LC:
            return '[' + self.value
        if self.bracket == Bracket.LO:
            return '(' + self.value
        if self.bracket == Bracket.RC:
            return self.value + ']'
        if self.bracket == Bracket.RO:
            return self.value + ')'

class Constraint:
    guard=None
    min_value = ""
    closed_min = True
    max_value = ""
    closed_max = True
    min_bn = None
    max_bn = None
    def __init__(self, guard=None):
        self.guard = guard
        self.__build()
    
    def __build(self):
        min_type, max_type = self.guard.split(',')
        min_bn_bracket = None
        max_bn_bracket = None
        if min_type[0] == '[':
            self.closed_min = True
            min_bn_bracket = Bracket.LC
        else:
            self.closed_min = False
            min_bn_bracket = Bracket.LO
        self.min_value = min_type[1:].strip()
        self.min_bn = BracketNum(self.min_value, min_bn_bracket)
        if max_type[-1] == ']':
            self.closed_max = True
            max_bn_bracket = Bracket.RC
        else:
            self.closed_max = False
            max_bn_bracket = Bracket.RO
        self.max_value = max_type[:-1].strip()
        self.max_bn = BracketNum(self.max_value, max_bn_bracket)
    
    def __eq__(self, constraint):
        if self.min_value == constraint.min_value and self.closed_min == constraint.closed_min and self.max_value == constraint.max_value and self.closed_max == constraint.closed_max:
            return True
        else:
            return False
            
    def __hash__(self):
        return hash(("CONSTRAINT", self.min_value, self.closed_min, self.max_value, self.closed_max))

    def __add__(self, constraint):
        if self.isEmpty() == True or constraint.isEmpty() == True:
            return Constraint("(0,0)")
        else:
            temp_min_value = ""
            temp_max_value = ""
            if self.min_value == '+' or constraint.min_value == '+':
                temp_min_value = '+'
            else:
                temp_min_value = str(int(self.min_value) + int(constraint.min_value))
            if self.max_value == '+' or constraint.max_value == '+':
                temp_max_value = '+'
            else:
                temp_max_value = str(int(self.max_value) + int(constraint.max_value))
            temp_closed_min = '('
            temp_closed_max = ')'
            if self.closed_min == True and constraint.closed_min == True:
                temp_closed_min = '['
            if self.closed_max == True and constraint.closed_max == True:
                temp_closed_max = ']'
            guard = temp_closed_min + temp_min_value + ',' + temp_max_value + temp_closed_max
            return Constraint(guard)
    def complement(self):
        if self.isEmpty() == True:
            return Constraint("[0,+)")
        complement_min_bn = self.min_bn.complement()
        complement_max_bn = self.max_bn.complement()
        left_constraint = None
        right_constraint = None
        complement_intervals = []
        if self.min_bn > BracketNum('0', Bracket.LC):
            left_constraint = Constraint('['+'0'+','+complement_min_bn.getbn())
            complement_intervals.append(left_constraint)
        if self.max_bn < BracketNum('+', Bracket.RO):
            right_constraint = Constraint(complement_max_bn.getbn()+','+'+'+')')
            complement_intervals.append(right_constraint)
        if len(complement_intervals) > 0:
            return complement_intervals, True
        else:
            return [Constraint("(0,0)")], False

    def isEmpty(self):
        if self.max_bn < self.min_bn:
            return True
        else:
            return False
    
    def isininterval(self, num):
        #if self.max_value == '+':
            #return True
        if num < self.get_min():
            return False
        elif num == self.get_min():
            if self.closed_min == True:
                return True
            else:
                return False
        elif num > self.get_min() and num < self.get_max():
            return True
        elif num == self.get_max():
            if self.closed_max == True:
                return True
            else:
                return False
        else:
            return False

    def isPoint(self):
        if self.min_value == '+' or self.max_value == '+':
            return False
        if self.min_value == self.max_value and self.closed_min == True and self.closed_max == True:
            return True
        else:
            return False

    def issubset(self, c2):
        min_bn1 = self.min_bn
        max_bn1 = self.max_bn
        min_bn2 = c2.min_bn
        max_bn2 = c2.max_bn
        if min_bn1 >= min_bn2 and max_bn1 <= max_bn2:
            return True
        else:
            return False
    def get_min(self):
        return int(self.min_value)
    
    def get_max(self):
        if self.max_value == '+':
            closed_max=False
            return MAXVALUE
        else:
            return int(self.max_value)

    def show(self):
        return self.guard

    def __str__(self):
        return self.show()
        
    def __repr__(self):
        return self.show()

def min_constraint_number(c):
    """
        get the minimal number in a interval.
        1. if the interval is empty, return None
        2. if [a, b$, return "a" .  Note: a < b, $ means ) or ]
        3. if (a, b$, return "a.1" .
    """
    if c.isEmpty():
        return None
    if c.closed_min == True:
        return int(c.min_value)
    else:
        return float(c.min_value+".1")

def min_constraints_number(cs):
    """
        get the minimal number in unintersection intervals.
        return the minimal number or None
    """
    minimal_numbers = []
    for c in cs:
        temp = min_constraint_number(c)
        if temp != None:
            minimal_numbers.append(temp)
    minimal_numbers.sort()
    if len(minimal_numbers) > 0:
        return minimal_numbers[0]
    else:
        return None

def intersect_constraint(c1, c2):
    if c1.isEmpty() == True or c2.isEmpty() == True:
        return Constraint("(0,0)"), False
    min_bn1 = c1.min_bn
    max_bn1 = c1.max_bn
    min_bn2 = c2.min_bn
    max_bn2 = c2.max_bn
    bnlist = [min_bn1, max_bn1, min_bn2, max_bn2]
    bnlist.sort()
    left_bn = bnlist[1]
    right_bn = bnlist[2]
    if left_bn in [min_bn1, min_bn2] and right_bn in [max_bn1, max_bn2]:
        return Constraint(left_bn.getbn()+','+right_bn.getbn()), True
    else:
        return Constraint("(0,0)"), False

def constraint_subset(c1, c2):
    """Determin whether c1 is a subset of c2.
    """
    min_bn1 = c1.min_bn
    max_bn1 = c1.max_bn
    min_bn2 = c2.min_bn
    max_bn2 = c2.max_bn
    if min_bn1 >= min_bn2 and max_bn1 <= max_bn2:
        return True
    else:
        return False
    
def constraint_contain(c, intervals):
    intertemp = []
    for constraint in intervals:
        intersect, flag = intersect_constraint(c, constraint)
        if flag == True:
            intertemp.append(intersect)
    union = Constraint("(0,0)")
    num = 1
    for t in intertemp:
        if num == 1 :
            union, num = union_constraint(union, t)
    if num==1 and union == c:
        return True
    else:
        return False

def union_constraint(c1, c2):
    if c1.isEmpty() == True:
        return c2, 1
    if c2.isEmpty() == True:
        return c1, 1
    sortlist = [c1,c2]
    #lqsort(sortlist, 0, len(sortlist)-1)
    lbsort(sortlist)
    if sortlist[1].min_bn.getIntvalue() < sortlist[0].max_bn.getIntvalue():
        temp_bn = sortlist[0].max_bn
        if sortlist[0].max_bn < sortlist[1].max_bn:
            temp_bn = sortlist[1].max_bn
        return Constraint(sortlist[0].min_bn.getbn()+','+temp_bn.getbn()), 1
    elif sortlist[1].min_bn.getIntvalue() == sortlist[0].max_bn.getIntvalue():
        if sortlist[0].max_bn.bracket == Bracket.RO and sortlist[1].min_bn.bracket == Bracket.LO:
            return sortlist, 2
        else:
            return Constraint(sortlist[0].min_bn.getbn()+','+sortlist[1].max_bn.getbn()), 1
    else:
        return sortlist, 2

def union_constraints(cs):
    intervals = copy.deepcopy(cs)
    lbsort(intervals)
    union_intervals = []
    union = Constraint("(0,0)")
    num = 1
    for constraint in intervals:
        if num == 1:
            union, num = union_constraint(union, constraint)
        if num == 2:
            union_intervals.append(union[0])
            union = union[1]
            union, num = union_constraint(union, constraint)
    union_intervals.append(union)
    return union_intervals

def intervals_partition(intervals):
    partitions = []
    floor_bn = BracketNum('0',Bracket.LC)
    ceil_bn = BracketNum('+',Bracket.RO)
    key_bns = []
    for constraint in intervals:
        min_bn = constraint.min_bn
        max_bn = constraint.max_bn
        if min_bn not in key_bns:
            key_bns+= [min_bn]
        if max_bn not in key_bns:
            key_bns+=[max_bn]
    key_bnsc = copy.deepcopy(key_bns)
    for bn in key_bns:
        bnc = bn.complement()
        if bnc not in key_bnsc:
            key_bnsc.append(bnc)
    if floor_bn not in key_bnsc:
        key_bnsc.append(floor_bn)
    if ceil_bn not in key_bnsc:
        key_bnsc.append(ceil_bn)
    key_bnsc.sort()
    for index in range(len(key_bnsc)):
        if index%2 == 0:
            temp_constraint = Constraint(key_bnsc[index].getbn()+','+key_bnsc[index+1].getbn())
            partitions.append(temp_constraint)
    return partitions, key_bnsc

def unintersect_intervals(uintervals):
    length = len(uintervals)
    intervals = copy.deepcopy(uintervals)
    #lqsort(intervals, 0, length-1)
    lbsort(intervals)
    if length <= 1:
        return intervals
    un_intervals = []
    i = 0
    temp = intervals[0]
    while i < length - 1:
        i = i + 1
        uc, flag = union_constraint(temp, intervals[i])
        if flag == 1:
            temp = uc
        if flag == 2:
            un_intervals.append(temp)
            temp = intervals[i]
    if temp not in un_intervals:
        un_intervals.append(temp)
    return un_intervals

def complement_intervals(uintervals):
    partitions, key_bnsc = intervals_partition(uintervals)
    for c in uintervals:
        if c in partitions:
            partitions.remove(c)
    return partitions

def lqsort(array, left, right):
    if left < right:
        mid = lqsortpartition(array, left, right)
        lqsort(array, left, mid-1)
        lqsort(array, mid+1, right)

def lqsortpartition(array, left, right):
    temp = array[left]
    while left < right:
        while left < right and array[right].min_bn > temp.min_bn:
            right = right - 1
        array[left] = array[right]
        while left < right and array[right].min_bn <= temp.min_bn:
            left = left + 1
        array[right] = array[left]
    array[left] = temp
    return left

def lbsort(array):
    for i in range(len(array)-1):
        for j in range(len(array)-i-1):
            if array[j].min_bn > array[j+1].min_bn:
                array[j], array[j+1] = array[j+1], array[j]
def main():
    c1 = Constraint("[4,5]")
    c2 = Constraint("[0,0]")
    c3 = Constraint("[4,5]")
    c4 = Constraint("[0,1)")
    c5 = Constraint("(2,3)")
    b1 = BracketNum('6', Bracket.LO)
    b2 = BracketNum('6', Bracket.LC)
    b3 = BracketNum('+', Bracket.RO)
    b4 = BracketNum('7', Bracket.LC)
    b5 = BracketNum('6', Bracket.LO)
    compl1, flag1 = c2.complement()
    print(flag1)
    for c in compl1:
        print(c.show())
    print("-----------------------------")
    l = [c5, c3, c2, c1, c4]
    #lqsort(l, 0, 3)
    lbsort(l)
    for c in l:
        print(c.show())
    print("-----------------------------")
    unl = unintersect_intervals(l)
    for c in unl:
        print(c.show())
    print("-----------------------------")
    cunl = complement_intervals(unl)
    for c in cunl:
        print(c.show())
    print("-----------------------------")
    print(c1.isPoint())
    print(c2.isPoint())
    print(c4.isPoint())
    print(c5.isPoint())
    print("------------------------------")
    c6 = Constraint("(3,+)")
    print(c6.isininterval(3))
    print("---------------------------------")
    print(min_constraints_number([c3]))
    print(min_constraint_number(Constraint("(0,0)")))
    print(min_constraint_number(c2))
    print(min_constraint_number(c4))
    print(min_constraints_number([c2, c5]))
    print(min_constraints_number([c3, c5]))
    print("---------------------constraint_subset-------------")
    print(constraint_subset(Constraint("[1,2]"), Constraint("(1,3)")))
    print(constraint_subset(Constraint("(1,2]"), Constraint("(1,3)")))
    print(constraint_subset(Constraint("(1,2]"), Constraint("(1,2)")))
    print(constraint_subset(Constraint("[1,1]"), Constraint("(0,3)")))
    print(constraint_subset(Constraint("(1,+)"), Constraint("(1,2)")))
    print(constraint_subset(Constraint("(2,4)"), Constraint("(1,4)")))
    print("-----------------issubset-----------------------")
    print(Constraint("[1,2]").issubset(Constraint("(1,3)")))
    print(Constraint("(1,2]").issubset(Constraint("(1,3)")))
    print(Constraint("(1,+)").issubset(Constraint("(1,2)")))

if __name__=='__main__':
	main()
