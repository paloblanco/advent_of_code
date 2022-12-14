from collections import defaultdict
from dataclasses import dataclass, field

TEST_NAME = "day14input_test.txt"
INPUT_NAME = "day14input.txt"

def get_tuples_from_file(fname=TEST_NAME):
    tuple_list = []
    with open(fname,"r") as tuple_file:
        for line in tuple_file:
            line=line.strip().split(" -> ")
            row = [[int(e) for e in each.split(",")] for each in line]
            tuple_list.append(row)
    return tuple_list

def get_numbers_between(n1,n2):
    if abs(n1-n2) <= 1:
        return []
    elif n1 > n2:
        return list(range(n2+1,n1))
    else:
        return list(range(n1+1,n2))

    
def make_map_from_tuples(tuple_list):
    map = defaultdict(int)
    b = [500,0,500,0] # bounds = minx,miny,maxx,maxy
    for row in tuple_list:
        for i,(x,y) in enumerate(row):
            map[(x,y)] = 1
            b = [min(x,b[0]),min(y,b[1]),max(x,b[2]),max(y,b[3])]
            if i==0: continue
            xprev,yprev = row[i-1]
            for xx in get_numbers_between(x,xprev) or [x,]:
                for yy in get_numbers_between(y,yprev) or [y,]:
                    map[(xx,yy)] = 1
    return map,b
            
def draw_map(map,b):
    xoffset = b[0]
    width = b[2] - xoffset
    map_str = [["." for each in range(width+1)] for r in range(b[3]+1)]
    chars = {
        0:".",
        1:"#",
        2:"+",
        3:"O"
    }
    for (x,y),val in map.items():
        map_str[y][x-xoffset]=chars[val]
    map_str = [''.join(row) for row in map_str]
    for row in map_str:
        print(row)

def part1(fname=TEST_NAME):
    tuples = get_tuples_from_file(fname)
    map,b = make_map_from_tuples(tuples)
    draw_map(map,b)
    settled_sand = 0
    dead_sand=False
    while not dead_sand: #break out when sand is gone
        xsand = 500
        ysand = 0
        while True:
            # draw_map(map,b)
            map[(xsand,ysand)]=0
            
            # input()
            ysand += 1
            if map[(xsand,ysand)] > 0:
                xsand += -1
                if map[(xsand,ysand)] > 0:
                    xsand += 2
                    if map[(xsand,ysand)] > 0:
                        xsand += -1
                        ysand += -1
                        map[(xsand,ysand)] = 3
                        settled_sand += 1
                        break
            map[(xsand,ysand)]=2
            if ysand >= b[3] or xsand < b[0] or xsand > b[2]:
                dead_sand = True
                print(f"Dead sand {(xsand, ysand)}  {b}")
                break
    draw_map(map,b)
    return settled_sand                


if __name__ == "__main__":
    sand_count_test = part1()
    print(f"{sand_count_test=}")

    sand_count_part1 = part1(INPUT_NAME)
    print(f"{sand_count_part1=}")
