#!/usr/bin/env python3
"""Demo hashing 'Lonn' 1000 times using SHA256."""
import hashlib


def hash_chain(data: bytes, iterations: int) -> bytes:
    h = data
    for _ in range(iterations):
        h = hashlib.sha256(h).digest()
    return h


def main():
    initial = b"Lonn"
    final_hash = hash_chain(initial, 1000)
    print(f"Final hash after 1000 rounds: {final_hash.hex()}")


if __name__ == "__main__":
    main()
