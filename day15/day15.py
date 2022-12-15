from collections import defaultdict
from dataclasses import dataclass, field

INPUT_NAME = r"day15input.txt"
TEST_NAME = r"day15input_test.txt"


def return_tuples_from_file(fname=TEST_NAME):
    tuple_list=[]
    bx = [] #bounds
    by = []
    with open(fname) as input_file:
        for line in input_file:
            line = line.strip().split()
            x0 = int(line[2][2:-1])
            y0 = int(line[3][2:-1])
            x1 = int(line[8][2:-1])
            y1 = int(line[9][2:])
            bx = bx + [x0,x1]
            by = by + [y0,y1]
            tuple_list.append([(x0,y0),(x1,y1)])
    b = [min(bx),min(by),max(bx),max(by)]
    return tuple_list, b

EMPTY   = 0
SENSOR  = 1
BEACON  = 2
EXCLUDE = 3

def get_tuples_in_range(x: int,y: int,d: int):
    if d == 0: return []
    tups = []
    for yy in range(y-d,y+d+1):
        dx = d-abs(yy-y)
        xx = x-dx
        tups.append((xx,yy,2*dx+1))
    return tups


def make_exclusion_map_from_data(tuple_list: list[list[tuple[int,int]]]):
    map = defaultdict(int)
    minx = []
    for (xs,ys), (xb,yb) in tuple_list:
        # map[(xs,ys)] = SENSOR
        man_dist = abs(xs-xb) + abs(ys-yb)
        tups_exclude = get_tuples_in_range(xs,ys,man_dist)
        for xe,ye,d in tups_exclude:
            map[(xe,ye)] = d
            minx.append(xe)
    return map, min(minx)

def part1(fname=TEST_NAME, ytarget: int = 10):
    t,b = return_tuples_from_file(fname)
    sensors = {(each[0][0],each[0][1]) for each in t}
    beacons = {(each[1][0],each[1][1]) for each in t}
    map,minx = make_exclusion_map_from_data(t)
    exclude_count = 0
    str_row = ""
    x_range_build = range(minx,b[2]+1) 
    x_range_solve = range(b[0],b[2]+1) 
    thisrow = defaultdict(int)
    for x in x_range_build:
        val = map[(x,ytarget)]
        if val == 0: 
            continue
        for i in range(val):
            thisrow[x+i]=1
        print(f"{x=}  {val=}")
    row = ""
    for x in x_range_solve: 
        row += str(thisrow[x])
    print(row)
    for x in x_range_solve:
        if (x,ytarget) not in beacons:
           exclude_count+=thisrow[x] 
        else:
            print("beacon!")
    return exclude_count


if __name__ == "__main__":
    test1 = part1()
    print(f"{test1 =}")

    # part1_solve = part1(INPUT_NAME, ytarget=2000000)
    # print(f"{part1_solve =}")