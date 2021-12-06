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

