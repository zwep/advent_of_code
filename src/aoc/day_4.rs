use std::path::{Path};
use crate::utils::file;
use std::{env, char};
use std::str::FromStr;

fn get_neighbours(i: usize, j: usize, nrows: usize, ncols: usize) -> Vec<(usize, usize)>
{

    [(-1, 0), (-1, -1), (1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (1, -1)]
        .into_iter()
        .filter_map(|(di, dj)| {
            let ni = i.checked_add_signed(di)?;
            let nj = j.checked_add_signed(dj)?;

            if ni < nrows && nj < ncols {
                Some((ni, nj))
            } else {
                None
            }
        }).collect()
}

fn alter_data(data: &mut Vec<Vec<char>>) -> i32{
    // Get the size of the thing
    let n = data.len();
    let m = data[0].len();
    let mut available_rols = 0;
    // start looping over each position
    for i in 0..n {
        for j in 0..m {
            if data[i][j] != char::from_str("@").unwrap() {
                continue;
            }
            let mut monkey_counter = 0;
            let valid_ij_neighbours = get_neighbours(i, j, n, m);
            for valid_point in valid_ij_neighbours{
                if data[valid_point.0][valid_point.1] == '@' {
                    monkey_counter += 1;
                }
            }
            if monkey_counter < 4 {
                data[i][j] = '.';
                available_rols += 1;
            }
        }
    }
    available_rols
}

pub fn part_1(){
    println!("Starting part 1");
    let path = env::current_dir().unwrap().display().to_string();
    println!("The current directory is {}", path);
    let datapath = Path::new("data/day_4.txt");
    let file_seperator: &str = "\n";
    let loaded_data: _ = file::load_data(datapath, file_seperator);
    let mut data: Vec<Vec<char>> = file::vec_string_to_char(loaded_data);
    for idata in &data {
        println!("{:?}", idata);
    }

    let mut total_roles = 0;
    let mut delta_roles = 1;
    while delta_roles > 0 {
        delta_roles = alter_data(&mut data);
        total_roles += delta_roles;
        println!("{}", delta_roles);
    }

    for idata in &data {
        println!("{:?}", idata);
    }

    println!("Final value is {}", total_roles);
}
