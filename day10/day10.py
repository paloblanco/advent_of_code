DAY10_FNAME = r"day10input.txt"

def get_text_from_file(fname: str=DAY10_FNAME) -> str:
    with open(fname,"r") as f:
        return f.read()

def get_instructions_from_text(text: str) -> list[list[any]]:
    instructions_list = text.splitlines()
    for i in range(len(instructions_list)):
        if "noop" in instructions_list[i]:
            instructions_list[i] = None
        else:
            instructions_list[i] = int(instructions_list[i].split(" ")[1])
    return instructions_list[::-1] #can pop off instructions

def process_instruction(instr):
    if instr is None:
        return 0,1
    else:
        return instr,2

def run_program(instructions:list, track_start=20, track_interval=40) -> int:
    cycle = 1
    X = 1
    strength_sum = 0
    while instructions:
        next_instruction = instructions.pop()
        dX,dcycle = process_instruction(next_instruction)
        for i in range(dcycle):
            if (cycle-track_start)%track_interval==0:
                strength_sum += X * cycle
            cycle += 1
        X += dX
    return strength_sum

TEST_DATA = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

if __name__ == "__main__":
    instr_test = get_instructions_from_text(TEST_DATA)
    sum_test = run_program(instr_test)
    assert sum_test==13140 , f"Wrong, your value is {sum_test}"

    instr_real = get_instructions_from_text(get_text_from_file())
    sum_real = run_program(instr_real)
    print(f"Sum strength: {sum_real}")