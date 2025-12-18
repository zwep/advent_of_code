use std::fs;
use std::path::Path;
use std::str::FromStr;

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

pub fn vec_string_to_int<T>(line: Vec<String>) -> Vec<Vec<T>>
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
