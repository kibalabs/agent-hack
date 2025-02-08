import React from 'react';

import { Direction, Stack } from '@kibalabs/ui-react';
import styled, { keyframes } from 'styled-components';

const bounce = keyframes`
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1.0);
  }
`;

const Dot = styled.div`
  width: 8px;
  height: 8px;
  background-color: rgb(39, 236, 111);
  border-radius: 0;
  display: inline-block;
  margin: 0 3px;
  animation: ${bounce} 1.4s infinite ease-in-out both;

  &:nth-child(1) {
    animation-delay: -0.32s;
  }

  &:nth-child(2) {
    animation-delay: -0.16s;
  }
`;

export function LoadingIndicator(): React.ReactElement {
  return (
    <Stack direction={Direction.Horizontal} shouldAddGutters={true}>
      <Dot />
      <Dot />
      <Dot />
    </Stack>
  );
}
