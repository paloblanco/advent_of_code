from collections import defaultdict

RUCKSACKS_FNAME = r"input_day3.txt"

def get_priority(letter: str) -> int:
    assert len(letter)==1, "Can only pass single characters"
    my_ord = ord(letter)
    if my_ord >= 97: # lowercase
        return my_ord - 96
    else: #uppercase
        return my_ord - 65 + 27 

def return_rucksacks(fname = RUCKSACKS_FNAME) -> list:
    with open(fname, "r") as rucksacks_file:
        rucksacks_lists = rucksacks_file.readlines()
    rucksacks_lists = [each.strip() for each in rucksacks_lists]
    print(f"Rucksack count: {len(rucksacks_lists)}")
    return rucksacks_lists

def return_rucksacks_compartments(fname=RUCKSACKS_FNAME) -> list:
    rucksacks_lists = return_rucksacks(fname=fname)
    rucksacks_compartments=[]
    for rucksack in rucksacks_lists:
        len_half = len(rucksack)//2
        left = list(rucksack[:len_half])
        right = list(rucksack[len_half:])
        rucksacks_compartments.append([left,right])
    return rucksacks_compartments

def return_rucksacks_triples(fname=RUCKSACKS_FNAME) -> list:
    rucksacks_lists = return_rucksacks(fname=fname)
    rucksacks_triples=[]
    current_group=[]
    for rucksack in rucksacks_lists:
        current_group.append(list(rucksack))
        if len(current_group) == 3:
            rucksacks_triples.append(current_group)
            current_group = []
    assert not current_group, "Leftover elves in the current group!"
    return rucksacks_triples
    
def get_value_from_all_groups_of_three(fname=RUCKSACKS_FNAME) -> int:
    rucksacks_triples = return_rucksacks_triples(fname=fname)
    running_total=0
    counter = defaultdict(int)
    for group in rucksacks_triples:
        common_items_set = get_common_item_type(*group)
        counter[len(common_items_set)] += 1
        for item in common_items_set:
            running_total += get_priority(item)
    print(f"Histogram of repeat items: {counter}")
    return running_total

def get_common_item_type(*groups) -> set:
    common_set = set(groups[0])
    for each in groups[1:]:
        common_set = common_set & set(each)
    return common_set

def get_value_of_all_intersecting_items(fname=RUCKSACKS_FNAME) -> int:
    rucksacks_compartments = return_rucksacks_compartments(fname=fname)
    running_total=0
    counter = defaultdict(int)
    for left,right in rucksacks_compartments:
        common_items_set = get_common_item_type(left,right)
        counter[len(common_items_set)] += 1
        for item in common_items_set:
            running_total += get_priority(item)
    print(f"Histogram of repeat items: {counter}")
    return running_total


if __name__ == "__main__":
    total_compartments = get_value_of_all_intersecting_items()
    total_groups = get_value_from_all_groups_of_three()
    print(f"Total priority compartments: {total_compartments}")
    print(f"Total priority groups: {total_groups}")