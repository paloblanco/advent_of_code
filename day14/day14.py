from collections import defaultdict
import pyxel

TEST_NAME = "day14input_test.txt"
INPUT_NAME = "day14input.txt"

def init_pyxel():
    pyxel.init(120, 200, title="AdventOfCode, Day 14", fps=60, capture_scale=3, capture_sec=60)
    pyxel.cls(0)
    pyxel.text(16,5,"Advent of Code Day 14",3)
    pyxel.flip()

def pyxel_map(map,xmin):
    xs=24
    ys=16
    pyxel.rect(xs,ys,72,171,1)
    for (x,y) in map.keys():
        pyxel.pset(x-xmin+xs,y+ys,3)
    pyxel.flip()

def pset(x,y,xmin,c=3):
    xs=24
    ys=16
    pyxel.pset(x-xmin+xs,y+ys,c)
    pyxel.flip()


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
    framecount=0
    modulo=2
    msec=0
    tuples = get_tuples_from_file(fname)
    map,b = make_map_from_tuples(tuples)
    if DRAW:
        init_pyxel()
        pyxel_map(map,b[0])
    # draw_map(map,b)
    settled_sand = 0
    dead_sand=False
    while not dead_sand: #break out when sand is gone
        xsand = 500
        ysand = 0
        xold=500
        yold=0
        while True: # break when sand settles or sand is dead (out of bounds)
            framecount = (framecount+1)%modulo
            msec = (msec+1)%100
            if msec==0: modulo += 1
            map[(xsand,ysand)]=0
            if DRAW and framecount==1: pset(xold,yold,b[0],1)
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
                        if DRAW: pset(xsand,ysand,b[0],15)
                        break
            map[(xsand,ysand)]=2
            if DRAW and framecount==0: 
                pset(xsand,ysand,b[0],15)
                xold=xsand
                yold=ysand
            if ysand >= b[3] or xsand < b[0] or xsand > b[2]:
                dead_sand = True
                print(f"Dead sand {(xsand, ysand)}  {b}")
                break
    # draw_map(map,b)
    print(b)
    if DRAW: pyxel.show()
    return settled_sand                

def part2(fname=TEST_NAME):
    tuples = get_tuples_from_file(fname)
    map,b = make_map_from_tuples(tuples)
    draw_map(map,b)
    settled_sand = 0
    while True: # break out when sand fills to top
        xsand = 500
        ysand = 0
        if map[(xsand,ysand)]==3: 
            break
        while True: # break out when sand settles
            map[(xsand,ysand)]=0
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
            if ysand >= b[3] + 1:
                map[(xsand,ysand)] = 3
                settled_sand += 1
                break
    xall = [x for (x,y) in map.keys()]
    yall = [y for (x,y) in map.keys()]
    b = [min(xall),min(yall),max(xall),max(yall)]
    draw_map(map,b)
    return settled_sand


if __name__ == "__main__":
    # sand_count_test = part1()
    # print(f"{sand_count_test=}")

    DRAW=True
    sand_count_part1 = part1(INPUT_NAME)
    print(f"{sand_count_part1=}")

    # sand_count_test2 = part2()
    # print(f"{sand_count_test2=}")

    # sand_count_part2 = part2(INPUT_NAME)
    # print(f"{sand_count_part2=}")
