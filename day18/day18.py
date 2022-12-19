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

if __name__ == "__main__":
    test1 = part1()
    print(f"{test1=}")

    real1 = part1(INPUT_NAME)
    print(f"{real1=}")
    
