
#[aoc(day2, part1, Chars)]
pub fn part1_chars(input: &str) -> u32 {
    let mut x = 0;
    let mut d = 0;

    for l in input.lines() {
        let l: Vec<&str> = l.trim().split(' ').collect();
        let c = l[0];
        let q: u32 = l[1].trim().parse().expect("Should be int");
        match c {
            "down"    => d += q,
            "up"      => d -= q,
            "forward" => x += q,
            _ => unreachable!(),
        };
    }

    x * d
}


#[aoc(day2, part2, Chars)]
pub fn part2_chars(input: &str) -> u32 {
    let mut x = 0;
    let mut d = 0;
    let mut a = 0;

    for l in input.lines() {
        let l: Vec<&str> = l.trim().split(' ').collect();
        let c = l[0];
        let q: u32 = l[1].trim().parse().unwrap();
        match c {
            "down"    => a += q,
            "up"      => a -= q,
            "forward" => { x += q ; d += a * q },
            _ => unreachable!(),
        };
    }

    x * d
}

