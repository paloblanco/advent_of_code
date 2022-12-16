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
    ranges = excluded_ranges_for_row(sensors_with_radii,ytarget)
    beacons_here = [beacon for beacon in beacons if beacon[1]==ytarget]
    for (x0,x1) in ranges:
        exclude_count += x1-x0+1
        for bx,_ in beacons_here:
            if x0<=bx<=x1:
                exclude_count += -1
    return exclude_count

def coalesce_ranges(e_r):
    e_r = sorted(e_r)
    new_ranges = []
    outer = enumerate(e_r)
    for ix,(x0,x1) in outer:
        xstart = x0
        xend = x1
        for jx,(xsnew,xenew) in enumerate(e_r[ix:]):
            if xsnew > xend+1:
                break
            xend = max(xend,xenew)
            try:
                next(outer) # tik the outer loop if needed
            except StopIteration:
                pass
        new_ranges.append((xstart,xend))
    return new_ranges

def excluded_ranges_for_row(s_r,ytarg):
    excluded_ranges = []
    for (x,y), d in s_r.items():
        width = d-abs(ytarg-y)
        if width >= 0:
            excluded_ranges.append((x-width,x+width))
    # need to coalesce the ranges
    fixed_ranges = coalesce_ranges(excluded_ranges)
    return fixed_ranges


def part2(fname=TEST_NAME, limit: int = 20):
    t,b = return_tuples_from_file(fname)
    sensors = {(each[0][0],each[0][1]) for each in t}
    beacons = {(each[1][0],each[1][1]) for each in t}
    sensors_with_radii = return_sensors_with_radii(t)
    xb,yb = -1,-1
    for y in range(limit+1):
        ranges = excluded_ranges_for_row(sensors_with_radii,y)
        for i,(x0,x1) in enumerate(ranges[1:]):
            if x0-1 > ranges[i][1]:
                xb,yb = x0-1,y
                break
        if xb != -1: break
    return xb*4000000 + yb

    
def part2_alt(fname=INPUT_NAME, limit: int = 4000000):
    t,b = return_tuples_from_file(fname)
    sensors = {(each[0][0],each[0][1]) for each in t}
    beacons = {(each[1][0],each[1][1]) for each in t}
    sensors_with_radii = return_sensors_with_radii(t)
    scale = 100/limit
    xoff=0
    yoff=0
    while scale < .999:
        map1 = [[1 for i in range(100)] for j in range(100)]
        for (x,y), d in sensors_with_radii.items():
            x,y,d = int(x*scale), int(y*scale), int(d*scale)
            for d0 in range(-d,d+1):
                y0 = y+d0
                if y0<yoff or y0>yoff+99:
                    continue
                xmin = max(xoff, x - (d - abs(d0)))
                xmax = min(xoff+99, x + (d - abs(d0)))
                for x0 in range(xmin,xmax+1):
                    map1[y0+yoff][x0+xoff]=0
        # find the 1
        xwin=-1
        ywin=-1
        for y,row in enumerate(map1):
            for x,val in enumerate(row):
                if val==1:
                    xwin,ywin=x,y
                    break
            if xwin>-1: break
        print(f"{xoff=}   {yoff=}   {scale=}")
        for row in map1:
            print(''.join([str(each) for each in row]))
        xoff = int(xoff+xwin/scale)
        yoff = int(yoff+ywin/scale)
        scale *= 100


if __name__ == "__main__":
    # test1 = part1()
    # print(f"{test1 =}")

    # part1_solve = part1(INPUT_NAME, ytarget=2000000)
    # print(f"{part1_solve =}") # 4254101 too low

    # p2test = part2()
    # print(f"{p2test=}")

    # p2 = part2(INPUT_NAME,limit=4000000)
    # print(f"{p2=}") # 13784551204480 is right

    part2_alt()