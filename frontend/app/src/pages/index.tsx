import { useStarknet, useStarknetCall } from '@starknet-react/core'
import type { NextPage } from 'next'
import { ConnectWallet } from '~/components/ConnectWallet'
import { IncrementCounter } from '~/components/IncrementCounter'
import { TransactionList } from '~/components/TransactionList'
import { useCounterContract } from '~/hooks/counter'
import { useSNSContract } from '~/hooks/sns'

import { ShowNameLookup } from '~/components/ShowNameLookup'

const Home: NextPage = () => {
  const { contract: counter } = useCounterContract()
  const { data: counterValue } = useStarknetCall({ contract: counter, method: 'counter', args: {} })

  const { contract: sns } = useSNSContract()

  return (
    <div>
      <h2>Wallet</h2>
      <ConnectWallet />
      <h2>Starknet Name Service</h2>
      <p>Address (testnet): {sns?.connectedTo}</p>

      <ShowNameLookup />

    </div>
  )
}

export default Home
