# Milestone 4: Vyper ERC‑20 with Ape Framework

## Overview

In this movement, you'll compose a ten‑line Vyper ERC‑20 "PadawanToken", compile it with Ape's Vyper plugin, and unit‑test core functions (`mint`, `transfer`, `burn`) on a local mainnet fork. By the end, you'll understand on‑chain contract workflows from coding to automated tests.

## Objectives

- Scaffold an Ape project ready for Vyper compilation.
- Write a minimal Vyper ERC‑20 contract with name, symbol, decimals, and events.
- Compile your contract with the Ape Vyper plugin.
- Deploy and test the contract on a local chain with `ape test`.
- Learn how to assert state changes and read emitted events in tests.

## Prerequisites

1. Python 3.8+ with a virtual environment activated.
2. Completed Milestones 1–3: SHA256 chaining, block header parsing, Taproot wallet demo.
3. Installed dependencies:
   ```bash
   pip install eth-ape ape-vyper
   ```
4. Ape project initialized in your repo root (via `ape init`).

## Steps

1.  **Add Your Contract**

    - Create `contracts/Token.vy` with the Vyper ERC‑20 code:

      ```vyper # @version ^0.3.7
      NULL_ADDRESS: constant(address) = 0x000...000

           event Transfer:
               sender: indexed(address)
               receiver: indexed(address)
               value: uint256

           name: public(String[64])
           symbol: public(String[32])
           decimals: public(uint256)
           balances: public(HashMap[address, uint256])

           @external

      def **init**():
      self.name = "PadawanToken"
      self.symbol = "PAD"
      self.decimals = 18

           @external

      def mint(to: address, amount: uint256):
      self.balances[to] += amount
      log Transfer(NULL_ADDRESS, to, amount)

           @external

      def burn(amount: uint256):
      self.balances[msg.sender] -= amount
      log Transfer(msg.sender, NULL_ADDRESS, amount)

           @external

      def transfer(to: address, amount: uint256) -> bool:
      assert self.balances[msg.sender] >= amount
      self.balances[msg.sender] -= amount
      self.balances[to] += amount
      log Transfer(msg.sender, to, amount)
      return True
      ```

2.  **Compile Contracts**

    ```bash
    ape compile
    ```

    You should see a SUCCESS message for `Token.vy`.

3.  **Write Unit Tests**

    - Create `tests/test_token.py` and verify:
      - **mint** increases `balances(owner)`
      - **transfer** moves tokens and updates balances
      - **burn** decreases supply and emits the correct event
    - Example test structure:

      ```python
      import ape

      def test_mint_burn_transfer(project, accounts):
          owner = accounts[0]
          receiver = accounts[1]
          token = project.Token.deploy(sender=owner)
          initial = token.balances(owner)
          token.mint(owner, 1_000 * 10**18, sender=owner)
          assert token.balances(owner) == initial + 1_000 * 10**18
          token.transfer(receiver, 100 * 10**18, sender=owner)
          assert token.balances(receiver) == 100 * 10**18
          token.burn(50 * 10**18, sender=owner)
          assert token.balances(owner) == initial + 900 * 10**18 - 50 * 10**18
      ```

4.  **Run Tests**
    ```bash
    ape test
    ```
    All tests should pass green.

## Expected Output

- **Compilation** logs a successful compile of `Token.vy`.
- **Test run** shows a single test suite passing with no errors.

```
$ ape test
==== test session starts ====
collected 1 item

tests/test_token.py . [100%]

==== 1 passed in 0.3s ====
```

## Next Steps

- Script a Python bot to watch the `Transfer` event and react off‑chain.
- Slide into Milestone 5: stream live USDC transfers into a graph, then train a GNN to spot anomalies. 🎷📈
