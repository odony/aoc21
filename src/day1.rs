

#[aoc(day1, part1, loop)]
pub fn part1_chars(input: &str) -> u32 {
    let mut prev = u32::MAX;
    let mut c = 0;

    for l in input.lines() {
        let n: u32 = l.trim().parse().unwrap();
        if n > prev {
            c += 1;
        }
        prev = n;
    }

    c
}


// Alternative to the `for` loop version above
#[aoc(day1, part1, iter)]
pub fn part1_iter(input: &str) -> u32 {
    let mut prev = u32::MAX;
    input
        .lines()
        .map(|l| {
            let n: u32 = l.trim().parse().unwrap();
            if n > prev {
                prev = n;
                return 1;
            } else {
                prev = n;
                return 0;
            }
        })
        .sum()
}