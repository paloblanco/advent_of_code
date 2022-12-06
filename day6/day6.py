INPUT_FNAME = r"day6_input.txt"

def return_buffer(fname=INPUT_FNAME):
    with open(fname,"r") as buffer_file:
        buffer_string = buffer_file.read().strip()
    return buffer_string

def return_characters_until_start(buffer:str, length=4) -> int:
    for ix in range(length,len(buffer)):
        start_string=buffer[ix-length:ix]
        start_set=set(start_string)
        if len(start_set)==length:
            return ix

if __name__ == "__main__":
    buffer = return_buffer()
    start = return_characters_until_start(buffer, length=4)
    print(f"Start character: {start}")
    start_message = return_characters_until_start(buffer, length=14)
    print(f"Start character character: {start_message}")

