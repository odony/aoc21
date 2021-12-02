// use std::env;
// use std::fs;

extern crate aoc21;
extern crate aoc_runner_derive;
extern crate aoc_runner;

use aoc_runner_derive::aoc_main;

aoc_main! { lib = aoc21 }





// fn day1a(input: Vec<u32>) -> u32 {
//     let mut prev: u32 = u32::MAX;
//     let mut count: u32 = 0;
//     for n in input {
//         if n > prev {
//            count += 1;
//         }
//         prev = n;
//     }
//     count
// }



// const INPUTS_DIR: &str = "inputs";

// fn main() {

//     let args: Vec<String> = env::args().collect();
//     if args.len() < 2 {
//         panic!("Synopsis: {} <dayXX>", args[0]);
//     }

//     let filename = &args[1];
//     println!("AoC 2021 -- {}", filename);

//     // load the file
//     let contents = fs::read_to_string(format!("{}/{}", INPUTS_DIR, filename))
//         .expect("Can't read file");
//     let mut inputs: Vec<&u32> = contents
//         .lines()
//         .map(|s| s.trim().parse::<u32>());

//     println!("File length: {:?}", inputs.len());

//     day1a(input);

// }