package main

import (
	"fmt"
	"math/rand"
	"sort"
	"sync"
	"time"
)

const (
	SIZE      = 1_000_000
	THRESHOLD = 10_000 // Fallback to sequential sort below this size
)

func main() {
	fmt.Printf("Generating %d integers...\n", SIZE)
	arr := make([]int, SIZE)
	rng := rand.New(rand.NewSource(42))
	for i := 0; i < SIZE; i++ {
		arr[i] = int(rng.Int31())
	}

	fmt.Println("Sorting...")
	start := time.Now()
	
	// Parallel Mergesort
	parallelMergesort(arr)
	
	duration := time.Since(start)
	fmt.Printf("BENCHMARK_TIME: %.6f\n", duration.Seconds())
	fmt.Printf("Sorted %d items in %v\n", SIZE, duration)

	// Verify
	if !sort.IntsAreSorted(arr) {
		panic("Array not sorted!")
	}
}

func parallelMergesort(arr []int) {
	if len(arr) <= THRESHOLD {
		sort.Ints(arr)
		return
	}

	mid := len(arr) / 2
	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		defer wg.Done()
		parallelMergesort(arr[:mid])
	}()

	parallelMergesort(arr[mid:])
	wg.Wait()

	merge(arr, mid)
}

func merge(arr []int, mid int) {
	left := make([]int, mid)
	copy(left, arr[:mid])
	
	// Right part is already in place in arr[mid:], but we need to merge into arr
	// We can just use standard merge logic
	// To avoid excessive allocation, we copied left. Right is arr[mid:].
	// We overwrite arr.
	
	i, j, k := 0, mid, 0
	for i < len(left) && j < len(arr) {
		if left[i] <= arr[j] {
			arr[k] = left[i]
			i++
		} else {
			arr[k] = arr[j]
			j++
		}
		k++
	}

	for i < len(left) {
		arr[k] = left[i]
		i++
		k++
	}
	// Remaining elements from right are already in place
}


