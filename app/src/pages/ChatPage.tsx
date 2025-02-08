import React from 'react';

import { useNavigator } from '@kibalabs/core-react';
import { Alignment, Direction, Form, IconButton, InputFrame, KibaIcon, PaddingSize, Spacing, Stack, useTheme } from '@kibalabs/ui-react';
import { useWeb3Account, useWeb3ChainId } from '@kibalabs/web3-react';
import styled from 'styled-components';

import { ChatMessage } from '../components/ChatMessage';
import { LoadingIndicator } from '../components/LoadingIndicator';
import { ChatService, Message } from '../services/ChatService';

const StyledSingleLineInput = styled.input`
  background: none;
  border: none;
  outline: none;
  cursor: text;
  overflow: hidden;
  white-space: nowrap;
  box-shadow: none;

  &:hover {
    box-shadow: none;
  }

  &:focus {
    outline: none;
  }

  &.disabled {
    pointer-events: none;
  }

  &.hideSpinButtons {
    &[type='number'] {
      -moz-appearance: textfield;
    }

    &::-webkit-outer-spin-button,
    &::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  }
`;

export function ChatPage(): React.ReactElement {
  const navigator = useNavigator();
  const chainId = useWeb3ChainId();
  const account = useWeb3Account();
  const [messages, setMessages] = React.useState<Message[]>([
    {
      date: new Date(),
      isUser: false,
      content: 'Welcome, Wallet Holder!',
    },
    {
      date: new Date(),
      isUser: false,
      content: 'I\'m here to find you the best yield possible. I\'ll do everything for you but I need to understand your needs first. Let\'s get started by understanding what you\'re looking for in your yield-seeking adventures.',
    },
  ]);
  const [inputText, setInputText] = React.useState<string>('');
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const chatService = React.useMemo(() => new ChatService(), []);

  React.useEffect((): void => {
    if (chainId !== 8453 || account == null) {
      navigator.navigateTo('/');
    }
  }, [chainId, account, navigator]);

  React.useEffect((): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const onSubmitClicked = async (): Promise<void> => {
    if (!inputText.trim() || !account) {
      return;
    }

    setIsLoading(true);
    const userMessage: Message = {
      content: inputText.trim(),
      isUser: true,
      date: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputText('');

    try {
      const response = await chatService.sendMessage(userMessage.content, account.address);
      setMessages((prevMessages) => [...prevMessages, response]);
    } catch (error) {
      console.error('Failed to get AI response:', error);
      const errorMessage: Message = {
        content: 'Sorry, something went wrong. Please try again.',
        isUser: false,
        date: new Date(),
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const theme = useTheme();

  return (
    <Stack direction={Direction.Vertical} isFullHeight={true} isFullWidth={true} maxWidth='1500px'>
      <Stack.Item growthFactor={1} shrinkFactor={1} shouldShrinkBelowContentSize={true} alignment={Alignment.Center}>
        <Stack isFullHeight={true} isFullWidth={true} isScrollableVertically={true} childAlignment={Alignment.Center}>
          <Stack direction={Direction.Vertical} shouldAddGutters={true} paddingVertical={PaddingSize.Wide} contentAlignment={Alignment.End} width='min(95%, 750px)' defaultGutter={PaddingSize.Wide}>
            {messages.map((message: Message): React.ReactElement => (
              <ChatMessage key={message.date.toISOString()} message={message} />
            ))}
            {isLoading && (
              <Stack direction={Direction.Horizontal} childAlignment={Alignment.Start} contentAlignment={Alignment.Start} paddingHorizontal={PaddingSize.Wide}>
                <LoadingIndicator />
              </Stack>
            )}
            <div ref={messagesEndRef} />
          </Stack>
        </Stack>
      </Stack.Item>
      <Form onFormSubmitted={onSubmitClicked}>
        <InputFrame
          theme={theme?.TextFrameTheme}
          inputWrapperVariant='chatInput'
          isEnabled={!isLoading}
        >
          <Stack direction={Direction.Horizontal} childAlignment={Alignment.Center} shouldAddGutters={true}>
            <Spacing variant={PaddingSize.Wide} />
            <Stack.Item growthFactor={1} shrinkFactor={1} shouldShrinkBelowContentSize={true}>
              <StyledSingleLineInput
                type='text'
                autoComplete='on'
                value={inputText}
                onChange={(event: React.ChangeEvent<HTMLInputElement>): void => setInputText(event.target.value)}
                aria-label='input'
                placeholder='Ask Yield Seeker...'
                autoFocus={true}
                spellCheck={true}
                disabled={isLoading}
              />
            </Stack.Item>
            <IconButton
              variant='primary-large'
              icon={<KibaIcon iconId='ion-send' />}
              buttonType='submit'
              isEnabled={inputText.length > 0 && !isLoading}
            />
          </Stack>
        </InputFrame>
      </Form>
    </Stack>
  );
}
