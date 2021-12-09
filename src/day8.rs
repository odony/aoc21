use std::collections::{HashSet, HashMap};

#[aoc(day8, part1)]
pub fn part1(input: &str) -> usize {
    input.lines()
         .map(|l| l.split(" | ")
                   .last()
                   .unwrap()
                   .split(" "))
         .flatten()
         .filter(|w| [2, 3, 4, 7].contains(&w.len()))
         .count()
}

#[aoc(day8, part2)]
pub fn part2(input: &str) -> usize {
    //                              0       1*     2        3        4*      5         6       7*       8*         9
    //const NUMBERS: &[&str] = &["abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"];
    let fingerprints: HashMap<_,usize> = [
            (vec![2, 3, 3, 6], 0),
            (vec![1, 2, 2, 5], 2),
            (vec![2, 3, 3, 5], 3),
            (vec![1, 3, 2, 5], 5),
            (vec![1, 3, 2, 6], 6),
            (vec![2, 4, 3, 6], 9) 
    ].iter().cloned().collect();
    let mut result: usize = 0;
    for l in input.lines() {
        let parts: Vec<&str> = l.split(" | ").collect();
        let digits: Vec<&str> = parts[0].split(" ").collect();
        let display: Vec<&str> = parts[1].split(" ").collect();
        let mut map: HashMap<usize, &str> = HashMap::new();
        for digit in digits.iter() {
            match digit.len() {
                2 => {map.insert(1, &digit);},
                3 => {map.insert(7, &digit);},
                4 => {map.insert(4, &digit);},
                7 => {map.insert(8, &digit);},
                _ => {}
            }
        }
        for (i, digit) in display.into_iter().rev().enumerate() {
            let value: usize = match digit.len() {
                    2 => 1,
                    3 => 7,
                    4 => 4,
                    7 => 8,
                5 | 6 => {
                      let digit_chars: HashSet<char> = digit.chars().collect();
                      let fingerprint: Vec<usize> = [1,4,7,8].iter().map(|d| {
                        let candi_set: HashSet<char> = map.get(d).unwrap().chars().collect();
                        candi_set.intersection(&digit_chars).count()
                      }).collect();
                      *fingerprints.get(&fingerprint).unwrap()
                    },
                _ => panic!()
            };
            result += usize::pow(10usize, i as u32) * value; 
        }
    }
    result
}

