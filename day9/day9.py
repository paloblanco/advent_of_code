import pyxel

DAY9_FNAME = r"day9input.txt"

def return_file_as_sequence_of_steps(fname=DAY9_FNAME):
    with open(fname,"r") as day9_file:
        steps_order = [each.strip().split(" ") for each in day9_file.readlines()]
    steps_stack = []
    for direction, step_count in steps_order:
        for s in range(int(step_count)):
            steps_stack.append(direction)
    steps_stack = steps_stack[::-1]
    return steps_stack

DIRECTIONS = {
    "U": [0,-1],
    "D": [0,1],
    "L": [-1,0],
    "R": [1,0],
}

def move_rope(H,T,dx,dy):
    H[0] += dx
    H[1] += dy
    len_x = H[0] - T[0]
    len_y = H[1] - T[1]
    len_mag = abs(len_x) + abs(len_y)
    if abs(len_x) >= 2:
        T[0] += len_x // 2
        if len_mag >= 3: # need to move diagonally
            T[1] += len_y
    if abs(len_y) >= 2:
        T[1] += len_y // 2
        if len_mag >= 3: # need to move diagonally
            T[0] += len_x
    return H,T
    
def init_pyxel():
    pyxel.init(300, 200, title="AdventOfCode, Day9", fps=60, capture_scale=3, capture_sec=60)
    pyxel.camera(-50,-100)
    pyxel.cls(0)
    pyxel.flip()

def refresh_pyxel(H,T,Hc,Tc,flip=True):
    pyxel.pset(H[0],H[1],Hc)
    pyxel.pset(T[0],T[1],Tc)
    if flip: pyxel.flip()

def refresh_big_rope(knots,c,flip=True):
    for knot in knots:
        pyxel.pset(knot[0],knot[1],c)
    if flip: pyxel.flip()

def move_big_rope(knot0,knot1):
    len_x = knot0[0] - knot1[0]
    len_y = knot0[1] - knot1[1]
    len_mag = abs(len_x) + abs(len_y)
    if abs(len_x) >= 2:
        knot1[0] += len_x // 2
        if len_mag == 3: # need to move diagonally
            knot1[1] += len_y
    if abs(len_y) >= 2:
        knot1[1] += len_y // 2
        if len_mag == 3: # need to move diagonally
            knot1[0] += len_x
    return knot1

def simulate_rope(steps_stack, draw = False):
    if draw:
        init_pyxel()
    H = [0,0] #x position, y position
    T = [0,0]
    T_visited_set = set() # strings in format of x_y
    T_visited_set.add(f"{T[0]}_{T[1]}")
    while steps_stack:
        if draw: refresh_pyxel(H,T,0,2,False)
        new_move = steps_stack.pop()
        dx,dy = DIRECTIONS[new_move]
        H, T = move_rope(H,T,dx,dy)
        T_visited_set.add(f"{T[0]}_{T[1]}")
        if draw: 
            msg = f"Tail has visited: {len(T_visited_set)}"
            pyxel.rect(2,90,100,10,0)
            pyxel.text(2,90,msg,2)
            refresh_pyxel(H,T,7,6,True)
    if draw: pyxel.show()
    return len(T_visited_set)

def simulate_long_rope(steps_stack,rope_length=10,draw = False):
    if draw:
        init_pyxel()
    rope = [[0 for j in range(2)] for i in range(rope_length)]
    T_visited_set = set() # strings in format of x_y
    T_visited_set.add(f"{rope[-1][0]}_{rope[-1][1]}")
    while steps_stack:
        if draw: 
            refresh_big_rope(rope,0,flip=False)
            pyxel.pset(rope[-1][0],rope[-1][1],2)
        new_move = steps_stack.pop()
        dx,dy = DIRECTIONS[new_move]
        rope[0][0] += dx
        rope[0][1] += dy
        for ix in range(1,len(rope)):
            rope[ix] = move_big_rope(rope[ix-1], rope[ix])
        T_visited_set.add(f"{rope[-1][0]}_{rope[-1][1]}")
        if draw: 
            msg = f"Tail has visited: {len(T_visited_set)}"
            pyxel.rect(2,90,100,10,0)
            pyxel.text(2,90,msg,2)
            refresh_big_rope(rope,7,flip=True)
    return len(T_visited_set)

if __name__ == "__main__":
    steps = return_file_as_sequence_of_steps()
    tail_visited_count = simulate_rope(steps,draw=False)
    print(f"Tail has visited: {tail_visited_count}")
    steps = return_file_as_sequence_of_steps()
    tail_long_rope = simulate_long_rope(steps,rope_length=10,draw=False)
    print(f"Long Rope Tail has visited: {tail_long_rope}")
