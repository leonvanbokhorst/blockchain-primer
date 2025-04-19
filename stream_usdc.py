#!/usr/bin/env python3
"""stream_usdc.py: Stream USDC Transfer events from Ethereum mainnet."""

import os
import sys
import time
import json
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
USDC_ABI_MINIMAL = """
[
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "Transfer",
    "type": "event"
  }
]
"""


def stream_transfers(w3, contract):
    """Continuously poll for new Transfer events and yield them."""
    event_filter = contract.events.Transfer.create_filter(fromBlock="latest")
    while True:
        try:
            new_events = event_filter.get_new_entries()
            for event in new_events:
                yield (event.args["from"], event.args["to"], event.args["value"])
        except Exception as e:
            print(f"Error fetching events: {e}", file=sys.stderr)
            time.sleep(5)  # Avoid rapid-fire errors
        time.sleep(15)  # Poll every 15 seconds


def main():
    api_key = os.getenv("ALCHEMY_API_KEY") or os.getenv("INFURA_API_KEY")
    if not api_key:
        print(
            "Error: ALCHEMY_API_KEY or INFURA_API_KEY environment variable not set.",
            file=sys.stderr,
        )
        sys.exit(1)

    provider_url = f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"  # Assume Alchemy
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected():
        print(
            f"Error: Could not connect to provider at {provider_url}", file=sys.stderr
        )
        sys.exit(1)

    print(f"Connected to Ethereum mainnet provider.", file=sys.stderr)
    usdc_contract = w3.eth.contract(address=USDC_ADDRESS, abi=USDC_ABI_MINIMAL)
    print(f"Streaming USDC transfers from {USDC_ADDRESS}...", file=sys.stderr)

    for src, dst, val in stream_transfers(w3, usdc_contract):
        print(json.dumps({"src": src, "dst": dst, "value": val}), flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStream interrupted. Exiting.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error in main loop: {e}", file=sys.stderr)
        sys.exit(1)
