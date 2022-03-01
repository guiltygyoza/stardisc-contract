import { useContract } from '@starknet-react/core'
import { Abi } from 'starknet'

import SNSAbi from '~/abi/sns_abi.json'

export function useSNSContract() {
  return useContract({
    abi: SNSAbi.abi as Abi[],
    address: '0x00b14b453b3bf720812269d58a709b610a079289becfd53ddb00ff579101a04a',
  })
}
