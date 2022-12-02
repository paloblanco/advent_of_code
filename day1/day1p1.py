elves_fname = r"input1.txt"

with open(elves_fname,"r") as elves_file:
    elves_entries = elves_file.readlines()
    elves_totals=[]
    current_total=0
    for entry in elves_entries:
        entry=entry.strip()
        if entry:
            current_total += int(entry)
        else:
            elves_totals.append(current_total)
            current_total = 0
    elves_totals.append(current_total)

print(f"Max cals carried by one elf: {max(elves_totals)}")

elves_totals.sort()
print(f"Cals held by the three top elves: {sum(elves_totals[-3:])}")
