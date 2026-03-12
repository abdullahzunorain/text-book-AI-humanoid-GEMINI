import React, { useState } from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chat from '@site/src/components/Chat';
import AuthModal from '@site/src/components/AuthModal';
import { useAuth } from '@site/src/hooks/useAuth';
import type LayoutType from '@theme/Layout';

export default function Layout(props: React.ComponentProps<typeof LayoutType>) {
  const { user, token, isAuthenticated, signUp, signIn, signOut } = useAuth();
  const [showAuth, setShowAuth] = useState(false);

  return (
    <>
      <div style={{
        position: 'fixed',
        top: 8,
        right: 16,
        zIndex: 999,
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
      }}>
        {isAuthenticated ? (
          <>
            <span style={{ fontSize: '0.85rem', color: 'var(--ifm-color-emphasis-700)' }}>
              {user?.name}
            </span>
            <button
              onClick={signOut}
              className="button button--outline button--sm"
              style={{ fontSize: '0.8rem' }}
            >
              Sign Out
            </button>
          </>
        ) : (
          <button
            onClick={() => setShowAuth(true)}
            className="button button--primary button--sm"
            style={{ fontSize: '0.8rem' }}
          >
            Sign In
          </button>
        )}
      </div>

      <OriginalLayout {...props} />

      <Chat authToken={token} />

      <AuthModal
        isOpen={showAuth}
        onClose={() => setShowAuth(false)}
        onSignUp={signUp}
        onSignIn={signIn}
      />
    </>
  );
}
