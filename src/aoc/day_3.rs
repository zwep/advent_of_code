use std::path::{Path};
use crate::utils::file;
use std::env;
use crate::aoc::day_3;
use crate::utils::file::argsort;

fn form_stuff(data: &Vec<u32>, n_digit: usize, total: u32) -> u32 {
    // So it is more normal to pass a slice than a vec here...
    // But what -is- a &Vec? Isnt that 'just' a slice?
    // So what we gonna do...
    // Get the max of the first len(data) - N entries
    // Then recall this function for the remaining entries
    println!("Incomming data {:?}", data);
    println!("Number of digits {:?}", n_digit);
    println!("Current total {:?}", total);
    if n_digit == 0 {
        return total;
    }
    let n = data.len() as usize;
    let data_subet = &data[0..n - n_digit];
    println!("data subset: {:?}", data_subet);
    let max_value = data_subet.iter().max().unwrap();
    let max_index = data_subet
        .iter()
        .position(|x| x == max_value)
        .unwrap();
    println!("index {:?}", max_index);
    let new_data = &data[max_index+1 .. n].to_vec();
    let delta = (max_value) * 10_u32.pow((n_digit - 1) as u32);
    form_stuff(new_data, n_digit-1, total + delta)
}

#[allow(dead_code)]
fn form_another_large_number(data: &Vec<u32>) -> i64 {
    let mut result: i64 = 0;
    for i in 0..data.len(){
        for j in i+1..data.len(){
            let temp = format!("{}{}", data[i], data[j]).parse::<i64>().unwrap();
            if temp > result {
                result = temp;
            }
        }
    }
    result
}

#[allow(dead_code)]
pub fn part_1(){
    println!("Starting with part 1");
    let path = env::current_dir().unwrap().display().to_string();
    println!("The current directory is {}", path);
    let datapath = Path::new("data/day_3.txt");
    let file_seperator: &str = "\n";
    let loaded_data: _ = file::load_data(datapath, file_seperator);
    println!("{:?}", loaded_data);
    let data: _ = file::vec_string_to_int(loaded_data);
    println!("----------------");
    let mut total = 0;
    // Now do everything
    for data in data{
        let temp = form_another_large_number(&data);
        println!("{:?}", temp);
        total += temp;
    }
    println!("{:?}", total);
}

pub fn part_2(){
    println!("Starting with part 2");
    let path = env::current_dir().unwrap().display().to_string();
    println!("The current directory is {}", path);
    let datapath = Path::new("data/day_3.txt");
    let file_seperator: &str = "\n";
    let loaded_data: _ = file::load_data(datapath, file_seperator);
    println!("{:?}", loaded_data);
    let data: _ = file::vec_string_to_int::<u64>(loaded_data);
    println!("----------------");
    form_stuff(&data[0], 12, 0);
}