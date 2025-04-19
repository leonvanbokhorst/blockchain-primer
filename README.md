# Blockchain Primer

This repository follows a hands-on curriculum designed to build intuition for blockchain concepts through practical Python exercises. Think of it as learning riffs that gradually weave into a larger solo, moving from fundamental cryptography to on-chain analysis with graph neural networks.

## Curriculum Overview

The journey progresses through five key milestones:

1.  **Hashing & Immutability:** Understanding cryptographic hash functions and how they build chains.
2.  **Bitcoin Core Concepts:** Parsing real block headers and transactions.
3.  **Testnet Interaction:** Creating wallets and broadcasting live (testnet) transactions.
4.  **Smart Contracts:** Writing and testing a simple ERC-20 token with Ape/Vyper.
5.  **On-Chain Analysis:** Streaming live data and applying GNNs for anomaly detection.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd blockchain-primer
    ```

2.  **Create and activate a Python virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: Depending on your OS and Python version, you might encounter specific installation issues for packages like `torch` or `torch_geometric`. Refer to their official documentation if needed.)_

4.  **API Keys (for Milestone 5):** Obtain an API key from a provider like [Alchemy](https://www.alchemy.com/) or [Infura](https://www.infura.io/). Create a `.env` file in the project root:
    ```plaintext
    # .env
    ALCHEMY_API_KEY="your_key_here"
    # or INFURA_API_KEY="your_key_here"
    ```
    The scripts will load this automatically.

## Milestones & Code

Each milestone has associated Python scripts and detailed documentation.

### Milestone 1: SHA256 Hash Chaining

- **Goal:** Implement SHA256 hash chaining.
- **Code:** [`hash_demo.py`](./hash_demo.py)
- **Docs:** [`docs/milestone1_hash_demo.md`](./docs/milestone1_hash_demo.md)
- **Run:** `python hash_demo.py` or `./hash_demo.py` (after `chmod +x`)

### Milestone 2: Bitcoin Block Header & Coinbase

- **Goal:** Fetch and parse a Bitcoin block header and its coinbase transaction.
- **Code:** [`block_header_demo.py`](./block_header_demo.py)
- **Docs:** [`docs/milestone2_block_header.md`](./docs/milestone2_block_header.md)
- **Run:** `./block_header_demo.py`

### Milestone 3: Taproot Testnet Wallet

- **Goal:** Create a Taproot wallet, fund it via a testnet faucet, and broadcast a transaction.
- **Code:** [`wallet_demo.py`](./wallet_demo.py)
- **Docs:** [`docs/milestone3_taproot_wallet.md`](./docs/milestone3_taproot_wallet.md)
- **Run:** `./wallet_demo.py` (interactive - requires faucet funding)

### Milestone 4: Vyper ERC-20 with Ape

- **Goal:** Write and test a simple ERC-20 token using Vyper and the Ape framework.
- **Contract:** [`contracts/Token.vy`](./contracts/Token.vy)
- **Tests:** [`tests/test_token.py`](./tests/test_token.py)
- **Docs:** [`docs/milestone4_vyper_erc20.md`](./docs/milestone4_vyper_erc20.md)
- **Run Tests:** `ape test`

### Milestone 5: USDC Streaming & GNN Anomaly Detection

- **Goal:** Stream live USDC transfers, build a graph, and use a GAE to detect anomalous transfers.
- **Code (Streamer):** [`stream_usdc.py`](./stream_usdc.py)
- **Code (GNN):** [`gnn_train.py`](./gnn_train.py)
- **Docs:** [`docs/milestone5_usdc_graph_gnn.md`](./docs/milestone5_usdc_graph_gnn.md)
- **Run Pipeline:** `./stream_usdc.py | ./gnn_train.py` (Requires API key in `.env`)
