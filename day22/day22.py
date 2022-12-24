TEST_NAME = r"day22input_test.txt"
INPUT_NAME = r"day22input.txt"

EMPTY = 0
FLOOR = 1
WALL  = 2

TEXT2MAP = {
    " ":EMPTY,
    ".":FLOOR,
    "#":WALL
}

class Map:

    def __init__(self,fname = TEST_NAME):
        self._map, self._directions = self.make_map_from_file(fname)
        self._directions = self.fix_directions(self._directions)
        self.direction = 0
        self.height = len(self._map)
        self.width = len(self._map[0])
        
    def mget(self,x,y):
        return self._map[y-1][x-1]

    @staticmethod
    def fix_directions(directions: str):
        dir_list = []
        new_fig = ""
        for letter in directions:
            if letter in ["L","R"]:
                if new_fig:
                    dir_list.append(int(new_fig))
                    new_fig=""
                dir_list.append(letter)
            else:
                new_fig += letter
        if new_fig:
            dir_list.append(int(new_fig))
        return dir_list


    @staticmethod
    def make_map_from_file(fname=TEST_NAME):
        rows=[]
        maxrow = 0
        directions = None
        with open(fname) as f:
            for line in f:
                line=line[:-1]
                if not line:
                    line = next(f).strip()
                    directions = line
                    break
                row = list(line)
                row = [TEXT2MAP[e] for e in row]
                maxrow = max(len(row),maxrow)
                rows.append(row)
        print(f"{maxrow=}")
        for i,row in enumerate(rows):
            if (rr:=len(row)) < maxrow:
                zeros = [0,] * (maxrow-rr)
                rows[i] = row + zeros
        return rows, directions

DIRECTIONS = [
    (1,0),
    (0,1),
    (-1,0),
    (0,-1),
]

def part1(fname=TEST_NAME):
    map = Map(fname)
    x,y = 1,1
    while map.mget(x,y) != 1:
        x += 1
    direction = 0
    instructions = map._directions
    for step in instructions:
        if step=="L":
            direction = (direction - 1)%4
        elif step=="R":
            direction = (direction + 1)%4
        else:
            for i in range(step):
                dx,dy = DIRECTIONS[direction]
                nx,ny = x+dx,y+dy
                #wrap if needed
                if nx > map.width: nx = 1
                if nx < 1: nx = map.width
                if ny > map.height: ny = 1
                if ny < 1: ny = map.height
                while map.mget(nx,ny)==0:
                    nx,ny = nx+dx,ny+dy
                    if nx > map.width: nx = 1
                    if nx < 1: nx = map.width
                    if ny > map.height: ny = 1
                    if ny < 1: ny = map.height
                if map.mget(nx,ny)==2:
                    break
                x,y = nx,ny
    print(f"{x=}   {y=}   {direction=}")
    return 4*x + 1000*y + direction

ZONES = [
    [0,1,2],
    [0,3,0],
    [4,5,0],
    [6,0,0]
]

def get_zone(x,y):
    return ZONES[(y-1)//50][(x-1)//50]

def part2(fname=TEST_NAME):
    map = Map(fname)
    x,y = 1,1
    while map.mget(x,y) != 1:
        x += 1
    direction = 0
    instructions = map._directions
    for step in instructions:
        if step=="L":
            direction = (direction - 1)%4
        elif step=="R":
            direction = (direction + 1)%4
        else:
            for i in range(step):
                zone_now = get_zone(x,y)
                # print(f"{x=}   {y=}   {zone_now=}")
                dx,dy = DIRECTIONS[direction]
                dnew=direction
                nx,ny = x+dx,y+dy
                #wrap if needed
                if dx > 0:
                    if nx > map.width or map.mget(nx,ny)==0:
                        match zone_now:
                            case 2:
                                nx=100
                                dnew=2
                                ny=100+(51-ny)
                            case 3:
                                ny=50
                                dnew=3
                                nx=100+(ny-50) 
                            case 5:
                                nx=150
                                dnew=2
                                ny=151-ny
                            case 6:
                                ny=150
                                dnew=3
                                nx=50+(ny-150)
                elif dx < 0:
                    if nx < 1 or map.mget(nx,ny)==0:
                        match zone_now:
                            case 1:
                                nx=1
                                dnew=0
                                ny=100+(51-ny)
                            case 3:
                                ny=101
                                dnew=1
                                nx = ny-50
                            case 4:
                                nx=51
                                dnew=0
                                ny=151-ny
                            case 6:
                                ny=1
                                dnew=1
                                nx = ny-100
                elif dy > 0:
                    if ny > map.height or map.mget(nx,ny)==0:
                        match zone_now:
                            case 2:
                                nx=100
                                dnew=2
                                ny=50+nx-100
                            case 5:
                                nx=50
                                dnew=2
                                ny=150+nx-50
                            case 6:
                                ny=1
                                dnew=1
                                nx=nx+100
                elif dy < 0:
                    if ny < 1 or map.mget(nx,ny)==0:
                        match zone_now:
                            case 2:
                                ny=200
                                dnew=3
                                nx=nx-100
                            case 1:
                                nx=1
                                dnew=0
                                ny=150+nx-50
                            case 4:
                                nx=50
                                dnew=0
                                ny=50+nx
                if map.mget(nx,ny)==WALL:
                    break
                x,y, direction = nx,ny,dnew
    print(f"{x=}   {y=}   {direction=}")
    return 4*x + 1000*y + direction


if __name__ == "__main__":
    pwtest = part1()
    print(f"{pwtest=}")

    pw1 = part1(INPUT_NAME)
    print(f"{pw1=}")
    
    pwtest2 = part2(INPUT_NAME)
    print(f"{pwtest2=}") # pwtest2=55370 too low