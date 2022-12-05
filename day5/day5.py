STACKS_FILENAME = r"day5input.txt"

def get_data_from_file(fname=STACKS_FILENAME):
    with open(fname,"r") as stacks_file:
        stacks_lines = stacks_file.readlines()
    stacks_lines = [each.strip() for each in stacks_lines]
    stacks_start_lines = stacks_lines[:8]
    stacks_moves_lines = stacks_lines[10:]
    return stacks_start_lines, stacks_moves_lines

def return_stacks_from_lines(lines:list):
    stacks = [[] for i in range(9)]
    offset_ix = 1
    steps_to_next_id = 4
    max_id = 8
    for line in lines:
        for ix in range(9):
            position = offset_ix + steps_to_next_id*ix
            try:
                crate_id = line[position]
                if crate_id != " ":
                    stacks[ix].append(crate_id)
            except:
                pass
    for stack in stacks:
        stack.reverse()
    return stacks

def return_moves_from_lines(lines):
    moves_triples=[]
    for line in lines:
        triple = line.split(" ")[1::2]
        moves_triples.append([int(each) for each in triple])
    return moves_triples

def execute_moves(stacks,moves):
    for move_count, stack_from, stack_to in moves:
        for i in range(move_count):
            crate_id = stacks[stack_from-1].pop()
            stacks[stack_to-1].append(crate_id)
    return stacks

def execute_moves_new_crane(stacks,moves):
    for move_count, stack_from, stack_to in moves:
        stacks[stack_to-1] = stacks[stack_to-1] + stacks[stack_from-1][-move_count:]
        stacks[stack_from-1] = stacks[stack_from-1][:-move_count]
    return stacks

def return_top_of_each_stack(fname=STACKS_FILENAME, moving_algo = execute_moves):
    start, moves = get_data_from_file(fname=fname)
    stacks = return_stacks_from_lines(start)
    moves = return_moves_from_lines(moves)
    stacks_new = moving_algo(stacks,moves)
    top_string=""
    for stack in stacks_new:
        top_string = top_string + stack[-1]
    return top_string


if __name__ == "__main__":
    tops = return_top_of_each_stack()
    print(f"stack tops: {tops}")
    tops_new = return_top_of_each_stack(moving_algo=execute_moves_new_crane)
    print(f"stack tops new: {tops_new}")