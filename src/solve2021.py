#!/usr/bin/python3
import os
import sys

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

