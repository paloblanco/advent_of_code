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

def return_sensors_with_radii(t):
    sensor_radii = defaultdict(int)
    for (xs,ys), (xb,yb) in t:
        man_dist = abs(xs-xb) + abs(ys-yb)
        sensor_radii[(xs,ys)] = man_dist
    return sensor_radii

def collide(point,s_r):
    x = point[0]
    y = point[1]
    for (xs,ys), d in s_r.items():
        dd = abs(x-xs) + abs(y-ys)
        if dd <= d:
            return True
    return False

def part1(fname=TEST_NAME, ytarget: int = 10):
    t,b = return_tuples_from_file(fname)
    sensors = {(each[0][0],each[0][1]) for each in t}
    beacons = {(each[1][0],each[1][1]) for each in t}
    exclude_count = 0
    sensors_with_radii = return_sensors_with_radii(t)
    maxd = max([d for d in sensors_with_radii.values()])
    minx = b[0] - maxd
    maxx = b[2] + maxd
    for x in range(minx,maxx+1):
        point = (x,ytarget)
        if (collide(point,sensors_with_radii)) and (not point in beacons):
            exclude_count += 1
    return exclude_count
    

if __name__ == "__main__":
    test1 = part1()
    print(f"{test1 =}")

    part1_solve = part1(INPUT_NAME, ytarget=2000000)
    print(f"{part1_solve =}") # 4254101 too low