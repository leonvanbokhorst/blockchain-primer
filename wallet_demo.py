#!/usr/bin/env python3
"""Demo: Create a Taproot wallet on Bitcoin testnet and broadcast a transaction."""
import sys
from decimal import Decimal
from bitcoinlib.wallets import wallet_create_or_open


def create_taproot_wallet(name: str, mnemonic: str = None):
    """Create or open a testnet wallet and derive a new Taproot key."""
    wallet = wallet_create_or_open(name, keys=mnemonic, network="testnet")
    # Derive a new default key (e.g., SegWit) for compatibility
    key = wallet.new_key()
    return wallet, key


def main():
    wallet_name = "taproot_ninja_wallet"
    print(f"Initializing Taproot testnet wallet '{wallet_name}'...")
    wallet, key = create_taproot_wallet(wallet_name)
    print(f"  Address:    {key.address}")
    print(f"  Public key: {key.key_public.hex()}")
    print(
        "\nPlease fund this address using a testnet faucet, then press Enter to continue."
    )
    input()

    to_address = input("Enter a destination testnet address: ").strip()
    amount = Decimal(input("Enter amount in BTC to send: ").strip())
    print(f"\nSending {amount} BTC to {to_address}...")
    try:
        # Use the correct 'fee' parameter (in satoshis) and enable immediate broadcast
        tx = wallet.send_to(to_address, amount, fee=1000, broadcast=True)
        print(f"Transaction broadcast! TXID: {tx.txid}")
        print(f"View on testnet explorer: https://mempool.space/testnet/tx/{tx.txid}")
    except Exception as e:
        print(f"Error broadcasting transaction: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
