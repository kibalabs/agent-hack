import React from 'react';

import { LocalStorageClient, Requester } from '@kibalabs/core';
import { IRoute, MockStorage, Router } from '@kibalabs/core-react';
import { Alignment, Box, ComponentDefinition, Direction, IHeadRootProviderProps, KibaApp, Stack } from '@kibalabs/ui-react';
import { buildToastThemes, Toast, ToastContainer, ToastThemedStyle, useToastManager } from '@kibalabs/ui-react-toast';
import { Web3AccountControlProvider } from '@kibalabs/web3-react';

import { MatrixBackground } from './components/MatrixBackground';
import { GlobalsProvider, IGlobals } from './GlobalsContext';
import { PageDataProvider } from './PageDataContext';
import { ChatPage } from './pages/ChatPage';
import { HomePage } from './pages/HomePage';
import { ChatService } from './services/ChatService';
import { buildHookeTheme } from './theme';

declare global {
  export interface Window {
    KRT_API_URL?: string;
  }
}

const requester = new Requester();
const baseUrl = typeof window !== 'undefined' && window.KRT_API_URL ? window.KRT_API_URL : 'https://demo-api.yieldseeker.xyz';
const chatService = new ChatService(baseUrl);
const localStorageClient = new LocalStorageClient(typeof window !== 'undefined' ? window.localStorage : new MockStorage());
const sessionStorageClient = new LocalStorageClient(typeof window !== 'undefined' ? window.sessionStorage : new MockStorage());
const theme = buildHookeTheme();

export const globals: IGlobals = {
  requester,
  localStorageClient,
  sessionStorageClient,
  chatService,
};

export const routes: IRoute<IGlobals>[] = [
  { path: '/chat', page: ChatPage },
  { path: '/', page: HomePage },
];

export interface IAppProps extends IHeadRootProviderProps {
  staticPath?: string;
  pageData?: unknown | undefined | null;
}

// @ts-expect-error
const extraComponentDefinitions: ComponentDefinition[] = [{
  component: Toast,
  themeMap: buildToastThemes(theme.colors, theme.dimensions, theme.boxes, theme.texts, theme.icons),
  themeCssFunction: ToastThemedStyle,
}];

export function App(props: IAppProps): React.ReactElement {
  const toastManager = useToastManager();

  const onWeb3AccountError = (error: Error): void => {
    toastManager.showTextToast(error.message, 'error');
  };

  return (
    <KibaApp theme={theme} isFullPageApp={true} setHead={props.setHead} extraComponentDefinitions={extraComponentDefinitions}>
      <PageDataProvider initialData={props.pageData}>
        <GlobalsProvider globals={globals}>
          {/* @ts-expect-error */}
          <Web3AccountControlProvider localStorageClient={localStorageClient} onError={onWeb3AccountError}>
            <MatrixBackground />
            <Box zIndex={1} position='absolute' isFullWidth={true} isFullHeight={true}>
              <Stack direction={Direction.Vertical} isFullWidth={true} isFullHeight={true} contentAlignment={Alignment.Start} childAlignment={Alignment.Center}>
                <Router staticPath={props.staticPath} routes={routes} />
                <ToastContainer />
              </Stack>
            </Box>
          </Web3AccountControlProvider>
        </GlobalsProvider>
      </PageDataProvider>
    </KibaApp>
  );
}
