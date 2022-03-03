# SNS - Starknet Name Service
A reckless attempt at prototyping Starknet Name Service, so that we have an onchain registery for address-name lookup, where name is a short string literal. This helps with any scoreboarding UI, including the one at [0xstrat v1](https://github.com/topology-gg/fountain/tree/v0.1/examples/zeroxstrat_v1)

### where and how to use it
- Currently deployed on StarkNet testnet at: https://goerli.voyager.online/contract/0x02ef8e28b8d7fc96349c76a0607def71c678975dbd60508b9c343458c4758fac#writeContract
- Function for address-name lookup: `sns_lookup (adr : felt) -> (exist : felt, name : felt)`

### use cases
- `sns_lookup_adr_to_name()`: for any application that maintains scoreboards for addresses, mapping addresses to legible names is desirable
- `sns_lookup_name_to_adr()`: for accessing public goods smart contracts already deployed on StarkNet by legible names instead of raw hex address

### improvements to be made
- may integrate with string library to attach arbitrarily long strings to the short string literal `name` 
