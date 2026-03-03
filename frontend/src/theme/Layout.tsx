import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chat from '@site/src/components/Chat';
import type LayoutType from '@theme/Layout';

/**
 * Custom Layout wrapper that includes the AI Chat component.
 * This wraps the default Docusaurus Layout to add chat functionality.
 */
export default function Layout(props: React.ComponentProps<typeof LayoutType>) {
  return (
    <>
      <OriginalLayout {...props} />
      <Chat 
        apiUrl="http://localhost:8000" 
        userId={1} 
      />
    </>
  );
}
