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
        if not self._value:
            self._value = self.oper(self.left.value,self.right.value)
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


if __name__ == "__main__":
    test1root = part1()
    print(f"{test1root=}")

    part1root = part1(INPUT_NAME)
    print(f"{part1root=}")

