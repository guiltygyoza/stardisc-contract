import pytest
import os
import random
import math
from starkware.starknet.testing.starknet import Starknet
import asyncio
from Signer import Signer
from binascii import hexlify, unhexlify


NUM_SIGNING_ACCOUNTS = 3
DUMMY_PRIVATE = 49582320498
users = []

### Reference: https://github.com/perama-v/GoL2/blob/main/tests/test_GoL2_infinite.py

@pytest.fixture(scope='module')
def event_loop():
    return asyncio.new_event_loop()

@pytest.fixture(scope='module')
async def account_factory():
    starknet = await Starknet.empty()
    print()

    accounts = []
    print(f'> Deploying {NUM_SIGNING_ACCOUNTS} accounts...')
    for i in range(NUM_SIGNING_ACCOUNTS):
        signer = Signer(DUMMY_PRIVATE + i)
        account = await starknet.deploy(
            "contracts/Account.cairo",
            constructor_calldata=[signer.public_key]
        )
        await account.initialize(account.contract_address).invoke()
        users.append({
            'signer' : signer,
            'account' : account
        })

        print(f'  Account {i} is: {hex(account.contract_address)}')
    print()

    return starknet, accounts

@pytest.mark.asyncio
async def test_sns (account_factory):

    starknet, accounts = account_factory
    contract = await starknet.deploy('contracts/sns.cairo')
    print()

    names = ['tom', 'kate', 'mahir']
    for user,name in zip(users[0:2], names[0:2]):
        await user['signer'].send_transaction(
            account=user['account'],
            to=contract.contract_address,
            selector_name='sns_register',
            calldata=[ ascii_to_felt(name) ]
        )

    for user in users:
        ret = await contract.sns_lookup(user['account'].contract_address).call()
        if ret.result.exist == 1:
            name = felt_to_ascii (ret.result.name)
            print(f'exist: 1 / recovered name: {name}')
        else:
            print(f'exist: {ret.result.exist}')

def felt_to_ascii (felt):
    bytes_object = bytes.fromhex( hex(felt)[2:] )
    return unhexlify(bytes_object).decode("ASCII")

def ascii_to_felt (str):
    return int( hexlify(str.encode()).hex(), 16 )
