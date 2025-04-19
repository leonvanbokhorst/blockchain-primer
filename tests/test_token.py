# Use `project` and `accounts` fixtures to deploy and test within the test function
import pytest
import ape


@pytest.fixture
def token_contract(project, accounts):
    # Deploy the Token contract for testing
    owner = accounts[0]
    return project.Token.deploy(sender=owner)


def test_mint_burn_transfer(project, accounts):
    # Deploy the Token contract for testing
    owner = accounts[0]
    receiver = accounts[1]
    token = project.Token.deploy(sender=owner)
    initial_balance = token.balances(owner)

    # Mint 1000 tokens to owner
    token.mint(owner, 1_000 * 10**18, sender=owner)
    assert token.balances(owner) == initial_balance + 1_000 * 10**18

    # Transfer 100 tokens to receiver
    token.transfer(receiver, 100 * 10**18, sender=owner)
    assert token.balances(receiver) == 100 * 10**18
    assert token.balances(owner) == initial_balance + 900 * 10**18

    # Burn 50 tokens from owner
    token.burn(50 * 10**18, sender=owner)
    assert token.balances(owner) == initial_balance + 850 * 10**18
