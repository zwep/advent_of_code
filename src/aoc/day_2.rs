use std::fs;
use std::collections::HashSet;


fn construct_valid_number(x: i64, m: i64) -> i64 {
    let x_length = x.ilog10() as i64 + 1;
    let mut s = 0;
    for i in 0..x_length{
        if i % m == 0 {
            s += 10_i64.pow(i as u32);
        }
    }
    //println!("x: {}, m: {}", (x % 10_i64.pow(m as u32)), x);
    // here... if
    if x % 10_i64.pow(m as u32) == 0 {
        (x % 10_i64.pow(m as u32)) * s
    } else if ((x % 10_i64.pow(m as u32)).ilog10() + 1) != m as u32 {
        (x % 10_i64.pow(m as u32)) * s
    } else {
        (x % 10_i64.pow(m as u32)) * s
    }

}

// This is the main function.
pub fn main() {
    // Statements here are executed when the compiled binary is called.
    let contents = fs::read_to_string("data/day_2.txt")
        .expect("Could not read utils");
    let lines: Vec<&str> = contents.split(",").collect();
    let mut result_list = Vec::new();

    for line in &lines {
        let components: Vec<&str> = line.split("-").collect();
        // Lets own these strings
        let lower_bound = components[0].parse::<i64>().unwrap();
        let upper_bound = components[1].parse::<i64>().unwrap();
        for x in lower_bound..=upper_bound {
            // the 'length' of it.
            let x_length = x.ilog10() as i64 + 1;
            let mut max_size = x_length/2;
            if x_length % 2 == 1{
                max_size = 1;
            }
            for n in 1..max_size+1 {
                //println!("constructed nr {} {}", construct_valid_number(x, n), n);
                if x == construct_valid_number(x, n){
                    println!("{} -- {}",x, n);
                    result_list.push(x)
                }
            }
        }
    }
    let unique: HashSet<_> = result_list.into_iter().collect();
    let sum: i64 = unique.iter().sum();
    println!("{}", sum);
    // too high
    // 66501300881 - 90909 - 30303-50505-40404-60606-80808
    // too low
    // 64959405848
    // lol
    //66500947346
}