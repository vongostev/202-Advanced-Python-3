cube = lambda x: x * x * x

def fibonacci(n):
    lst_f = [0, 1]
    for i in range(n - 1):
        lst_f.append(lst_f[-1] + lst_f[-2])

    return lst_f[:n]