DAY10_FNAME = r"day10input.txt"


import pyxel

def init_pyxel():
    pyxel.init(128, 128, title="AdventOfCode, Day10", fps=30, capture_scale=3, capture_sec=60)
    pyxel.load("my_resource.pyxres")
    pyxel.cls(0)
    pyxel.bltm(0,0,0,0,0,128,128)
    pyxel.text(40,20,"AoC Day 10", 1)
    pyxel.text(5,120,"NormGear -- CRT matrix display", 5)
    pyxel.flip()

def refresh_pyxel(x,y,c):
    offx = 20
    offy = 40
    scale = 2
    px = x*scale + offx
    py = y*scale + offy
    pyxel.rect(px,py,scale,scale,c)
    pyxel.flip()

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

def render_text(text_list: list[str]) -> str:
    text_out = ""
    for i,text in enumerate(text_list):
        if DRAW:
            drawx = i%40
            drawy = i//40
            color = 1 if text=="." else 6
            refresh_pyxel(drawx,drawy,color)
        text_out = text_out + text
        if (i+1)%40==0:
            text_out = text_out + "\n"
    return text_out

def run_program(instructions:list, track_start=20, track_interval=40) -> int:
    if DRAW: init_pyxel()
    cycle = 1
    X = 1
    strength_sum = 0
    text_output = [".",]*240
    while instructions:
        next_instruction = instructions.pop()
        dX,dcycle = process_instruction(next_instruction)
        for i in range(dcycle):
            pix = cycle-1
            if X-1<=(pix%40)<=X+1:
                text_output[pix]="#"
            if (cycle-track_start)%track_interval==0:
                strength_sum += X * cycle
            cycle += 1
        X += dX
    text_output = render_text(text_output)
    return strength_sum, text_output

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
    DRAW=False
    instr_test = get_instructions_from_text(TEST_DATA)
    sum_test, text_test = run_program(instr_test)
    assert sum_test==13140 , f"Wrong, your value is {sum_test}"
    print("Test Text:")
    print(text_test)

    DRAW=True
    instr_real = get_instructions_from_text(get_text_from_file())
    sum_real, text_real = run_program(instr_real)
    print(f"Sum strength: {sum_real}")
    print("Real Text:")
    print(text_real)
    if DRAW: pyxel.show()