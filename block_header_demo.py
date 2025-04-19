#!/usr/bin/env python3
"""Demo fetching and parsing Bitcoin block 800000 header and coinbase TX."""
from bitcoinlib.services.services import Service
from binascii import unhexlify


def bits_to_target(bits: int) -> int:
    exp = bits >> 24
    mant = bits & 0xFFFFFF
    return mant * 2 ** (8 * (exp - 3))


def target_to_difficulty(target: int) -> float:
    # Maximum target (difficulty 1) for Bitcoin
    max_target = 0xFFFF * 2 ** (8 * (0x1D - 3))
    return max_target / target


def main():
    s = Service()
    height = 800000
    print(f"Fetching block at height {height}...")
    block = s.getblock(height)

    print("\nBlock Header:")
    print(f"  Hash:             {block.block_hash.hex()}")
    print(f"  Version:          {block.version_int}")
    print(f"  Previous Block:   {block.prev_block.hex()}")
    print(f"  Merkle Root:      {block.merkle_root.hex()}")
    print(f"  Time:             {block.time}")
    print(f"  Bits (hex):       {hex(block.bits_int)}")
    print(f"  Difficulty (RPC): {block.difficulty}")

    bits_int = block.bits_int
    target = bits_to_target(bits_int)
    calc_diff = target_to_difficulty(target)
    print(f"  Calculated Diff:  {calc_diff:.6e}")

    print("\nCoinbase Transaction:")
    # Extract coinbase transaction and data
    coinbase_tx = block.transactions[0]
    print(f"  TX ID: {coinbase_tx.txid}")
    # The actual coinbase payload is in the unlocking_script of the first input
    coinbase_input = coinbase_tx.inputs[0]
    coinbase_bytes = coinbase_input.unlocking_script
    coinbase_hex = coinbase_bytes.hex()
    print(f"  Raw coinbase hex: {coinbase_hex}")
    try:
        # Decode payload directly from bytes
        decoded = coinbase_bytes.decode("utf-8", errors="ignore")
        print(f"  Decoded coinbase data: {decoded}")
    except Exception as e:
        print(f"  Could not decode coinbase data: {e}")


if __name__ == "__main__":
    main()
