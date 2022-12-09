import pyxel

elves_fname = r"input1.txt"

DRAW = True

def init_pyxel():
    pyxel.init(256, 200, title="AdventOfCode, Day1", fps=60, capture_scale=3, capture_sec=60)
    pyxel.cls(0)
    pyxel.flip()

draw_cursor = [0,0] # x,y

def refresh(ynew=0, dc=draw_cursor):
    scale = 190.0/71000.0
    ynew = 190-ynew*scale
    yold = 190 - dc[1]*scale
    pyxel.line(dc[0],yold,dc[0],ynew,7)
    pyxel.flip()

if DRAW: init_pyxel()

with open(elves_fname,"r") as elves_file:
    elves_entries = elves_file.readlines()
    elves_totals=[]
    current_total=0
    for entry in elves_entries:
        entry=entry.strip()
        if entry:
            current_total += int(entry)
            if DRAW:
                refresh(current_total,draw_cursor)
                draw_cursor[1] = current_total
        else:
            elves_totals.append(current_total)
            current_total = 0
            if DRAW:
                draw_cursor[0] = draw_cursor[0] + 1
                draw_cursor[1] = 0
    elves_totals.append(current_total)

print(f"Total elves: {len(elves_totals)}")
print(f"Max cals carried by one elf: {max(elves_totals)}")

elves_totals.sort()
print(f"Cals held by the three top elves: {sum(elves_totals[-3:])}")

if DRAW:pyxel.show()