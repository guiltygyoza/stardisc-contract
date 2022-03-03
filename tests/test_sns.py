import pytest
import os
import random
import math
from starkware.starknet.testing.starknet import Starknet
import asyncio
from Signer import Signer
from binascii import hexlify, unhexlify

NUM_SIGNING_ACCOUNTS = 5
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

    names = ['tom', 'kate', 'mahir', 'priya']
    N = 2
    print(f'> Begin registering {N} pairs of (adr,name)')
    for user,name in zip(users[0:N], names[0:N]):
        await user['signer'].send_transaction(
            account=user['account'],
            to=contract.contract_address,
            selector_name='sns_register',
            calldata=[ ascii_to_felt(name) ]
        )

    print(f'> Begin lookup adr->name')
    for i,user in enumerate(users):
        ret = await contract.sns_lookup_adr_to_name (user['account'].contract_address).call()

        if i<N:
            assert ret.result.exist == 1
        else:
            assert ret.result.exist == 0

        if ret.result.exist == 1:
            name = felt_to_ascii (ret.result.name)
            print(f'exist: 1 / recovered name: {name}')
        else:
            print(f'exist: {ret.result.exist}')
    print()

    print(f'> Begin lookup name->adr')
    for i,name in enumerate(names):
        name_in_felt = ascii_to_felt (name)
        ret = await contract.sns_lookup_name_to_adr (name_in_felt).call()

        if i<N:
            assert ret.result.exist == 1
        else:
            assert ret.result.exist == 0

        if ret.result.exist == 1:
            print(f'exist: 1 / recovered adr: {hex(ret.result.adr)}')
        else:
            print(f'exist: {ret.result.exist}')
    print()

    print(f'> Begin intentional registering with name collision')
    user_malicious = users[NUM_SIGNING_ACCOUNTS-1]
    with pytest.raises(Exception) as e_info:
        for i in range(N):
            await user_malicious['signer'].send_transaction(
                account=user_malicious['account'],
                to=contract.contract_address,
                selector_name='sns_register',
                calldata=[ ascii_to_felt(names[i]) ]
            )

def felt_to_ascii (felt):
    bytes_object = bytes.fromhex( hex(felt)[2:] )
    return unhexlify(bytes_object).decode("ASCII")

def ascii_to_felt (str):
    return int( hexlify(str.encode()).hex(), 16 )
