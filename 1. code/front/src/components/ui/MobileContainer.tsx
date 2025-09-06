import { ReactNode } from 'react';

interface MobileContainerProps {
  children: ReactNode;
}

export const MobileContainer = ({ children }: MobileContainerProps) => {
  return <div className="w-full min-h-screen flex flex-col">{children}</div>;
};
