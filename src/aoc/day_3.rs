use std::path::{Path};
use crate::utils::file;
use std::env;
use crate::aoc::day_3;
use crate::utils::file::argsort;
use std::cmp::Ord;
use std::fmt::{Debug, Display};
use num_traits::One;

pub fn form_stuff<T>(data: &[T], n_digit: usize, total: T) -> T
where
    T: Copy + One + Display  + Debug + Ord + std::ops::Add<Output = T> + std::ops::Mul<Output = T> + From<u32>,
{
    println!("Incoming data {:?}", data);
    println!("Total {:?}", total);
    println!("N digit {:?}", n_digit);
    // Get the max of the first len(data) - N entries
    // Then recall this function for the remaining entries
    if n_digit == 0 {
        println!("Finished");
        return total;
    }
    let n = data.len();
    let data_subet = &data[0..n - (n_digit - 1)];
    println!("Data subet {:?}", data_subet);
    let max_value = data_subet.iter().max().unwrap().to_owned();
    println!("Max value {:?}", max_value);
    let max_index = data_subet
        .iter()
        .position(|x| x == &max_value)
        .unwrap();
    println!("Max index {:?}", max_index);
    // Now, we slice the data vector to the remaining digits
    // And then we are going to call this function again
    let new_data = &data[max_index+1 .. ].to_vec();
    let pow10 = (0..(n_digit - 1))
        .fold(T::one(), |acc, _| acc * T::from(10u32));
    let new_total = total + max_value * pow10;
    println!("New total {:?}", new_total);
    println!("New data {:?}", new_data);

    form_stuff(new_data, n_digit-1, new_total)
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
    let mut total = 0;
    for line in data {
        println!("----------------------");
        let result = form_stuff::<u64>(&line, 12, 0);
        total += result;
    }
    println!("{:?}", total);

}