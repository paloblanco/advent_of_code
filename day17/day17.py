from itertools import cycle
from dataclasses import dataclass, field
from collections import defaultdict

TEST_NAME = r"day17input_test.txt"
INPUT_NAME = r"day17input.txt"

SHAPES = [
    [
        [1,1,1,1]
    ],

    [
        [0,1,0,],
        [1,1,1,],
        [0,1,0,]
    ],

    [
        [0,0,1],
        [0,0,1],
        [1,1,1],
    ],

    [
        [1],
        [1],
        [1],
        [1],
    ],

    [
        [1,1],
        [1,1],
    ],
]

def return_shape_tuple(shape: list[list[int]]):
    pairs = []
    for j,row in enumerate(shape):
        for i,col in enumerate(row):
            if col==1:
                pairs.append([i,j]) # x y coordinates!!
    return pairs

def get_input_data(fname = TEST_NAME):
    with open(fname) as f:
        jets = list(f.read().strip())
    replacing = {
        "<":-1,
        ">":1
    }
    jets = [replacing[each] for each in jets]
    return jets

@dataclass
class Map:
    width: int = 7
    height: int = 0
    solid_container: set = field(default_factory=set)

    def mget(self,x,y):
        if x<0 or x >= self.width:
            return 1
        elif y > 0:
            return 1
        else:
            return 1 if (x,y) in self.solid_container else 0

    def mset(self,x,y):
        self.height = min(self.height,y-1)
        assert (x,y) not in self.solid_container, "this is already here!"
        self.solid_container.add((x,y))

    
def part1(fname=TEST_NAME, rock_count = 2022):
    jets = get_input_data(fname)
    shape_factory = cycle(SHAPES)
    jet_factory = cycle(jets)
    map = Map()
    current_shape = None
    rocks=0
    while rocks < rock_count:
        # make if needed
        if not current_shape:
            shape_raw = next(shape_factory)
            current_shape = return_shape_tuple(shape_raw)
            move_shape_up = len(shape_raw)-1
            for i in range(len(current_shape)):
                current_shape[i][0] += 2
                current_shape[i][1] += -move_shape_up + map.height - 3
        # shape hit by jets
        jet = next(jet_factory)
        for i in range(len(current_shape)):
            current_shape[i][0] += jet
        collide = 0
        for i,(x,y) in enumerate(current_shape):
            collide += map.mget(x,y)
        if collide:
            for i in range(len(current_shape)):
                current_shape[i][0] += -jet
        # fall
        for i in range(len(current_shape)):
            current_shape[i][1] += 1
        collide = 0
        for i,(x,y) in enumerate(current_shape):
            collide += map.mget(x,y)
        if collide:
            for i,(x,y) in enumerate(current_shape):
                map.mset(x,y-1)
            current_shape = None
            rocks += 1
    return map.height


if __name__ == "__main__":
    height_part1 = part1()
    print(f"{height_part1=}")
    