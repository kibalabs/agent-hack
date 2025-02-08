import React from 'react';

import { getVariant, Text } from '@kibalabs/ui-react';


export interface IChatMessage {
  date: Date;
  isUser: boolean;
  content: string;
  // isPlaceholder: boolean;
}

export interface IChatMessageProps {
  className?: string;
  message: IChatMessage;
}

export function ChatMessage(props: IChatMessageProps): React.ReactElement {
  return (
    <div className={props.className} style={{ backgroundColor: props.message.isUser ? 'var(--color-background-light10)' : 'transparent', padding: '1em 1.5em', width: props.message.isUser ? '80%' : '100%', alignSelf: props.message.isUser ? 'flex-end' : 'flex-start', borderRadius: props.message.isUser ? '0.99em 0.99em 0 0.99em' : '0.5em' }}>
      <Text variant={getVariant(props.message.isUser ? 'default' : 'branded')}>{props.message.content}</Text>
    </div>
  );
}
