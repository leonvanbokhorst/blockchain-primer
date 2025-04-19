#!/usr/bin/env python3
"""Demo: Create a Taproot wallet on Bitcoin testnet and broadcast a transaction."""
import sys
from decimal import Decimal
from bitcoinlib.wallets import wallet_create_or_open


def create_taproot_wallet(name: str, mnemonic: str = None):
    """Create or open a testnet wallet and derive or reuse the Taproot key."""
    if mnemonic:
        wallet = wallet_create_or_open(name, keys=mnemonic, network="testnet")
    else:
        wallet = wallet_create_or_open(name, network="testnet")
    # Reuse the first existing key if it exists, else derive a new one
    existing_keys = wallet.keys()
    key = existing_keys[0] if existing_keys else wallet.new_key()
    return wallet, key


def main():
    wallet_name = "taproot_ninja_wallet"
    print(f"Initializing Taproot testnet wallet '{wallet_name}'...")

    wallet, key = create_taproot_wallet(wallet_name)
    # Refresh and detect new incoming faucet funds
    print("\nRefreshing wallet UTXOs to detect faucet funds...")
    wallet.utxos_update()
    balance_sats = wallet.balance()
    # Convert satoshis to BTC
    balance_btc = Decimal(balance_sats) / Decimal("1e8")
    print(f"  Current balance: {balance_btc} BTC ({balance_sats} sats)")
    # Print public key for both WalletKey and DbKey, convert to hex if bytes
    try:
        pub = key.key_public
    except AttributeError:
        pub = key.public
    pub_hex = pub.hex() if isinstance(pub, (bytes, bytearray)) else str(pub)
    print(f"  Public key: {pub_hex}")
    print(f"  Address: {key.address}")
    print(
        "\nPlease fund this address using a testnet faucet, then press Enter to continue."
    )
    input()

    to_address = input("Enter a destination testnet address: ").strip()
    amount_btc = Decimal(input("Enter amount in BTC to send: ").strip())
    # Convert BTC amount to integer satoshis for wallet.send_to
    amount_sats = int(amount_btc * Decimal("1e8"))
    print(f"\nSending {amount_btc} BTC ({amount_sats} sats) to {to_address}...")
    try:
        # Use the correct 'fee' parameter (in satoshis) and enable immediate broadcast
        tx = wallet.send_to(to_address, amount_sats, fee=1000, broadcast=True)
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
