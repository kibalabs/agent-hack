import React from 'react';

import { LocalStorageClient, Requester } from '@kibalabs/core';
import { IMultiAnyChildProps } from '@kibalabs/core-react';

import { ChatService } from './services/ChatService';

export interface IGlobals {
  localStorageClient: LocalStorageClient;
  requester: Requester;
  chatService: ChatService;
  sessionStorageClient: LocalStorageClient;
}

const GlobalsContext = React.createContext<IGlobals | null>(null);

interface GlobalsProviderProps extends IMultiAnyChildProps {
  globals: IGlobals;
}

export function GlobalsProvider(props: GlobalsProviderProps): React.ReactElement {
  return (
    <GlobalsContext.Provider value={props.globals}>
      {props.children}
    </GlobalsContext.Provider>
  );
}

export const useGlobals = (): IGlobals => {
  const globals = React.useContext(GlobalsContext);
  if (!globals) {
    throw new Error('Cannot use globals context without a provider');
  }
  return globals;
};
