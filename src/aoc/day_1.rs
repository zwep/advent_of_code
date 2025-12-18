use std::fs;

// This is the main function.
pub fn main() {
    // Statements here are executed when the compiled binary is called.
    let contents = fs::read_to_string("data/day_1.txt")
        .expect("Could not read utils");
    let parts:Vec<&str> = contents.split("\n").collect();
    let mut position = 50;
    let rotation_size = 100;
    let mut password = 0;

    for part in &parts {
        let direction = &part[0..1];
        let size = &part[1..].parse::<i32>().unwrap();
        println!("direction: {}\nsize: {}", direction, size);
        // Always do this...
        password += size / rotation_size;
        let netto_size = size % rotation_size;
        if direction == "L" {
            if (netto_size > position) & (position != 0) {
                password += 1
            }
            position = (position - size) % rotation_size;
        } else {
            if netto_size > (rotation_size - position) {
                password += 1
            }
            position = (position + size) % rotation_size;
        }
        position = position % rotation_size;
        println!("position: {}\npassword: {}", position, password);
        if position < 0 {
            position = rotation_size + position;
        }
        if position == 0 {
            password += 1;
        }
        println!("new position: {}\npassword: {}", position, password);

        println!("------------- {}", password);
    }
    println!("{}", password);
}