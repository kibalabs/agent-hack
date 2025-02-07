import React from 'react';

import { LocalStorageClient, Requester } from '@kibalabs/core';
import { IMultiAnyChildProps } from '@kibalabs/core-react';


export interface IGlobals {
  requester: Requester;
  localStorageClient: LocalStorageClient;
  sessionStorageClient: LocalStorageClient;
}

export const GlobalsContext = React.createContext<IGlobals | null>(null);

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
    throw new Error('Cannot use useGlobals since globals has not ben provided above in the hierarchy');
  }
  return globals;
};
