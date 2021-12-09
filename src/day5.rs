use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;
use num::signum;

fn _part1(input: &str, exclude_diag: bool) -> usize {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"\d+").unwrap();
    }

    let mut floor = HashMap::new();
    for line in input.lines() {
        // idiomatic findall into a vector
        let v: Vec<i32> = RE.find_iter(line)
                            .filter_map(|n| n.as_str().parse().ok())
                            .collect();
        
        // idiomatic destructuring of vector
        if let [x1, y1, x2, y2] = v[..] {
            if exclude_diag && x1 != x2 && y1 != y2 {
                continue;
            }
            let (mut x, mut y) = (x1, y1);
            floor.entry((x, y)).and_modify(|e| *e += 1).or_insert(1);
            while x != x2 || y != y2 {
                x += signum(x2 - x);
                y += signum(y2 - y);
                floor.entry((x, y)).and_modify(|e| *e += 1).or_insert(1);
            }
        }
    }

    floor.values().filter(|&v| *v > 1).map(|_| 1).sum()
}

#[aoc(day5, part1)]
pub fn part1(input: &str) -> usize {
    _part1(&input, true)
}


#[aoc(day5, part2)]
pub fn part2(input: &str) -> usize {
    _part1(&input, false)
}

