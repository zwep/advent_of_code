use std::collections::HashSet;
use std::env;
use std::fmt::{Debug, Display};
use std::ops::Range;
use std::path::Path;
use crate::utils::file;
use crate::utils::file::{consolidate_range, vec_char_to_int, vec_string_range_to_range, vec_string_to_int, vec_string_to_vec_int};

pub fn part_1(){
    println!("Starting part 1");
    let path = env::current_dir().unwrap().display().to_string();
    println!("The current directory is {}", path);
    let datapath = Path::new("data/day_5.txt");
    let file_seperator: &str = "\n";
    let loaded_data: _ = file::load_data(datapath, file_seperator);
    println!("{:?}", loaded_data);
    // Split the data
    let empty_index = loaded_data.iter().position(|n| n.is_empty()).unwrap();
    let (index_ranges,index_values) = loaded_data.split_at(empty_index);
    // Preprocess the index values
    let index_values = vec_string_to_int::<u64>(index_values.to_vec());
    // Preprocess the index ranges
    let index_range = vec_string_range_to_range::<u64>(index_ranges.to_vec());
    println!("{:?}", index_range);

    let mut containing_stuff = 0;
    for some_value in index_values {
        for some_range in &index_range {
            if some_range.contains(&some_value){
                println!("{}", some_value);
                containing_stuff += 1;
                break;
            };
        }
    }
    println!("total {}", containing_stuff);
}

fn consolidate_vec_of_ranges<T>(mut range_vec: Vec<Range<T>>) -> Vec<Range<T>>
    where T:Copy + Ord + Display + Debug
{
    let mut new_index_range: Vec<Range<T>> = Vec::new();
    while range_vec.len() > 0 {
        let mut current_range = range_vec.pop().unwrap();
        println!("Current range {:?}", current_range);
        println!("New index range length {}", new_index_range.len());
        loop {
            println!("Current range length {:?}", range_vec.len());
            let mut to_be_removed = Vec::new();
            for (i, xrange) in range_vec.iter().enumerate() {
                let new_range = consolidate_range(&current_range, xrange);
                // If the new range is different from the one we started with
                // Then this means that xrange is consolidated in current_range
                // And it (xrange) is marked for deletion
                if new_range != current_range {
                    println!("Consolidated {:?} and {:?} -> {:?}", current_range, xrange, new_range);
                    to_be_removed.push(i);
                    current_range = new_range;
                }
            }

            // If nothing is to be removed, then we are done...
            if to_be_removed.is_empty(){
                println!("Nothing has changed\n--------------");
                if !new_index_range.contains(&current_range){
                    new_index_range.push(current_range);
                }
                break;
            }
            for i in to_be_removed.into_iter().rev() {
                println!("\t Removing index {:?}", i);
                range_vec.swap_remove(i);
            }
        }
    }
    new_index_range
}
pub fn part_2(){
    println!("Starting part 2 - range consolidation");
    let path = env::current_dir().unwrap().display().to_string();
    println!("The current directory is {}", path);
    let datapath = Path::new("data/day_5.txt");
    let file_seperator: &str = "\n";
    let loaded_data: _ = file::load_data(datapath, file_seperator);
    // Split the data
    let empty_index = loaded_data.iter().position(|n| n.is_empty()).unwrap();
    let (index_ranges, _) = loaded_data.split_at(empty_index);
    // Preprocess the index ranges
    let index_range = vec_string_range_to_range::<u64>(index_ranges.to_vec());
    // Cloning the index ranges so we can alter them...?
    let mut current_index_range = index_range.clone();
    current_index_range.sort_by_key(|x| x.start);
    current_index_range.reverse();

    let new_range = consolidate_vec_of_ranges(current_index_range);
    println!("--->{}", &new_range.len());
    let new_range_2 = consolidate_vec_of_ranges(new_range);
    println!("--->{}", new_range_2.len());
    let new_range_3 = consolidate_vec_of_ranges(new_range_2);
    println!("--->{}", new_range_3.len());
    let new_range_4 = consolidate_vec_of_ranges(new_range_3);
    println!("--->{}", new_range_4.len());
    // too high
    // 381288701878261
    // still too high
    // 361380415036900
    // 373270476964079
    // 341753674214273 -- got it
    let mut s = 0;
    for x in new_range_4{
        s += x.end - x.start + 1;
    }
    println!("Result: {}", s);
}