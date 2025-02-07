import React from 'react';

import { Alignment, Direction, Stack, Text } from '@kibalabs/ui-react';


export interface IChatMessageProps {
  className?: string;
  isUser: boolean;
  content: string;
}

export function ChatMessage(props: IChatMessageProps): React.ReactElement {
  return (
    <Stack className={props.className} width='80%' direction={Direction.Horizontal} childAlignment={Alignment.Start} contentAlignment={props.isUser ? Alignment.End : Alignment.Start}>
      <Stack.Item className='message' growthFactor={1} shrinkFactor={1} shouldShrinkBelowContentSize={true}>
        <Text>{props.content}</Text>
      </Stack.Item>
    </Stack>
  );
}
