import React from 'react';
import { SignInButton, UserButton, useUser } from '@clerk/clerk-react';

const CustomAuth = () => {
  const { isSignedIn } = useUser();

  if (isSignedIn) {
    return <UserButton />;
  }

  return (
    <SignInButton mode="modal">
      <div
        style={{
          border: '1px solid var(--ifm-color-primary)',
          padding: '0.5rem 1rem',
          borderRadius: '0.25rem',
          color: 'var(--ifm-color-primary)',
          cursor: 'pointer',
          fontWeight: 600,
          whiteSpace: 'nowrap',
        }}
      >
        Sign In
      </div>
    </SignInButton>
  );
};

export default CustomAuth;