from cs50 import get_int

h = get_int("Height: ")
while h < 1 or h > 8:
    h = get_int("Height: ")

for i in range(h):

    # print left spaces
    for j in range(h-i-1):
        print(" ", end="")

    # print left blocks
    for j in range(i+1):
        print("#", end="")

    print("  ", end="")

    # print right blocks
    for j in range(i+1):
        print("#", end="")

    print()
