TEST_NAME = "day18input_test.txt"
INPUT_NAME = "day18input.txt"

def read_cube_file_into_set(fname=TEST_NAME) -> set[tuple[int,int,int]]:
    cubes = set()
    with open(fname) as cube_file:
        for line in cube_file:
            cube = tuple(int(each) for each in line.strip().split(","))
            cubes.add(cube)
    return cubes

def part1(fname=TEST_NAME):
    cubes = read_cube_file_into_set(fname)
    sides = 0
    for x,y,z in cubes:
        adjacent=0
        for dx in [-1,1]:
            if (x+dx,y,z) in cubes:
                adjacent += 1
        for dy in [-1,1]:
            if (x,y+dy,z) in cubes:
                adjacent += 1
        for dz in [-1,1]:
            if (x,y,z+dz) in cubes:
                adjacent += 1
        sides += 6-adjacent
    return sides

def part2(fname=TEST_NAME):
    cubes = read_cube_file_into_set(fname)
    lenx = max([x for x,y,z in cubes])
    leny = max([y for x,y,z in cubes])
    lenz = max([z for x,y,z in cubes])
    minx,miny,minz = -1,-1,-1
    box_size = (lenx+2)*(leny+2)*(lenz+2)

    # comb outer space, count blocks we can reach
    frontier = []
    explored = set()
    startcube = (minx,miny,minz)
    frontier.append(startcube)
    explored.add(startcube)
    sides_touched = 0
    while frontier:
        x,y,z = frontier.pop()
        neighbors = [
            [x+1,y,z],
            [x-1,y,z],
            [x,y+1,z],
            [x,y-1,z],
            [x,y,z+1],
            [x,y,z-1],
            ]
        for xnew,ynew,znew in neighbors:
            if xnew < minx or xnew > lenx+2: continue
            if ynew < miny or ynew > leny+2: continue
            if znew < minz or znew > lenz+2: continue
            if (xnew,ynew,znew) in cubes: sides_touched += 1
            if (xnew,ynew,znew) in cubes or (xnew,ynew,znew) in explored:
                continue
            explored.add((xnew,ynew,znew))
            frontier.append((xnew,ynew,znew))
    print(f"{sides_touched=}")
    return sides_touched

if __name__ == "__main__":
    test1 = part1()
    print(f"{test1=}")

    real1 = part1(INPUT_NAME)
    print(f"{real1=}")

    test2 = part2()
    print(f"{test2=}")

    real2 = part2(INPUT_NAME)
    print(f"{real2=}") # 4504 too high, 2549 too low
    
