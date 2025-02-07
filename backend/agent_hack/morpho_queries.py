LIST_CHAIN_ASSETS_QUERY = '''
query ListChainAssets($skip: Int!, $chainId: Int!) {
  assets(first: 1000, skip: $skip, where: {chainId_in: [$chainId]}) {
    pageInfo {
      countTotal
      count
      limit
      skip
    }
    items {
      id
      address
      decimals
      name
      symbol
      tags
      logoURI
      totalSupply
      priceUsd
      oraclePriceUsd
      spotPriceEth
  }
}
'''

GET_CHAIN_ASSET_QUERY = '''
query GetChainAsset($chainId: Int!, $assetSymbol: String!) {
  assets(where: {chainId_in: [$chainId], symbol_in: [$assetSymbol]}) {
    items {
      id
      address
      decimals
      name
      symbol
      tags
      logoURI
      totalSupply
      priceUsd
      oraclePriceUsd
      spotPriceEth
    }
  }
}
'''

GET_CHAIN_ASSET_BY_ADDRESS_QUERY = '''
query GetChainAssetByAddress($chainId: Int!, $assetAddress: String!) {
  assets(where: {chainId_in: [$chainId], address_in: [$assetAddress]}) {
    items {
      id
      address
      decimals
      name
      symbol
      tags
      logoURI
      totalSupply
      priceUsd
      oraclePriceUsd
      spotPriceEth
    }
  }
}
'''

LIST_CHAIN_ASSET_VAULTS_QUERY = '''
query ListChainAssetVaults($skip: Int!, $chainId: Int!, $assetAddress: String!) {
  vaults(first: 1000, skip: $skip, where: {chainId_in: [$chainId], assetAddress_in: [$assetAddress]}) {
    items {
      id
      name
      address
      symbol
      creationBlockNumber
      creationTimestamp
      creatorAddress
      whitelisted
      state {
        id
        totalAssets
        totalAssetsUsd
        lastTotalAssets
        totalSupply
        fee
        apy
        netApyWithoutRewards
        netApy
        curator
        feeRecipient
        guardian
        pendingGuardian
        pendingGuardianValidAt
        owner
        pendingOwner
        skimRecipient
        timelock
        pendingTimelock
        pendingTimelockValidAt
        timestamp
        allocation {
          id
          supplyAssets
          supplyAssetsUsd
          supplyShares
          supplyCap
          supplyCapUsd
          pendingSupplyCap
          pendingSupplyCapValidAt
          pendingSupplyCapUsd
          supplyQueueIndex
          withdrawQueueIndex
          enabled
          removableAt
          market {
            id
          }
        }
        rewards {
          yearlySupplyTokens
          supplyApr
          amountPerSuppliedToken
          asset {
            id
            address
            decimals
            name
            symbol
            tags
            logoURI
            totalSupply
            priceUsd
            oraclePriceUsd
            spotPriceEth
          }
        }
        sharePrice
        sharePriceUsd
        dailyApy
        dailyNetApy
        weeklyApy
        weeklyNetApy
        monthlyApy
        monthlyNetApy
        quarterlyApy
        quarterlyNetApy
        yearlyApy
        yearlyNetApy
        allTimeApy
        allTimeNetApy
      }
      liquidity {
        underlying
        usd
      }
      riskAnalysis {
        provider
        score
        isUnderReview
        timestamp
      }
      warnings {
        type
        level
      }
      metadata {
        description
        image
        forumLink
        curators {
          name
          image
          url
          verified
        }
      }
    }
    pageInfo {
      countTotal
      count
      limit
      skip
    }
  }
}
'''
