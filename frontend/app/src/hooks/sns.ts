import { useContract } from '@starknet-react/core'
import { Abi } from 'starknet'

import SNSAbi from '~/abi/sns_abi.json'

export function useSNSContract() {
  return useContract({
    abi: SNSAbi.abi as Abi[],
    address: '0x02ef8e28b8d7fc96349c76a0607def71c678975dbd60508b9c343458c4758fac',
  })
}
