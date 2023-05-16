import string
def fun(s):
    letter_n = 0

    while letter_n < len(s) - 1 and s[letter_n] != '@':
        if s[letter_n] not in string.ascii_letters + string.digits + '-_':
            return False
        letter_n += 1

    if not letter_n:
        return False
    
    letter_n += 1
    letter_n_prev = letter_n

    while letter_n < len(s) - 1 and s[letter_n] != '.':
        if s[letter_n] not in string.ascii_letters + string.digits:
            return False
        letter_n += 1

    if letter_n == letter_n_prev:
        return False

    letter_n += 1
    letter_n_prev = letter_n

    while letter_n < len(s):
        if s[letter_n] not in string.ascii_letters:
            return False
        letter_n += 1
    
    return 1 <= letter_n - letter_n_prev <= 3