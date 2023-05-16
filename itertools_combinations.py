from itertools import combinations

lst = input().split()

S = sorted(lst[0])
k = int(lst[1])

for i in range(1, k + 1):
    for comb in combinations(S, i):
        print(''.join(comb))