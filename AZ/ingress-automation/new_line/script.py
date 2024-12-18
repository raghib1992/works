filename = "read.txt"

with open(filename, 'rb+') as f:  # Open file in binary mode
    f.seek(-1, 2)  # Move to the last byte of the file
    last_byte = f.read(1)
    print(f"Last line is {last_byte}")
    if last_byte == b'-':
        print("Adding new line")
        f.write(b'\n')
        print(f"Added new line to file '{filename}'.")
    elif last_byte == b'\n':
        print(f"Last line is empty line")
        print("Check second last line")
        f.seek(-2,2)
        second_line=f.read(1)
        print(f"second last line is {second_line}")
        if second_line == b'-':
            print("File is Okay to procees")
        else:
            f.write(b'\n---\n')
    else:
        print("Addind --- and new line")
        f.write(b'\n---\n')
        
