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
    box_size = (lenx+2)*(leny+2)*(lenz+2)

    # comb outer space, count blocks we can reach
    frontier = []
    explored = set()
    startcube = (0,0,0)
    frontier.append(startcube)
    explored.add(startcube)
    while frontier:
        x,y,z = frontier.pop()
        for dx in [-1,1]:
            if x+dx < 0 or x+dx > lenx+2: 
                continue
            if (x+dx,y,z) in cubes or (x+dx,y,z) in explored:
                continue
            explored.add((x+dx,y,z))
            frontier.append((x+dx,y,z))
        for dy in [-1,1]:
            if y+dy < 0 or y+dy > leny+2: 
                continue
            if (x,y+dy,z) in cubes or (x,y+dy,z) in explored:
                continue
            explored.add((x,y+dy,z))
            frontier.append((x,y+dy,z))
        for dz in [-1,1]:
            if z+dz < 0 or z+dz > lenz+2: 
                continue
            if (x,y,z+dz) in cubes or (x,y,z+dz) in explored:
                continue
            explored.add((x,y,z+dz))
            frontier.append((x,y,z+dz))
    outer_bubble = len(explored)
    
    pockets = set()
    sides = 0
    for x,y,z in cubes:
        adjacent=0
        for dx in [-1,1]:
            if (x+dx,y,z) in cubes:
                adjacent += 1
            elif (x+dx,y,z) not in explored:
                pockets.add((x+dx,y,z))
        for dy in [-1,1]:
            if (x,y+dy,z) in cubes:
                adjacent += 1
            elif (x,y+dy,z) not in explored:
                pockets.add((x,y+dy,z))
        for dz in [-1,1]:
            if (x,y,z+dz) in cubes:
                adjacent += 1
            elif (x,y,z+dz) not in explored:
                pockets.add((x,y,z+dz))
        sides += 6-adjacent

    print(f"{pockets=}")
    for x,y,z in pockets:
        adjacent_solids = 0
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                for dz in [-1,0,1]:
                    if (x+dx,y+dy,z+dz) in cubes:
                        # print((x+dx,y+dy,z+dz))
                        adjacent_solids += 1
    return sides - adjacent_solids

if __name__ == "__main__":
    test1 = part1()
    print(f"{test1=}")

    real1 = part1(INPUT_NAME)
    print(f"{real1=}")

    test2 = part2()
    print(f"{test2=}")

    real2 = part2(INPUT_NAME)
    print(f"{real2=}")
    
