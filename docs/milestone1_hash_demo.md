# Milestone 1: SHA256 Hash Chaining Demo

## Overview

In this exercise, we explore the core concept of cryptographic hashing by chaining SHA256 hashes. We will repeatedly hash the initial string "Lonn" 1,000 times, observing how each iteration transforms the data and how tiny differences in input lead to completely different outputs.

## Objectives

- Understand the properties of a cryptographic hash (determinism, preimage resistance, avalanche effect).
- Learn how to use Python's built-in `hashlib` library for SHA256 hashing.
- Practice writing and structuring a simple Python script with functions and a `main` guard.
- Gain confidence running scripts in a virtual environment and tracking changes with Git.

## Prerequisites

1. Python 3.8+ installed
2. A virtual environment set up and activated (instructions in `requirements.txt`)
3. The `bitcoinlib` library installed (installed via `pip install bitcoinlib`)
4. Git repository initialized for this project

## Steps

1. **Inspect the Script**

   - Open `hash_demo.py` and review the `hash_chain` function.
   - Note how the loop applies `sha256` to the previous digest each iteration.

2. **Run the Demo**

   ```bash
   chmod +x hash_demo.py
   ./hash_demo.py
   ```

   You should see a final hex digest printed to the console.

3. **Experiment**

   - Change the number of iterations (e.g., 500 or 5000) and observe how the final digest changes.
   - Try a different initial string to reinforce the avalanche effect.

4. **Commit Your Work**
   ```bash
   git add hash_demo.py requirements.txt
   git commit -m "Milestone 1: SHA256 chaining demo"
   ```

## Expected Output

A single line similar to:

```
Final hash after 1000 rounds: ab12cd34... (64 hex characters)
```

Every run with the same initial string and iteration count should produce the same digest.

## Next Steps

Once you're comfortable with chaining hashes, we'll move on to parsing real Bitcoin block headers and verifying their difficulty targets. Onward to the toy chain! 🎷🔒
