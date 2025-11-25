use rayon::prelude::*;
use std::time::Instant;

struct Lcg {
    state: u64,
}

impl Lcg {
    fn new(seed: u64) -> Self {
        Lcg { state: seed }
    }

    fn next(&mut self) -> i32 {
        // LCG constants from Numerical Recipes
        self.state = self
            .state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        (self.state >> 32) as i32
    }
}

fn main() {
    const SIZE: usize = 1_000_000;
    println!("Generating {} integers...", SIZE);

    let mut rng = Lcg::new(42);
    let mut arr = Vec::with_capacity(SIZE);
    for _ in 0..SIZE {
        arr.push(rng.next());
    }

    println!("Sorting...");
    let start = Instant::now();
    arr.par_sort_unstable();
    let duration = start.elapsed();

    println!("BENCHMARK_TIME: {:.6}", duration.as_secs_f64());
    println!("Sorted {} items in {:?}", SIZE, duration);

    // Verify sort (optional, but good for sanity)
    for i in 0..SIZE - 1 {
        if arr[i] > arr[i + 1] {
            panic!("Array not sorted at index {}", i);
        }
    }
}
