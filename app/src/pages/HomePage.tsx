import React from 'react';

import { useNavigator } from '@kibalabs/core-react';
import { Alignment, Button, Direction, PaddingSize, Spacing, Stack, Text } from '@kibalabs/ui-react';
import { useOnLinkWeb3AccountsClicked, useWeb3Account, useWeb3ChainId, useWeb3LoginSignature, useWeb3OnLoginClicked } from '@kibalabs/web3-react';

export function HomePage(): React.ReactElement {
  const navigator = useNavigator();
  const chainId = useWeb3ChainId();
  const account = useWeb3Account();
  const onLinkAccountsClicked = useOnLinkWeb3AccountsClicked();
  const onAccountLoginClicked = useWeb3OnLoginClicked();
  const loginSignature = useWeb3LoginSignature();
  const [isLoggingIn, setIsLoggingIn] = React.useState<boolean>(false);

  React.useEffect((): void => {
    if (chainId === 8453 && account && loginSignature) {
      navigator.navigateTo('/chat');
    }
  }, [chainId, account, navigator, loginSignature]);

  const onConnectWalletClicked = async () => {
    await onLinkAccountsClicked();
  };

  const onLoginClicked = async (): Promise<void> => {
    setIsLoggingIn(true);
    await onAccountLoginClicked();
    setIsLoggingIn(false);
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
      <Spacing variant={PaddingSize.Wide3} />
      {chainId == null || account == null ? (
        <Button
          variant='tertiary-large'
          text='Connect Wallet'
          onClicked={onConnectWalletClicked}
        />
      ) : chainId !== 8453 ? (
        <React.Fragment>
          <Text variant='large'>Unsupported network, only base is supported</Text>
          <Spacing />
          <Button
            variant='tertiary-large'
            text='Switch to base'
            onClicked={onSwitchToBaseClicked}
          />
        </React.Fragment>
      ) : isLoggingIn ? (
        <Text>Please check your wallet to sign the login message</Text>
      ) : !loginSignature ? (
        <Button variant='primary-large' text='Log in' onClicked={onLoginClicked} isLoading={isLoggingIn} />
      ) : (
        <Text variant='large'>{`Connected to ${account.address}`}</Text>
      )}
    </Stack>
  );
}
