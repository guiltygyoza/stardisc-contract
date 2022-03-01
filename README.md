# SNS - Starknet Name Service
A reckless attempt at prototyping Starknet Name Service, so that we have an onchain registery for address-name lookup, where name is a short string literal. This helps with any scoreboarding UI, including the one at [0xstrat v1](https://github.com/topology-gg/fountain/tree/v0.1/examples/zeroxstrat_v1)

### where and how to use it
- Currently deployed on StarkNet testnet at: 0x079e0f3d15e10b15223d2aa9843bd2f6ea9d21408caa2592a2e9a6bfc33820ac
- Function for address-name lookup: `sns_lookup (adr) -> (exist, name)`
