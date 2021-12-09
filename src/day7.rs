use counter::Counter;

#[aoc(day7, part1)]
pub fn part1(input: &str) -> i32 {
    let crabs = input
                .trim()
                .split(",")
                .map(|f| f.parse::<i32>().unwrap())
                .collect::<Counter<_>>();
    let mut costs: Vec<i32> = vec![];
    let high_pos = crabs.keys().copied().max().unwrap();
    for align_pos in 0i32..high_pos {
        costs.push(
            crabs
            .iter()
            .map(|(&c, &n)| {
                 (c - align_pos).abs() * n as i32
            })
            .sum::<i32>())
        ;
    }
    costs.iter().copied().min().unwrap()
}

#[aoc(day7, part2)]
pub fn part2(input: &str) -> i32 {
    let crabs = input
                .trim()
                .split(",")
                .map(|f| f.parse::<i32>().unwrap())
                .collect::<Counter<_>>();
    let mut costs: Vec<i32> = vec![];
    let high_pos = crabs.keys().copied().max().unwrap();
    for align_pos in 0i32..high_pos {
        costs.push(
            crabs
            .iter()
            .map(|(&c, &n)| {
                let cost = (c - align_pos).abs();
                (cost * (cost + 1) / 2) * n as i32
            })
            .sum::<i32>())
        ;
    }
    costs.iter().copied().min().unwrap()
}