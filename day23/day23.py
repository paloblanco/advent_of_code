from collections import defaultdict
from itertools import cycle,product

TEST_NAME = r"day23input_test.txt"
INPUT_NAME = r"day23input.txt"

def read_input_map(fname=TEST_NAME):
    with open(fname) as f:
        snowmap = [e.strip for e in f.readlines()]
    elf_map = defaultdict(int)
    for r,row in enumerate(snowmap):
        for c,val in enumerate(row):
            if val=="#":
                elf_map[(r,c)] = 1
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
    for t in range(turns):
        # consideration
        to_map = defaultdict(int)
        dir_map = defaultdict(int)
        for elf,val in elf_map.items():
            if val != 1: continue # only consider elves, not blanks
            around_me = sum([elf_map[(elf[0]+y,elf[1]+x)] for y,x in product([-1,0,1],repeat=2)])
            if around_me == 1: continue # noone else is around me, so break
            for d in range(4):
                direction = (d+direction_turn)%4 #changes each turn
                if direction//2==0: 
                    directions_add = [[0,-1],[0,0],[0,1]]
                else:
                    directions_add = [[-1,0],[0,0],[1,0]]
                yto,xto == DIRECTIONS[direction]
                yelf,xelf = elf
                check = [(yelf+yto+y,xelf+xto+x) for y,x in directions_add]
                to_full = sum([elf_map[loc] for loc in check])
                if not to_full: # sum is 0, so go thhere!
                    to_map[elf] += 1
                    dir_map[elf] = direction
                    break # get out of this loop




    