# Project: Silicon Colosseum (Rust vs Go)

## Official Benchmark Results
- **Team Rust**: ~3.8ms 🏆
- **Team Go**: ~21ms

## The Verdict
Rust emerged as the clear victor, executing over **5x faster** than Go.

### Why Rust Won
1.  **LLVM Optimizations**: Rust compiles to highly optimized machine code using the LLVM backend, which aggressively optimizes loops and memory access.
2.  **Zero-Cost Abstractions**: Rust's high-level features compile down to efficient machine instructions without runtime penalty.
3.  **No Runtime Overhead**: Unlike Go, Rust does not have a garbage collector or heavy runtime, allowing it to utilize every CPU cycle for the sorting algorithm itself.

### Why Go Lost
Go's performance was hindered by its runtime overhead. The disassembly reveals frequent checks and function calls that consume valuable cycles:
-   **Stack Checks**: Frequent calls to `runtime.morestack` to manage goroutine stacks.
-   **Runtime Type Information**: Overhead from interface and type assertions.
-   **Garbage Collection**: Background processes managing memory allocation.

## Disassembly of Shame
Here is a snippet from the Go binary (`go_warrior.exe`) showing the runtime overhead (stack checks and panic handling) that contributed to its defeat:

```assembly
1400012e0: e8 fb 7f 03 00              	callq	0x1400392e0 <runtime.panicshift>
1400012e5: 90                          	nop
1400012e6: 48 89 44 24 08              	movq	%rax, 0x8(%rsp)
1400012eb: e8 10 ed 06 00              	callq	0x140070000 <runtime.morestack_noctxt.abi0>
1400012f0: 48 8b 44 24 08              	movq	0x8(%rsp), %rax
1400012f5: e9 66 ff ff ff              	jmp	0x140001260 <internal/abi.Name.Name>
```

## How to Run the Arena

### Prerequisites
-   Rust (Cargo)
-   Go
-   Python 3

### Installation
1.  Create and activate a virtual environment (optional but recommended).
2.  Install Flask:
    ```bash
    pip install flask
    ```

### Running the Fight
1.  Start the Flask application:
    ```bash
    python app.py
    ```
2.  Open your browser to [http://localhost:5000](http://localhost:5000).
3.  Click the **"FIGHT!"** button to witness the battle.
