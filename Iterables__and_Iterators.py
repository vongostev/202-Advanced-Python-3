from itertools import combinations

N = int(input())
letters = input().split()
K = int(input())

combinations_with_a = 0

all_combinations = list(combinations(letters, K))

for el in all_combinations:
    if 'a' in el:
        combinations_with_a += 1

print(round(combinations_with_a / len(all_combinations), 3))