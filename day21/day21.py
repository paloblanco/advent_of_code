from dataclasses import dataclass, field

TEST_NAME = r"day21input_test.txt"
INPUT_NAME = r"day21input.txt"

@dataclass
class Monkey:
    
    name: str
    _value: int = None
    left: 'Monkey' = None
    right: 'Monkey' = None
    oper: callable = None

    @property
    def value(self):
        if self._value==None:
            return self.oper(self.left.value,self.right.value)
        else:
            return self._value

OPERS = {
    "+": lambda x,y: x+y,
    "-": lambda x,y: x-y,
    "*": lambda x,y: x*y,
    "/": lambda x,y: x/y,
}

def get_monkeys_from_file(fname=TEST_NAME):
    monkeys = {}
    with open(fname) as f:
        for line in f:
            line=line.strip().split(" ")
            name = line[0][:4]
            if len(line) < 4:
                monkey = Monkey(name,int(line[1]))
                monkeys[name] = monkey
            else:
                monkey = Monkey(name, left = line[1],right=line[3],oper=OPERS[line[2]])
                monkeys[name] = monkey
    # go through again and link monkeys
    for i,monk in monkeys.items():
        if monk.left:
            monk.left = monkeys[monk.left]
        if monk.right:
            monk.right = monkeys[monk.right]
    return monkeys


def part1(fname=TEST_NAME):
    monkeys = get_monkeys_from_file(fname)
    return monkeys['root'].value

def between(value,b0,b1):
    return b1 < value  < b2 or b2 < value < b1

def part2(fname=TEST_NAME):
    monkeys = get_monkeys_from_file(fname)
    root = monkeys["root"]
    root.oper = lambda x,y: x-y
    humn = monkeys["humn"]
    
    def get_root(value):
        humn._value=value
        # print(humn)
        return root.value

    minh = -100000000000000
    maxh = 100000000000000
    minr = get_root(minh)
    maxr = get_root(maxh)
    newh = 0
    newr = get_root(newh)
    while newr != 0:
        minguess = (newh + minh)//2
        maxguess = (newh + maxh)//2
        minguessroot = get_root(minguess)
        maxguessroot = get_root(maxguess)
        if abs(minguessroot) < abs(maxguessroot):
            maxh=newh
            newr = minguessroot
            newh = minguess
        else:
            minh = newh
            newr = maxguessroot
            newh = maxguess
        print(f"{minh=}    {newh=}    {maxh=}    {newr=}")
    print(newr)
    return newh


if __name__ == "__main__":
    test1root = part1()
    print(f"{test1root=}")

    part1root = part1(INPUT_NAME)
    print(f"{part1root=}")

    test2 = part2()
    print(f"{test2=}")

    p2 = part2(INPUT_NAME)
    print(f"{p2=}")
