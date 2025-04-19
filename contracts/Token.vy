# @version ^0.3.7
ZERO_ADDRESS: constant(address) = 0x0000000000000000000000000000000000000000

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

name: public(String[64])
symbol: public(String[32])
decimals: public(uint256)
balances: HashMap[address, uint256]

@external
def __init__():
    self.name = "PadawanToken"
    self.symbol = "PAD"
    self.decimals = 18

@external
def mint(to: address, amount: uint256):
    self.balances[to] += amount
    log Transfer(ZERO_ADDRESS, to, amount)

@external
def burn(amount: uint256):
    self.balances[msg.sender] -= amount
    log Transfer(msg.sender, ZERO_ADDRESS, amount)

@external
def transfer(to: address, amount: uint256) -> bool:
    assert self.balances[msg.sender] >= amount
    self.balances[msg.sender] -= amount
    self.balances[to] += amount
    log Transfer(msg.sender, to, amount)
    return True 