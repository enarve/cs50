def check_number(num):
    if num.isnumeric():
        if check_if_valid(num):
            first = int(num[0])
            sum_of_two = int(num[0] + num[1])
            if first == 4 and len(num) in [13, 16]:
                print("VISA\n")
                return
            elif sum_of_two in [34, 37] and len(num) == 15:
                print("AMEX\n")
                return
            elif len(num) == 16 and sum_of_two in [51, 52, 53, 54, 55]:
                print("MASTERCARD\n")
                return

    print("INVALID\n")
    return


def check_if_valid(num):
    sum = 0
    for i in range(len(num)-2, -1, -2):
        d = 2 * int(num[i])
        for c in str(d):
            sum += int(c)

    for i in range(len(num)-1, -1, -2):
        sum += int(num[i])

    z = int(str(sum)[-1])
    if z == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    num = input("Number: ")
    check_number(num)
