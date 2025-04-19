import ape


def test_mint_burn_transfer(token_contract, accounts):
    owner = accounts[0]
    receiver = accounts[1]
    initial_balance = token_contract.balances(owner)

    # Mint tokens to owner
    tx = token_contract.mint(owner, 1_000 * 10**18, sender=owner)
    assert token_contract.balances(owner) == initial_balance + 1_000 * 10**18

    # Transfer tokens to receiver
    tx = token_contract.transfer(receiver, 100 * 10**18, sender=owner)
    assert token_contract.balances(receiver) == 100 * 10**18
    assert token_contract.balances(owner) == initial_balance + 900 * 10**18

    # Burn some tokens
    tx = token_contract.burn(50 * 10**18, sender=owner)
    assert token_contract.balances(owner) == initial_balance + 850 * 10**18
