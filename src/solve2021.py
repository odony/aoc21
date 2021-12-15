#!/usr/bin/python3
import os
import sys

from pprint import pprint

"""
My reference implementations of the AoC 2021 challenges.
Used to compare my solutions and runtimes with the rust version.

Run the solver for e.g. day1 like this::

  ./src/solve2021.py day1 input/2021/day1.txt

"""


# ---- Day 1 -----

def day1_1(data):
    p, c = 99999, 0
    nums = (int(s) for s in data)
    for n in nums:
        if n > p:
            c += 1
        p = n
    return c

def day1_2(data):
    nums = list(int(s) for s in data)
    sums = (sum(nums[i-1:i+2]) for i in range(1, len(nums)))
    return day1_1(sums)


# ---- Day 2 -----

def day2_1(data):
    d, x = 0, 0
    for l in data:
        action, qty = l.split(' ')
        qty = int(qty)
        if action == 'down':
            d += qty
        if action == 'up':
            d -= qty
        if action == 'forward':
            x += qty
    return d * x

def day2_2(data):
    d, x, a = 0, 0, 0
    for l in data:
        action, qty = l.split(' ')
        qty = int(qty)
        if action == 'down':
            a += qty
        if action == 'up':
            a -= qty
        if action == 'forward':
            x += qty
            d += a * qty
    return d * x


# ---- Day 3 -----

def bit_freqs(data):
    b_freqs = [[0,0] for b in range(len(data[0]))]
    for l in data:
        for i, b in enumerate(l):
            b_freqs[i][int(b)] += 1
    return b_freqs

def day3_1(data):
    b_freqs = bit_freqs(data)
    gamma_bin = ''.join('1' if b[1] > b[0] else '0' for b in b_freqs)
    epsilon_bin = ''.join('1' if b[1] < b[0] else '0' for b in b_freqs)
    gamma = int(gamma_bin, 2)
    epsilon = int(epsilon_bin, 2)
    print('gamma', gamma, 'epsilon', epsilon)
    return gamma * epsilon

# ~~

def filter_data(data, bit_pos, bit_val):
    bit_val = str(int(bit_val))
    res = [l for l in data if l[bit_pos] == bit_val]
    return res

def reduce_freq(data, high):
    remaining = data.copy()
    bit_pos = 0
    while len(remaining) > 1:
        b_freqs = bit_freqs(remaining)
        b0_freq, b1_freq = b_freqs[bit_pos]
        remaining = filter_data(
            remaining,
            bit_pos,
            b1_freq >= b0_freq if high else b0_freq > b1_freq)
        bit_pos += 1
    return int(remaining[0], 2)

def day3_2(data):
    o2_rate = reduce_freq(data, 1)
    co2_rate = reduce_freq(data, 0)
    return o2_rate * co2_rate


# ---- Day 4 -----

def generator_d4(data):
    draw = (int(n) for n in data.pop(0).split(','))
    data.pop(0)
    boards = []
    board = []
    num_map = {} # { 12: [(board1, x, y), ...]'}
    y = 0
    for line in data:
        if not line:
            boards.append(board)
            board = []
            y = 0
        else:
            board.append([])
            x = 0
            for n in line.split(' '):
                if not n.strip():
                    continue
                n = int(n)
                board[y].append([n, 0])
                num_map.setdefault(n, []).append((board, x, y))
                x += 1
            y += 1
    boards.append(board)
    return draw, boards, num_map

def is_winner_board_d4(board, x, y):
    # winner col/row has a sum of 5
    hsum = sum(board[y][i][1] for i in range(5))
    vsum = sum(board[i][x][1] for i in range(5))
    return 5 in (vsum, hsum)

def score_winner_board_d4(board, number):
    return number * sum(
            board[y][x][0]
            for y in range(5)
            for x in range(5)
            if not board[y][x][1]
        )

def day4_1(data):
    draw, boards, num_map = generator_d4(data.copy())
    for number in draw:
        for (board, x, y) in num_map.get(number, []):
            board[y][x][1] = 1
            if is_winner_board_d4(board, x, y):
                return score_winner_board_d4(board, number)

def day4_2(data):
    draw, boards, num_map = generator_d4(data.copy())
    for number in draw:
        for (board, x, y) in num_map.get(number, []):
            if not board in boards:
                continue
            board[y][x][1] = 1
            if is_winner_board_d4(board, x, y):
                boards.remove(board)
                if not boards:
                    return score_winner_board_d4(board, number)


# ---- Day 5 -----
import re
from collections import defaultdict

def day5_1(data, exclude_diag=True):
    floor = defaultdict(int)
    for l in data:
        x1, y1, x2, y2 = map(int, re.findall("\d+", l))
        if exclude_diag and x1 != x2 and y1 != y2:
            continue

        x, y = x1, y1
        floor[x, y] += 1
        while x != x2 or y != y2:
            x += ((x2 - x) / abs(x2 - x)) if (x2 - x) else 0
            y += ((y2 - y) / abs(y2 - y)) if (y2 - y) else 0
            floor[x, y] += 1

    return sum(1 for n in floor.values() if n > 1)

def day5_2(data):
    return day5_1(data, exclude_diag=False)


# ---- Day 6 -----
from collections import Counter

def day6_1(data, days=80):
    fish = Counter(map(int, data[0].split(',')))
    for d in range(days):
        fish = Counter({age - 1: num_fish
                        for age, num_fish in fish.items()})
        fish[8] += fish[-1]
        fish[6] += fish[-1]
        fish[-1] = 0
    return sum(fish.values())

def day6_2(data):
    return day6_1(data, 256)
    

# ---- Day 7 -----
from collections import Counter

def day7_1(data):
    crabs = Counter(map(int, data[0].split(',')))
    sums = [
        sum((abs(c - align_pos) * n) for c, n in crabs.items())
        for align_pos in range(max(crabs.elements()))
    ]
    return sorted(sums)[0]

def day7_2(data):
    crabs = Counter(map(int, data[0].split(',')))
    sums = [
        sum((abs(c - align_pos) * ((abs(c - align_pos) + 1) / 2) * n)
            for c, n in crabs.items())
        for align_pos in range(max(crabs.elements()))
    ]
    return int(sorted(sums)[0])

# ---- Day 8 -----
import itertools
import time

def day8_1(data):
    return sum(
        1 # let's not abuse bool shall we
        for line in data
        for digit in line.split()[-4:]
        if len(digit) in {2, 3, 4, 7})

def day8_2(data):
    DISPLAY = "abcdefg"
    NUMBERS = ("abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg")
    RAINBOW = defaultdict(dict)
    # 7! permutations (5040)
    for perm in itertools.permutations(DISPLAY):
        translator = {segment: DISPLAY[i] for i, segment in enumerate(perm)}
        digits = [frozenset(translator[seg] for seg in n) for n in NUMBERS]
        one = digits[1] # our index key
        mapping = {digit: i for i, digit in enumerate(digits)}
        RAINBOW[one][frozenset(digits)] = mapping
    result = 0
    for l in data:
        left, right = [p.split() for p in l.split(' | ')]
        [one] = [w for w in left if len(w) == 2]
        # n * log(n) because of the index on one
        key = frozenset(one)
        for words, mapping in RAINBOW[key].items():
            if frozenset(frozenset(w) for w in left) == words:
                result += sum(mapping[frozenset(w)] * 10**i for i, w in enumerate(right[::-1]))
                break
    return result


# ---- Day 9 -----

from math import prod

def d9_adj(i, j):
    return (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)

def day9_1(data):
    floor = {(i, j): int(x) for i, line in enumerate(data) for j, x in enumerate(line.strip())}
    return sum(cell + 1
               for p, cell in floor.items()
               if all(cell < floor.get(a, 9)
                      for a in d9_adj(*p)))

def day9_2(data):
    floor = {(i, j): int(x) for i, line in enumerate(data) for j, x in enumerate(line.strip())}
    basins = {}

    def explore_dfs(p, idx):
        if p in basins or floor.get(p, 9) == 9:
            return
        basins[p] = idx
        for a in d9_adj(*p):
            explore_dfs(a, idx)

    for i, p in enumerate(floor.keys()):
        explore_dfs(p, i)

    return prod(c for _, c in Counter(basins.values()).most_common(3))

# ---- Day 10 -----

def day10_1(data):
    ops = {'(': ')', '{': '}', '[': ']', '<': '>'}
    score_map = {')': 3, ']': 57, '}': 1197, '>': 25137}
    score = 0
    for l in data:
        state = []
        for c in l:
            if c in ops:
                state.append(c)
            elif state and c == ops[state[-1]]:
                state.pop()
            else:
                print(f"illegal {c} in: {l}")
                score += score_map[c]
                break
    return score


def day10_2(data):
    ops = {'(': ')', '{': '}', '[': ']', '<': '>'}
    score_map = {')': 1, ']': 2, '}': 3, '>': 4}
    scores = []
    for l in data:
        state = []
        for c in l:
            if c in ops:
                state.append(c)
            elif state and c == ops[state[-1]]:
                state.pop()
            else:
                # corrupted line: discarded
                state = []
                break
        if state:
            # repair the line
            score = 0
            for c in state[::-1]:
                score = score * 5 + score_map[ops[c]]
            print(f"score: {score} for incomplete line: {l}")
            scores.append(score)
    return sorted(scores)[len(scores)//2]


# ---- Day 11 -----

# So, day 9 all over again? ;-)
def octopus_adj(i, j):
    return ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1),
            (i - 1, j - 1), (i + 1, j - 1), (i + 1, j + 1), (i - 1, j + 1))

def day11_1(data, steps=100, stop_sync=False):
    energy = {(i, j): int(x) for i, line in enumerate(data) for j, x in enumerate(line.strip())}
    flashes = 0
    for s in range(steps):
        flashed = set()
        def flash_or_not(octopus):
            if octopus not in energy:
                return
            energy[octopus] += 1
            if energy[octopus] > 9 and octopus not in flashed:
                flashed.add(octopus)
                for neighbour in octopus_adj(*octopus):
                    flash_or_not(neighbour)
        for o in energy.keys():
            flash_or_not(o)
        for o in flashed:
            energy[o] = 0
        flashes += len(flashed)
        if stop_sync and len(flashed) == len(energy):
            return s+1
    return flashes

def day11_2(data):
    return day11_1(data, steps=1000, stop_sync=1)


# ---- Day 12 -----

def day12_1(data, allowed_dupes=0):
    is_small = lambda cave: cave.lower() == cave
    all_paths = set()
    paths  = defaultdict(list)
    for l in data:
        p_in, p_out = l.split("-")
        paths[p_in].append(p_out)
        paths[p_out].append(p_in)
    def visit(p, path, visited, allow_dupes):
        if p in visited:
            if not allow_dupes or p in {"start", "end"}:
                return
            allow_dupes -= 1
        path = path + (p,)
        if is_small(p):
            visited[p] += 1
        if p == 'end':
            all_paths.add(path)
            return
        for dest in paths[p]:
            visit(dest, path, visited.copy(), allow_dupes)
    visit("start", tuple(), defaultdict(int), allowed_dupes)
    return len(all_paths)

def day12_2(data):
    return day12_1(data, allowed_dupes=1)


# ---- Day 13 -----

def day13_1(data):
    dots  = {}
    axes = "xy"

    while(True):
        l = data.pop(0)
        if not l.strip():
            break
        x, y = map(int, l.strip().split(","))
        dots[(x,y)] = 1

    for i, l in enumerate(data):
        axis, fold = re.search("along ([xy])=(\d+)", l).groups()
        fold = int(fold)
        ax_idx = axes.index(axis)
        for p in list(dots):
            if p[ax_idx] > fold:
                new_pos = p[ax_idx] - 2 * (p[ax_idx] - fold)
                new_p = list(p)
                new_p[ax_idx] = new_pos
                del dots[p]
                dots[tuple(new_p)] = 1
        print(sum(1 for _, num in dots.items() if num))

    for j in range(0, 6):
        for i in range(0, 100):
            if (i,j) in dots:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    return


# ---- Day 14 -----

def day14_1(data, rounds=10):
    polymer = data[0]
    subst = dict([l.split(" -> ") for l in data[2:]])

    # Each polymer is made of overlapping pairs:
    # NNCB          =  NN NC CB
    # NCNBCHB       =  NC CN NB BC CH HB
    # NBCCNBBBCBHCB =  NB BC CC CN NB BB BB BC CB BH HC CB

    # For each pair, we'll get 2 resulting pairs after inserting
    # the new element, right and left. E.g. HN + C => HC + CN
    # So we can simulate the insertions by incrementing the
    # number of each new pair, instead of actually walking the
    # exponentially long polymer string.
    pairs = Counter(f"{p}{q}" for (p, q) in zip(polymer, polymer[1:]))
    for _ in range(rounds):
        new_pairs = Counter()
        for pair, count in pairs.items():
            p, q = pair
            # Count only the new pairs created by the insertion,
            # the old pair is consumed by the operation
            new_pairs[f"{p}{subst[pair]}"] += count
            new_pairs[f"{subst[pair]}{q}"] += count
        pairs = new_pairs

    # To count individual elements, we can count the leftmost element of
    # each pair + the final element of the polymer, which never changes.
    counter = Counter()
    counter[polymer[-1]] = 1 # last element
    for pair, count in pairs.items():
        counter[pair[0]] += count

    freqs = counter.most_common()
    return freqs[0][1] - freqs[-1][1]

def day14_2(data):
    return day14_1(data, rounds=40)




# ---- Runner -----

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Synopsis: {sys.argv[0]} <day> <input_file>")
        sys.exit()
    _, func, infile = sys.argv
    if func not in globals() and (func + "_1") not in globals():
        print(f"Not a valid day: {func}")
        sys.exit()
    if not os.path.isfile(infile):
        print(f"Not a valid file: {infile}")
        sys.exit()

    with open(infile, 'r') as fd:
        data_in = fd.readlines()
        data_in = [x.strip() for x in data_in]
        for fn in (func, func + "_1", func + "_2"):
            if fn in globals():
                result = globals()[fn](data_in)
                print(f"{fn} -> {result}")

