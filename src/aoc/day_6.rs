use std::env;
use std::path::Path;
use std::str::Chars;
use crate::utils::file;
use crate::utils::file::consolidate_range;

pub fn part_1(){
    println!("Starting part 1");
    let path = env::current_dir().unwrap().display().to_string();
    println!("The current directory is {}", path);
    let datapath = Path::new("data/day_6.txt");
    let file_seperator: &str = "\n";
    let loaded_data: _ = file::load_data(datapath, file_seperator);
    let processed: Vec<Vec<String>> = loaded_data
        .into_iter()
        .map(|line| {
            line.split_whitespace()
                .map(str::to_string)
                .collect::<Vec<_>>()
        })
        .collect();

    let processed_t = file::transpose_vec(processed);
    println!("{:?}", processed_t);
    let result = processed_t.iter().filter_map(|line| {
        let operator = line.last()?;
        let numbers = file::vec_string_to_int::<u64>(line[..line.len() - 1].to_vec());
        match operator.as_str() {
            "*" => Some(numbers.iter().product()),
            "+" => Some(numbers.iter().sum()),
            _ => None,
        }
    }
    ).collect::<Vec<u64>>();
    println!("{:?}", result);
    println!("{:?}", result.iter().sum::<u64>());
}

pub fn part_2() {
    // Read in the data
    println!("Starting part 2");
    let path = env::current_dir().unwrap().display().to_string();
    println!("The current directory is {}", path);
    let datapath = Path::new("data/day_6.txt");
    let file_seperator: &str = "\n";
    let loaded_data: _ = file::load_data(datapath, file_seperator);
    let loaded_data_char = loaded_data.iter().map(|x| file::string_to_char(x)).collect::<Vec<Vec<char>>>();
    let loaded_data_t = file::transpose_vec::<char>(loaded_data_char);
    println!("{:?}", loaded_data_t);
    let z = loaded_data_t.into_iter().map(|x| x.iter().collect::<String>()).collect::<Vec<String>>();
    println!("{:?}", z);
    let mut result: Vec<Vec<String>> = Vec::new();
    let mut temp = Vec::new();
    for line in z {
        if line.trim().is_empty() {
            temp.reverse();
            result.push(temp);
            temp = Vec::new();
            continue;
        } else {
            temp.push(line);
        }
    }
    temp.reverse();
    result.push(temp);
    println!("{:?}", result);
    let z = result.into_iter().map(|x| x.into_iter().collect::<String>()).collect::<Vec<String>>();
    println!("{:?}", z);
    let w: _ = z
        .into_iter()
        .map(|mut x| {
            let operator: char = x.pop().unwrap();
            (x, operator.to_string())
        }).collect::<Vec<(String, String)>>();
    println!("{:?}", w);
    let result = w.into_iter().filter_map(|(content, operator)| {
        let content_num = content.split(" ").map(|s| s.to_string()).collect::<Vec<String>>();
        let numbers = file::vec_string_to_int::<u64>(content_num);
        match operator.as_str() {
            "*" => Some(numbers.iter().product()),
            "+" => Some(numbers.iter().sum()),
            _ => None,
        }
    }
    ).collect::<Vec<u64>>();
    println!("{:?}", result);
    println!("{:?}", result.iter().sum::<u64>());
}