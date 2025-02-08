import React from 'react';

import styled, { keyframes } from 'styled-components';

const fallAnimation = keyframes`
  0% {
    transform: translateY(-100%);
    opacity: 0;
  }
  50% {
    opacity: 0.15;
  }
  100% {
    transform: translateY(100vh);
    opacity: 0;
  }
`;

const Container = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: transparent;
  z-index: 0;
  overflow: hidden;
`;

const Column = styled.div<{ delay: number; duration: number; left: number }>`
  position: absolute;
  top: 0;
  left: ${(props) => props.left}%;
  color: rgba(0, 255, 0, 1);
  font-family: monospace;
  font-size: 1.2em;
  line-height: 1.5em;
  white-space: pre;
  transform-origin: 50% 50%;
  text-shadow: 0 0 8px rgba(0, 255, 0, 0.3);
  opacity: 0;
  animation: ${fallAnimation} ${(props) => props.duration}s linear infinite;
  animation-delay: ${(props) => props.delay}s;
`;

const symbols = [
  'Ξ',
  '₿',
  '$',
  '%',
  '↑',
  '↗',
  '→',
];

const generateRandomString = (length: number): string => {
  let result = '';
  for (let i = 0; i < length; i += 1) {
    // 70% chance to add a space, 30% chance to add a symbol
    if (Math.random() < 0.7) {
      result += '  \n';
    } else {
      const symbol = symbols[Math.floor(Math.random() * symbols.length)];
      result += `${symbol}\n`;
    }
  }
  return result;
};

export function MatrixBackground(): React.ReactElement {
  const columnCount = 50;
  const columns = Array(columnCount)
    .fill(0)
    .map((_, index) => ({
      chars: generateRandomString(20),
      delay: Math.random() * 2,
      duration: 15 + Math.random() * 20,
      left: (index * 100) / columnCount,
    }));

  return (
    <Container>
      {columns.map((column) => (
        <Column
          key={column.chars}
          delay={column.delay}
          duration={column.duration}
          left={column.left}
        >
          {column.chars}
        </Column>
      ))}
    </Container>
  );
}
