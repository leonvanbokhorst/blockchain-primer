# Milestone 3: Taproot Test‑net Wallet Demo

## Overview

In this exercise, we'll step beyond passive parsing into real‑world blockchain transactions. You'll create or open a Bitcoin test‑net wallet with a P2TR (Taproot) address, fund it via a faucet, and send a transaction to another test‑net address.

## Objectives

- Use `bitcoinlib` to create and manage a Taproot (P2TR) wallet on Bitcoin test‑net.
- Understand mnemonic‑based wallet recovery and key derivation.
- Interact with the Bitcoin network: fund an address, build and broadcast a transaction.
- Practice real‑world error handling when constructing and sending transactions.

## Prerequisites

1. Virtual environment with `bitcoinlib` installed (see `requirements.txt`).
2. Access to a Bitcoin test‑net faucet.
3. The `wallet_demo.py` script at project root.

## Steps

1. **Review the Script**

   - Open `wallet_demo.py` and inspect `create_taproot_wallet`:
     - How it opens/creates a wallet with `network='testnet'`.
     - Derives a new key with `script_type='p2tr'`.
   - Note how `wallet.send_to()` constructs and broadcasts a TX.

2. **Run the Demo**

   ```bash
   chmod +x wallet_demo.py
   ./wallet_demo.py
   ```

   - The script will print a new Taproot address and public key.
   - It will pause, awaiting you to fund the address via a test‑net faucet.

3. **Fund Your Address**

   - Copy the displayed address and use a reliable faucet (e.g., https://testnet-faucet.mempool.co/) to send a few tBTC.
   - Wait for one or two confirmations.

4. **Broadcast a Transaction**

   - Press Enter in the script once your address is funded.
   - Input a destination test‑net address and the amount of BTC to send.
   - The script will build, sign, and broadcast the transaction.
   - It prints the TXID and a link to view it on a test‑net explorer.

5. **Commit Your Work**
   ```bash
   git add wallet_demo.py docs/milestone3_taproot_wallet.md
   git commit -m "Milestone 3: Taproot test‑net wallet demo"
   ```

## Expected Output

A console session resembling:

```
Initializing Taproot testnet wallet 'taproot_ninja_wallet'...
  Address:    tb1p...xyz
  Public key: 03ab...cd

Please fund this address using a testnet faucet, then press Enter to continue.

Enter a destination testnet address: tb1q...abc
Enter amount in BTC to send: 0.001

Sending 0.001 BTC to tb1q...abc...
Transaction broadcast! TXID: e2f3...789
View on testnet explorer: https://mempool.space/testnet/tx/e2f3...789
```

## Next Steps

With on‑chain transactions under your belt, the next layer is smart contracts. Let's slide into Milestone 4 by scaffolding a Vyper ERC‑20 with the Ape Framework, and unit‑test its mint, burn, and transfer functions. 🎷🔗
