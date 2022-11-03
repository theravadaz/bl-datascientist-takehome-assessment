from itertools import groupby

# GLOBAL VARIABLES
MIN = 7
MAX = 25


def main():
    print("The number of steps to make the password valid is: ", steps("z"))
    print("The number of steps to make the password valid is: ", steps("aA1"))
    print("The number of steps to make the password valid is: ", steps("1377C0d3"))
    print("The number of steps to make the password valid is: ", steps("aaaaaa"))
    print("The number of steps to make the password valid is: ", steps("g_czechout"))
    print("The number of steps to make the password valid is: ", steps("Aa123456."))
    print("The number of steps to make the password valid is: ", steps("valid_passwordAB123"))
    print("The number of steps to make the password valid is: ", steps("hello123456lll"))


def steps(password: str) -> int:
    # Deal with edge case where password fulfils conditions 1-3, but is in common passwords list
    if conditionOne(password) == 0 and conditionTwo(password) == 0 and conditionThree(password) == 0:
        if not conditionFour(password):
            return 1
        else:
            return 0

    step_count = 0
    free_steps = 0

    condition_one_steps = conditionOne(password)
    condition_two_steps = conditionTwo(password)
    condition_three_steps = conditionThree(password)

    # Note that in this case, we don't need to worry about condition 3, as it can always be satisfied by satisfying
    # condition 1 and 2
    if validLength(password) == "TOO_SHORT":
        step_count += condition_one_steps
        free_steps += condition_one_steps
        while condition_two_steps != 0 and free_steps != 0:
            condition_two_steps -= 1
            free_steps -= 1
        step_count += condition_two_steps
        return step_count

    # Pretty sure this one is wrong: unsure how to optimally remove characters while fulfilling condition 1 in order to
    # minimise number of chars needing to be changed to fulfil condition 3
    if validLength(password) == "TOO_LONG":
        step_count += condition_one_steps
        step_count += condition_two_steps
        step_count += condition_three_steps - step_count
        return step_count

    if validLength(password) == "VALID_LENGTH":
        step_count += condition_two_steps
        free_steps += condition_two_steps
        while condition_three_steps != 0 and free_steps != 0:
            condition_three_steps -= 1
            free_steps -= 1
        step_count += condition_three_steps
        return step_count


def validLength(password: str) -> str:
    if len(password) < MIN:
        return "TOO_SHORT"
    if len(password) > MAX:
        return "TOO_LONG"
    else:
        return "VALID_LENGTH"


# Function that returns the minimum number of steps needed to make sure condition (1) of password security is satisfied
# (password must contain between 7 and 25 characters)
# ASSUMPTION: password must contain between 7 and 25 characters INCLUSIVE
def conditionOne(password: str) -> int:
    if len(password) < MIN:
        return MIN - len(password)
    if len(password) > MAX:
        return len(password) - MAX
    else:
        return 0


# Function that returns the minimum number of steps required to ensure that condition (2) of password secuirity is
# satisfied (password must contain one lowercase character, one uppercase character, and one digit)
def conditionTwo(password: str) -> int:
    required_characters = 0
    if not any(char.islower() for char in password):
        required_characters += 1
    if not any(char.isupper() for char in password):
        required_characters += 1
    if not any(char.isdigit() for char in password):
        required_characters += 1

    return required_characters


# Function that returns the minimum number of steps required to ensure that condition (3) of password security (password
# cannot contain any individual character more than three times in succession) is satisfied
# ASSUMPTION: Condition is case-sensitive (i.e. ...aAA... does not violate condition)
def conditionThree(password: str) -> int:
    groups = groupby(password)
    consecutive_counts = [sum(1 for _ in group) for char, group in groups]
    steps = sum([x // 3 for x in consecutive_counts if x >= 3])
    return steps


# Function that returns False if password is in common passwords list, True otherwise
# ASSUMPTION: The phrase "It must not INCLUDE any of the common passwords" means that the password cannot be identical
# to any passwords in 'common_passwords.txt', NOT that password cannot be a substring of any passwords in
# common_passwords.txt
def conditionFour(password: str) -> bool:
    with open('data/common-passwords.txt', 'r') as f:
        common_passwords_list = f.read().splitlines()
    if password in common_passwords_list:
        return False
    else:
        return True


main()
