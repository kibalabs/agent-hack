import React from 'react';

import { Box, ColorSettingView, getVariant, Markdown, useColors } from '@kibalabs/ui-react';

import { Message } from '../services/ChatService';


export interface IChatMessageProps {
  className?: string;
  message: Message;
}

export function ChatMessage(props: IChatMessageProps): React.ReactElement {
  const colors = useColors();
  return (
    <Box className={props.className} variant={getVariant('chatMessage', props.message.isUser ? 'chatMessageUser' : 'chatMessageBot')} width={props.message.isUser ? '80%' : '100%'}>
      <ColorSettingView theme={{ text: props.message.isUser ? colors.text : colors.brandPrimary }}>
        <Markdown source={props.message.content} />
      </ColorSettingView>
    </Box>
  );
}
