use std::fs;
use std::ops::Range;
use std::path::Path;
use std::str::FromStr;
use num_traits::{One, Zero};

pub fn load_data(path: &Path, sep: &str) -> Vec<String> {
    let contents = fs::read_to_string(path).expect("Could not read file");
    contents.split(sep).map(|s|s.to_string()).collect()
}

pub fn string_to_char(line: String) -> Vec<char> {
    // Here we convert a single line of strings to a vec of characters
    line.chars().collect::<Vec<char>>()
}

pub fn vec_char_to_int<T>(data: Vec<char>) -> Vec<T>
where
    T: FromStr,
    T::Err: std::fmt::Debug,
{
    data.iter().map(|x| x.to_string().parse::<T>().expect("Oepsie")).collect()
}

pub fn vec_string_to_vec_int<T>(line: Vec<String>) -> Vec<Vec<T>>
where
    T: FromStr,
    T::Err: std::fmt::Debug,
{
    let mut data_content = Vec::new();

    for element in line {
        let temp = string_to_char(element);
        data_content.push(vec_char_to_int::<T>(temp));
    }

    return data_content;
}

pub fn vec_string_to_int<T>(line: Vec<String>) -> Vec<T>
where
    T: FromStr,
    T::Err: std::fmt::Debug,
{
    let data_content: Vec<T> = line
        .iter()
        .filter_map(|x| if x.is_empty() {None} else { Some(x.parse::<T>().unwrap()) })
        .collect();

    return data_content;
}

pub fn vec_string_range_to_range<T>(data: Vec<String>) -> Vec<Range<T>>
    where T:FromStr + Copy, T::Err: std::fmt::Debug,
{
    data.iter().filter_map(|range| {
        let z = range.split("-").map(|s| s.to_string()).collect();
        let q = vec_string_to_int::<T>(z);
        if q.len() == 2{
            Some(q[0]..q[1])
        } else {
            None
        }
    }).collect()
}

pub fn vec_string_to_char(line: Vec<String>) -> Vec<Vec<char>> {
    // Give a list of strings
    // Convert it to a list of list of chars
    let mut data_content: Vec<Vec<char>> = Vec::new();
    for element in line {
        data_content.push(string_to_char(element));
    }
    return data_content;
}


pub fn argsort<T: Ord>(data: &[T]) -> Vec<usize> {
    let mut indices = (0..data.len()).collect::<Vec<_>>();
    indices.sort_by_key(|&i| &data[i]);
    indices
}


pub fn consolidate_range<T>(range_x: &Range<T>, range_y: &Range<T>) -> Range<T>
where T:Copy + Ord {
    let mut new_range: Range<T> = range_x.clone();

    if range_x.start <= range_y.end && range_y.start <= range_x.end {
        new_range = range_x.start.min(range_y.start)
            ..range_x.end.max(range_y.end);
    }
    new_range
}