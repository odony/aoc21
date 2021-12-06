use counter::Counter;

fn simulate_fish(input: &str, days: u32) -> u64 {
    let mut fish = input
    				.trim()
    				.split(",")
    				.map(|f| f.parse::<i32>().unwrap())
    				.collect::<Counter<_, u64>>();
    for _ in 0..days {
    	// didn't succeed building a new pre-initialized counter
    	// so working in-place instead
    	for age in 0..9 {
    		fish[&(age-1)] = fish[&age];
    	}
		fish[&8] = fish[&-1];
	    fish[&6] += fish[&-1];
		fish[&-1] = 0;
    }
    fish.values().copied().sum()
}

#[aoc(day6, part1)]
pub fn part1(input: &str) -> u64 {
	simulate_fish(&input, 80)
}

#[aoc(day6, part2)]
pub fn part2(input: &str) -> u64 {
	simulate_fish(&input, 256)
}
