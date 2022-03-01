# SNS - Starknet Name Service
A reckless attempt at prototyping Starknet Name Service, so that we have an onchain registery for address-name lookup, where name is a short string literal. This helps with any scoreboarding UI, including the one at [0xstrat v1](https://github.com/topology-gg/fountain/tree/v0.1/examples/zeroxstrat_v1)

### where and how to use it
- Currently deployed on StarkNet testnet at: 0x00b14b453b3bf720812269d58a709b610a079289becfd53ddb00ff579101a04a
- Function for address-name lookup: `sns_lookup (adr : felt) -> (exist : felt, name : felt)`

### use cases
- for any application that maintains scoreboards for addresses, mapping addresses to legible names is desirable
- for accessing public goods smart contracts already deployed on StarkNet by legible names, not raw hex address

### improvements to be made
- use sparse merkle tree to tackle scalability
- may integrate with string library to attach arbitrarily long strings to the short string literal `name` 
