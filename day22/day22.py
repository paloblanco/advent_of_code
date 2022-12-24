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


if __name__ == "__main__":
    map = Map(TEST_NAME)
    for r in map._map:
        print(r)
    print(map._directions)