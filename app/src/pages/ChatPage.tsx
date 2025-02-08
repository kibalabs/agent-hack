import React from 'react';

import { useNavigator } from '@kibalabs/core-react';
import { Alignment, Direction, PaddingSize, SingleLineInput, Spacing, Stack, Text } from '@kibalabs/ui-react';
import { useWeb3Account, useWeb3ChainId } from '@kibalabs/web3-react';

import { ChatMessage } from '../components/ChatMessage';

export function ChatPage(): React.ReactElement {
  const navigator = useNavigator();
  const chainId = useWeb3ChainId();
  const account = useWeb3Account();
  const [messages, setMessages] = React.useState<Record<string, any>[]>([]);
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [input, setInput] = React.useState<string>('');
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  React.useEffect((): void => {
    if (chainId !== 8453 || account == null) {
      navigator.navigateTo('/');
    }
  }, [chainId, account, navigator]);

  React.useEffect((): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // const onMessageSubmitted = async (message: string): Promise<void> => {
  //   setIsLoading(true);
  //   // Add user message
  //   const userMessage: IChatMessage = {
  //     isUser: true,
  //     content: message,
  //   };
  //   setMessages((prevMessages) => [...prevMessages, userMessage]);

  //   // TODO: Add API call here
  //   // Simulate AI response for now
  //   setTimeout(() => {
  //     const aiMessage: IChatMessage = {
  //       isUser: false,
  //       content: 'This is a simulated AI response. The actual API integration will be added later.',
  //     };
  //     setMessages((prevMessages) => [...prevMessages, aiMessage]);
  //     setIsLoading(false);
  //   }, 1000);
  // };

  return (
    <Stack direction={Direction.Vertical} isFullHeight={true} isFullWidth={true}>
      <Stack.Item growthFactor={1} shrinkFactor={1} shouldShrinkBelowContentSize={true}>
        <Stack direction={Direction.Vertical} shouldAddGutters={false} paddingVertical={PaddingSize.Wide} contentAlignment={Alignment.End} isFullHeight={true} isFullWidth={true}>
          {messages.length > 0 ? (
            <React.Fragment>
              {messages.map((message, index) => (
                <ChatMessage message={message} />
              ))}
            </React.Fragment>
          ) : (
            <React.Fragment>
              <Stack.Item alignment={Alignment.Center}>
                <Text variant='header2'>Welcome, Wallet Holder</Text>
              </Stack.Item>
              <Spacing variant={PaddingSize.Wide3} />
              <Stack.Item alignment={Alignment.Center}>
                <ChatMessage isUser={false} content="I'm here to find you the best yield possible. I'll do everything for you but I need to understand your needs first. Let's get started by understanding what you're looking for in your yield-seeking adventures." />
              </Stack.Item>
              <Spacing variant={PaddingSize.Wide4} />
            </React.Fragment>
          )}
          <div ref={messagesEndRef} />
        </Stack>
      </Stack.Item>
      <SingleLineInput
        inputWrapperVariant='chatInput'
        isEnabled={!isLoading}
        value={input}
        onValueChanged={setInput}
        shouldAutofocus={true}
        placeholderText='Ask Yield Seeker...'
      />
    </Stack>
  );
}
