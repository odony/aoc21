
// PART 1

fn bit_freqs(data: &str, width: usize) -> Vec<[u32; 2]> {
    let mut b_freq = vec![[0,0]; width];
    for l in data.lines() {
        for (i, b) in l.chars().enumerate() {
            b_freq[i][b.to_digit(2).unwrap() as usize] += 1;
        }
    }
    b_freq
}

#[aoc(day3, part1)]
pub fn part1(input: &str) -> isize {
    let w: usize = input.lines().next().unwrap().len();
    let b_freqs: Vec<[u32; 2]> = bit_freqs(input, w);
    let gamma_bin = b_freqs
                        .iter()
                        .map(|&[a,b]| {
                            if a > b { return "0"; }
                            else { return "1"; }
                        })
                        .collect::<String>();
    let epsilon_bin = b_freqs
                        .iter()
                        .map(|&[a,b]| {
                            if a > b { return "1"; }
                            else { return "0"; }
                        })
                        .collect::<String>();
    let gamma = isize::from_str_radix(&gamma_bin, 2).unwrap();
    let epsilon = isize::from_str_radix(&epsilon_bin, 2).unwrap();

    gamma * epsilon
}


// PART 2

// What happened with part 2, it's not obvious that you
// can build much on part 1...?!
// I do have a variant of bit_freqs(), but not on the same data types, so 🤷‍♂️


fn bit_freqs_vec(data: &Vec<&str>, width: usize) -> Vec<[u32; 2]> {
    let mut b_freq = vec![[0,0]; width];
    for l in data.iter() {
        for (i, b) in l.chars().enumerate() {
            b_freq[i][b.to_digit(2).unwrap() as usize] += 1;
        }
    }
    b_freq
}

fn filter_lines(input: &str, width: usize, high: bool) -> &str {
    let mut input: Vec<&str> = input.lines().collect();
    for bit_pos in 0..width {
        let b_freqs: Vec<[u32; 2]> = bit_freqs_vec(&input, width);
        if (high && b_freqs[bit_pos][1] >= b_freqs[bit_pos][0]) ||
            (!high && b_freqs[bit_pos][1] < b_freqs[bit_pos][0])
        {
            input.retain(|line| line.chars().nth(bit_pos) == Some('1'));
        } else {
            input.retain(|line| line.chars().nth(bit_pos) == Some('0'));
        }
        if input.len() == 1 { break; }
    }
    input[0]
}

#[aoc(day3, part2)]
pub fn part2(input: &str) -> isize {
    let w: usize = input.lines().next().unwrap().len();
    let o2_rate = filter_lines(input, w, true);
    let co2_rate = filter_lines(input, w, false);
    
    isize::from_str_radix(&o2_rate, 2).unwrap() *
    isize::from_str_radix(&co2_rate, 2).unwrap()
}



