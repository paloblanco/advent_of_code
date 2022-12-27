TEST_NAME = r"day25input_test.txt"
INPUT_NAME = r"day25input.txt"

def get_snafu_from_file(fname=TEST_NAME):
    with open(fname) as f:
        return [e.strip() for e in f.readlines()]

S2D = {
    "=":-2,
    "-":-1,
    "0":0,
    "1":1,
    "2":2
}

D2S = {value:key for key,value in S2D.items()}

def snafu_to_digit(snafu: str) -> int:
    digit=1
    snafu_stack = list(snafu)
    number_return = 0
    while snafu_stack:
        s = snafu_stack.pop()
        number_return += S2D[s]*digit
        digit*=5
    return number_return

def get_base_list_from_number(number,base=5):
    num_list = []
    digit=1
    newnum=0
    while newnum != number:
        new_digit = (((number//digit)*digit) % (digit*base))//digit
        num_list.append(new_digit)
        newnum=0
        for i,d in enumerate(num_list):
            newnum += d * base**i
        digit *= base
    return num_list[::-1]

def int_to_snafu(number: int) -> str:
    number_list = get_base_list_from_number(number,base=5)[::-1]
    snafu_list = []
    next_add=0
    for i,n in enumerate(number_list):
        n += next_add
        next_add = 0
        if n > 2:
            n = n-5
            next_add = 1
        snafu_list.append(n)
    if next_add:
        snafu_list.append(1)
    snafu_list = [D2S[d] for d in snafu_list]
    return ''.join(snafu_list[::-1])
    

def part1(fname=TEST_NAME):
    snafus = get_snafu_from_file(fname)
    sum_int = sum([snafu_to_digit(s) for s in snafus])
    return int_to_snafu(sum_int)

if __name__ == "__main__":
    test1 = part1()
    print(f"{test1=}")

    p1 = part1(INPUT_NAME)
    print(f"{p1=}")
