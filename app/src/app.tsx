import React from 'react';

import { LocalStorageClient, Requester } from '@kibalabs/core';
import { IRoute, MockStorage, Router } from '@kibalabs/core-react';
import { Alignment, Direction, Head, IHeadRootProviderProps, KibaApp, Stack } from '@kibalabs/ui-react';

import { GlobalsProvider, IGlobals } from './GlobalsContext';
import { PageDataProvider } from './PageDataContext';
import { HomePage } from './pages/HomePage';
import { buildHookeTheme } from './theme';


declare global {
  export interface Window {
    KRT_API_URL?: string;
  }
}

const requester = new Requester();
// const baseUrl = typeof window !== 'undefined' && window.KRT_API_URL ? window.KRT_API_URL : 'https://api.yieldseeker.xyz';
const localStorageClient = new LocalStorageClient(typeof window !== 'undefined' ? window.localStorage : new MockStorage());
const sessionStorageClient = new LocalStorageClient(typeof window !== 'undefined' ? window.sessionStorage : new MockStorage());
const theme = buildHookeTheme();

export const globals: IGlobals = {
  requester,
  localStorageClient,
  sessionStorageClient,
};

export const routes: IRoute<IGlobals>[] = [
  { path: '/', page: HomePage },
];

export interface IAppProps extends IHeadRootProviderProps {
  staticPath?: string;
  pageData?: unknown | undefined | null;
}

export function App(props: IAppProps): React.ReactElement {
  return (
    <KibaApp theme={theme} isFullPageApp={true} setHead={props.setHead}>
      <PageDataProvider initialData={props.pageData}>
        <GlobalsProvider globals={globals}>
          <Head headId='app'>
            <title>Yield Seeker</title>
          </Head>
          <Stack direction={Direction.Vertical} isFullWidth={true} contentAlignment={Alignment.Start}>
            <Router staticPath={props.staticPath} routes={routes} />
            {/* <ToastContainer /> */}
          </Stack>
        </GlobalsProvider>
      </PageDataProvider>
    </KibaApp>
  );
}
