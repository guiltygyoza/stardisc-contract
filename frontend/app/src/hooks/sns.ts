import { useContract } from '@starknet-react/core'
import { Abi } from 'starknet'

import SNSAbi from '~/abi/sns_abi.json'

export function useSNSContract() {
  return useContract({
    abi: SNSAbi.abi as Abi[],
    address: '0x079e0f3d15e10b15223d2aa9843bd2f6ea9d21408caa2592a2e9a6bfc33820ac',
  })
}
