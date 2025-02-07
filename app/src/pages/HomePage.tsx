import React from 'react';

import { Alignment, Button, Direction, PaddingSize, Spacing, Stack, Text } from '@kibalabs/ui-react';
import { useOnLinkWeb3AccountsClicked, useWeb3Account, useWeb3ChainId } from '@kibalabs/web3-react';

export function HomePage(): React.ReactElement {
  const chainId = useWeb3ChainId();
  const account = useWeb3Account();
  const onLinkAccountsClicked = useOnLinkWeb3AccountsClicked();

  const onConnectWalletClicked = async () => {
    await onLinkAccountsClicked();
  };

  const onSwitchToBaseClicked = async () => {
    // @ts-expect-error
    await window.ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: `0x${parseInt('8453', 10).toString(16)}` }],
    });
  };

  return (
    <Stack direction={Direction.Vertical} childAlignment={Alignment.Center} contentAlignment={Alignment.Center} shouldAddGutters={true} isFullHeight={true} isFullWidth={true}>
      <Text variant='header1'>Yield Seeker</Text>
      <Spacing variant={PaddingSize.Wide} />
      <Text variant='bold-large'>The Best AI Agent for Maximizing Crypto Yields</Text>
      <Spacing variant={PaddingSize.Wide2} />
      {chainId == null || account == null ? (
        <Button
          variant='primary'
          text='Connect Wallet'
          onClicked={onConnectWalletClicked}
        />
      ) : chainId !== 8453 ? (
        <React.Fragment>
          <Text variant='large'>Unsupported network, only base is supported</Text>
          <Spacing />
          <Button
            variant='primary'
            text='Switch to base'
            onClicked={onSwitchToBaseClicked}
          />
        </React.Fragment>
      ) : (
        <Text variant='large'>
          Connected to
          {account.address}
        </Text>
      )}
    </Stack>
  );
}
