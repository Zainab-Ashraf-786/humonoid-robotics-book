import React from 'react';
import { ClerkProvider } from '@clerk/clerk-react';
import { useHistory } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import ChatbotWidget from '../components/ChatbotWidget/ChatbotWidget';

export default function Root({ children }) {
  const { siteConfig } = useDocusaurusContext();
  const { clerkPublishableKey } = siteConfig.customFields;
  const history = useHistory();
  const navigate = (to) => history.push(to);

  return (
    <ClerkProvider
      publishableKey={clerkPublishableKey as string}
      navigate={navigate}
    >
      {children}
      <ChatbotWidget />
    </ClerkProvider>
  );
}
