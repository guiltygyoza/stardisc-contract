import { useStarknet, useStarknetCall } from '@starknet-react/core'
import React from 'react'
import { useSNSContract } from '~/hooks/sns'

export function ShowNameLookup() {
  const { account } = useStarknet()
  const { contract: sns } = useSNSContract()
  const { data: valueSnsLookup } = useStarknetCall ({ contract: sns, method: 'sns_lookup_adr_to_name', args: { adr:'0' } })

  if (!account) {
    return null
  }

  return (
    <div>
      <p>your address exist?: {valueSnsLookup?.exist}</p>
      <p>your name if exist: {valueSnsLookup?.name}</p>
    </div>
  )

}
