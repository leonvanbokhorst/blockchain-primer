# Milestone 2: Bitcoin Block Header & Coinbase Demo

## Overview

This exercise takes you from hashing riffs to the real blockchain stage. We'll fetch block 800000 from Bitcoin mainnet, inspect its header fields, verify the difficulty target, and decode the coinbase transaction's scriptSig.

## Objectives

- Use `bitcoinlib` to interact with a Bitcoin node or service.
- Understand how block headers are structured: version, previous hash, Merkle root, timestamp, bits, and nonce.
- Convert the compact `bits` field into a full target and calculate difficulty.
- Extract and interpret the coinbase transaction payload from the scriptSig.

## Prerequisites

1. Virtual environment with `bitcoinlib` installed (see `requirements.txt`).
2. A running Bitcoin node or access to a public service (default `Service()` will use bitcoinlib's default API).
3. The `block_header_demo.py` script at project root.

## Steps

1. **Review the Script**

   - Open `block_header_demo.py` and inspect the functions `bits_to_target` and `target_to_difficulty`.
   - Note how `Service` is used to fetch block data and raw transactions.

2. **Run the Demo**

   ```bash
   chmod +x block_header_demo.py
   ./block_header_demo.py
   ```

   You should see:

   - Block header fields printed.
   - Both RPC-reported and calculated difficulty values.
   - The coinbase TX ID and scriptSig hex.
   - A decoded preview of the coinbase data (often human-readable miner messages).

3. **Experiment**

   - Change `height` to another block (e.g., 700000) and observe new header values.
   - Modify the decoding logic to extract timestamp or embedded messages.

4. **Commit Your Work**
   ```bash
   git add block_header_demo.py docs/milestone2_block_header.md
   git commit -m "Milestone 2: Block header and coinbase demo"
   ```

## Expected Output

A console session resembling:

```
Fetching block at height 800000...

Block Header:
  Hash:             00000000000000000007d0f...
  Version:          536870912
  Previous Block:   0000000000000000000a...
  Merkle Root:      4c9d0b0...
  Time:             1601423417
  Bits (hex):       170d74ac
  Difficulty (RPC): 15.34e6
  Calculated Diff:  1.534000e+07

Coinbase Transaction:
  TX ID: e3a1...
  Raw scriptSig hex: 034f5f...
  Decoded coinbase data: /Satoshi added extra text/
```

## Next Steps

Once you're comfortable with header parsing, we'll build a tiny wallet to generate a Taproot key pair and broadcast a transaction on test‑net. Let's keep this solo rolling! 🎷🔍
