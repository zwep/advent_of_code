use std::fs;

// This is the main function.
fn main() {
    // Statements here are executed when the compiled binary is called.
    let contents = fs::read_to_string("data/day_1.txt")
        .expect("Could not read file");
    let parts:Vec<&str> = contents.split("\n").collect();

    for part in &parts {
        println!("{}", part);
    }
}