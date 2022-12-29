from collections import defaultdict
from itertools import cycle,product

TEST_NAME = r"day23input_test.txt"
INPUT_NAME = r"day23input.txt"

def read_input_map(fname=TEST_NAME):
    with open(fname) as f:
        snowmap = [e.strip() for e in f.readlines()]
    elf_map = set()
    for r,row in enumerate(snowmap):
        for c,col in enumerate(list(row)):
            if col=="#":
                elf_map.add((r,c))
    return elf_map

DIRECTIONS = [
    [-1,0],
    [1,0],
    [0,-1],
    [0,1],
]

def part1(fname=TEST_NAME,turns=10):
    elf_map = read_input_map(fname)
    direction_turn = 0
    miny,maxy,minx,maxx = 0,0,0,0
    for t in range(turns):
        # consideration
        to_map = defaultdict(int)
        dir_map = {}
        for elf in elf_map:
            around_me = {(elf[0]+y,elf[1]+x) for y,x in product([-1,0,1],repeat=2)}
            if len(around_me & elf_map) < 1: 
                continue # noone else is around me, so break
            for d in range(4):
                direction = (d+direction_turn)%4 #changes each turn
                if direction//2==0: 
                    directions_add = [[0,-1],[0,0],[0,1]]
                else:
                    directions_add = [[-1,0],[0,0],[1,0]]
                yto,xto = DIRECTIONS[direction]
                yelf,xelf = elf
                check = {(yelf+yto+y,xelf+xto+x) for y,x in directions_add}
                to_full = len(check & elf_map) > 0
                if not to_full: # sum is 0, so go thhere!
                    to_map[(yelf+yto,xelf+xto)] += 1
                    dir_map[elf] = direction
                    break # get out of this inner direction loop
        # if to_map is more than 1 anywhere, those elves don't move
        for (y,x) in elf_map:
            if (y,x) not in dir_map: 
                continue #break out if this elf is not moving
            yplus,xplus = DIRECTIONS[dir_map[(y,x)]]
            yto,xto = y+yplus,x+xplus
            if to_map[(yto,xto)] > 1:
                continue # more than one elf wants to go here
            elf_map.remove((y,x))
            elf_map.add((yto,xto))
            miny = min([miny,y,yto])
            maxy = max([maxy,y,yto])
            minx = min([minx,x,xto])
            maxx = max([maxx,x,xto])
        direction_turn = (direction_turn+1)%4 #rotate through directions
    # get area
    area = (maxy-miny+1) * (maxx-minx+1)
    print(f"{area=}")
    print(f"{maxy=}   {miny=}   {maxx=}   {minx=}")
    return area - len(elf_map)
    

if __name__ == "__main__":
    test1 = part1()
    print(f"{test1=}")

            





    