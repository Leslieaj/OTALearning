#OTA equivalence

from ota import *

def get_regions(max_time_value, closed_flag):
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

def main():
    paras = sys.argv
    A,_ = buildRTA(paras[1])
    A.show()
    print("--------------max value---------------------")
    max_time_value, closed_flag = A.max_time_value()
    print(max_time_value, closed_flag)
    print("--------------all regions---------------------")
    regions = get_regions(max_time_value, closed_flag)
    for r in regions:
        print(r.show())

if __name__=='__main__':
	main()
