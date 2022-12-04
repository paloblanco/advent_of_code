ASSIGNMENTS_FNAME = "day4input.txt"

def return_assignments_from_file(fname=ASSIGNMENTS_FNAME):
    with open(fname,"r") as assignments_file:
        assignments_lines=[each.strip() for each in assignments_file.readlines()]
    assignments_pairs=[each.split(",") for each in assignments_lines]
    ap = assignments_pairs
    assignments_nums = [[[int(each) for each in bnds.split("-")] for bnds in pair] for pair in ap]
    return assignments_nums

def fully_contain(pair1, pair2):
    return pair1[0] <= pair2[0] and pair1[1] >= pair2[1]

def fully_contain_both_ways(pair1,pair2):
    return fully_contain(pair1,pair2) or fully_contain(pair2,pair1)

def overlapping_ranges(pair1,pair2):
    return pair1[0]<=pair2[1] and pair1[1]>=pair2[0]

def count_overlapping_pairs(fname=ASSIGNMENTS_FNAME,over_func=fully_contain_both_ways):
    assignments = return_assignments_from_file(fname=fname)
    print(f"Total assignments pairs: {len(assignments)}")
    count_fully_contains=0
    for pair1,pair2 in assignments:
        if over_func(pair1,pair2):
            count_fully_contains += 1
    return count_fully_contains

if __name__ == "__main__":
    count_containing = count_overlapping_pairs()
    count_overlapping = count_overlapping_pairs(over_func=overlapping_ranges)
    print(f"Containing pairs count: {count_containing}")
    print(f"Overlapping pairs count: {count_overlapping}")