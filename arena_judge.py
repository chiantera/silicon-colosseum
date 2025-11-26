import subprocess
import time
import os
import sys
import shutil
import platform

# Detect OS
IS_WINDOWS = platform.system() == "Windows"
EXE_EXT = ".exe" if IS_WINDOWS else ""

# Configuration - Dynamic paths using shutil.which to find executables in PATH
# This works on both Windows (if in PATH) and Linux (Docker container)
RUSTC_PATH = shutil.which("rustc") or "rustc"
CARGO_PATH = shutil.which("cargo") or "cargo"
GO_PATH = shutil.which("go") or "go"

# objdump usually comes with build-essential or binutils in Linux
OBJDUMP_PATH = shutil.which("objdump") or "objdump"

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
        print(f"Compiler not found: {CARGO_PATH}")
        return False

def compile_go():
    print("Compiling Team Go...")
    try:
        # Output binary name depends on OS
        out_name = f"go_warrior{EXE_EXT}"
        subprocess.run([GO_PATH, "build", "-o", out_name, "team_go/main.go"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Team Go failed to compile!")
        return False
    except FileNotFoundError:
        print(f"Compiler not found: {GO_PATH}")
        return False

def run_warrior(executable):
    # Ensure executable path has correct extension if needed
    if IS_WINDOWS and not executable.endswith(EXE_EXT):
        executable += EXE_EXT
        
    # On Linux/Mac, local executables need ./ prefix if not in PATH
    if not IS_WINDOWS and not os.path.isabs(executable) and not executable.startswith("./"):
        executable = "./" + executable

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
        # Return infinite time on failure so the other team wins
        return float('inf'), output
    except Exception as e:
        print(f"Error running {executable}: {e}")
        return float('inf'), ""

def disassemble(executable):
    # Fix path for disassembly
    if IS_WINDOWS and not executable.endswith(EXE_EXT):
        executable += EXE_EXT
    if not IS_WINDOWS and not os.path.isabs(executable) and not executable.startswith("./"):
        executable = "./" + executable
        
    print(f"Disassembling {executable}...")
    try:
        with open("shame.txt", "w") as f:
            # Use standard objdump args
            subprocess.run([OBJDUMP_PATH, "-d", "-C", executable], stdout=f, stderr=subprocess.DEVNULL)
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
    
    # Paths relative to project root
    rust_bin = "team_rust/target/release/team_rust"
    go_bin = "go_warrior"
    
    rust_time, rust_out = run_warrior(rust_bin)
    print(f"Team Rust: {rust_time:.6f}s")
    
    go_time, go_out = run_warrior(go_bin)
    print(f"Team Go:   {go_time:.6f}s")

    print("\nRESULTS:")
    winner = "DRAW"
    shame_output = ""
    
    # Logic: Lowest time wins. If both inf, nobody wins.
    if rust_time == float('inf') and go_time == float('inf'):
        winner = "BOTH_DIED"
        shame_output = "Both warriors failed to report time."
    elif rust_time < go_time:
        print("   RUST WINS!")
        winner = "RUST"
        disassemble(go_bin) # Shame the loser (Go)
    else:
        print("   GO WINS!")
        winner = "GO"
        disassemble(rust_bin) # Shame the loser (Rust)
        
    try:
        if os.path.exists("shame.txt"):
            with open("shame.txt", "r") as f:
                # Read only first 2000 chars to avoid huge JSON payload
                shame_output = f.read(2000) + "\n... (truncated)"
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