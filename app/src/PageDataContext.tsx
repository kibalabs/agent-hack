import React, { useContext, useState } from 'react';

import { IMultiAnyChildProps } from '@kibalabs/core-react';

// NOTE(krishan711): this may be better without the setData?
interface IPageData<DataType = unknown, > {
  data: DataType | null | undefined;
  setData: (data: DataType | null | undefined) => void;
}

const PageDataContext = React.createContext<IPageData | null>(null);

interface IPageDataProviderProps extends IMultiAnyChildProps {
  initialData: unknown | null | undefined;
}

export function PageDataProvider(props: IPageDataProviderProps) {
  const [data, setData] = useState<unknown | null | undefined>(props.initialData);
  return (
    // eslint-disable-next-line react/jsx-no-constructed-context-values
    <PageDataContext.Provider value={{ data, setData }}>
      {props.children}
    </PageDataContext.Provider>
  );
}

export const usePageData = <DataType, >(): IPageData<DataType> => {
  const pageDataContext = useContext(PageDataContext);
  if (!pageDataContext) {
    throw new Error('Cannot use usePageData since pageDataContext has not ben provided above in the hierarchy');
  }
  return {
    data: pageDataContext.data as DataType,
    setData: pageDataContext.setData as ((data: DataType | null | undefined) => void),
  };
};
