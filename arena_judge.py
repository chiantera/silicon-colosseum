import subprocess
import time
import os
import sys

# Configuration - Absolute paths
RUSTC_PATH = r"C:\Users\faust\.cargo\bin\rustc.exe"
CARGO_PATH = r"C:\Users\faust\.cargo\bin\cargo.exe"
GO_PATH = r"C:\Program Files\Go\bin\go.exe"
OBJDUMP_PATH = r"C:\Users\faust\.rustup\toolchains\stable-x86_64-pc-windows-msvc\lib\rustlib\x86_64-pc-windows-msvc\bin\llvm-objdump.exe"

def compile_rust():
    print("Compiling Team Rust (Cargo)...")
    try:
        # Build with Cargo
        subprocess.run([CARGO_PATH, "build", "--release", "--manifest-path", "team_rust/Cargo.toml"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Team Rust failed to compile!")
        return False
    except FileNotFoundError:
        print(f"Compiler not found at {CARGO_PATH}")
        return False

def compile_go():
    print("Compiling Team Go...")
    try:
        subprocess.run([GO_PATH, "build", "-o", "go_warrior.exe", "team_go/main.go"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Team Go failed to compile!")
        return False
    except FileNotFoundError:
        print(f"Compiler not found at {GO_PATH}")
        return False

def run_warrior(executable):
    try:
        result = subprocess.run([executable], capture_output=True, text=True)
        output = result.stdout
        
        # Parse BENCHMARK_TIME
        for line in output.splitlines():
            if "BENCHMARK_TIME:" in line:
                try:
                    time_str = line.split(":")[1].strip()
                    return float(time_str), output
                except ValueError:
                    pass
        
        print(f"⚠️  Could not find BENCHMARK_TIME in output for {executable}")
        return float('inf'), output
    except Exception as e:
        print(f"Error running {executable}: {e}")
        return float('inf'), ""

def disassemble(executable):
    print(f"Disassembling {executable}...")
    try:
        # Try to find objdump in the same dir as g++ or just in path
        objdump = OBJDUMP_PATH
        with open("shame.txt", "w") as f:
            subprocess.run([objdump, "-d", executable], stdout=f)
        print("   -> Shame dumped to shame.txt")
    except Exception as e:
        print(f"   -> Could not disassemble: {e}")

def run_match():
    print("WELCOME TO THE CODE ARENA")
    
    rust_ok = compile_rust()
    go_ok = compile_go()

    if not rust_ok or not go_ok:
        print("Compilation failed. Match cancelled.")
        return {
            "error": "Compilation failed",
            "rust_ok": rust_ok,
            "go_ok": go_ok
        }

    print("\nFIGHT!")
    
    rust_time, rust_out = run_warrior("team_rust/target/release/team_rust.exe")
    print(f"Team Rust: {rust_time:.6f}s")
    
    go_time, go_out = run_warrior("./go_warrior.exe")
    print(f"Team Go:   {go_time:.6f}s")

    print("\nRESULTS:")
    winner = "DRAW"
    shame_output = ""
    
    if rust_time < go_time:
        print("   RUST WINS!")
        winner = "RUST"
        disassemble("go_warrior.exe")
    else:
        print("   GO WINS!")
        winner = "GO"
        disassemble("team_rust/target/release/team_rust.exe")
        
    try:
        with open("shame.txt", "r") as f:
            shame_output = f.read()
    except:
        shame_output = "Could not read shame.txt"

    return {
        "winner": winner,
        "rust_time": rust_time,
        "go_time": go_time,
        "rust_out": rust_out,
        "go_out": go_out,
        "shame": shame_output
    }

if __name__ == "__main__":
    run_match()