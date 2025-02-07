import React from 'react';

import { Alignment, Box, Direction, Stack, Text } from '@kibalabs/ui-react';

export function HomePage(): React.ReactElement {
  return (
    <Box width='100%'>
      <Stack direction={Direction.Vertical} childAlignment={Alignment.Center} contentAlignment={Alignment.Center} shouldAddGutters={true} isFullHeight={true}>
        <Text variant='header1'>Welcome to Yield Seeker</Text>
      </Stack>
    </Box>
  );
}
