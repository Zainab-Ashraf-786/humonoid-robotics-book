import React from 'react';
import { useUser, UserButton } from '@clerk/clerk-react';
import { useHistory } from '@docusaurus/router';

export default function Auth() {
  const { isSignedIn } = useUser();
  const history = useHistory();

  if (isSignedIn) {
    return <UserButton afterSignOutUrl="/" />;
  }

  return (
    <button
      onClick={() => history.push('/sign-in')}
      style={{
        background: 'none',
        border: 'none',
        color: 'var(--ifm-navbar-link-color)',
        cursor: 'pointer',
        fontSize: '1rem',
      }}
    >
      Sign In
    </button>
  );
}
