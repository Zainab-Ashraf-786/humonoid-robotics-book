import React, { useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import { translate } from '@docusaurus/Translate';

const LanguageToggle: React.FC = () => {
  const location = useLocation();
  const [currentLang, setCurrentLang] = useState('en');
  const [isRTL, setIsRTL] = useState(false);

  useEffect(() => {
    // Determine current language from URL or default to 'en'
    const langFromUrl = location.pathname.split('/')[1] || 'en';
    const isCurrentRTL = langFromUrl === 'ur';

    setCurrentLang(langFromUrl);
    setIsRTL(isCurrentRTL);

    // Update document direction based on language
    document.documentElement.dir = isCurrentRTL ? 'rtl' : 'ltr';
  }, [location.pathname]);

  const switchLanguage = (lang: string) => {
    // Get current path without the language prefix
    const pathParts = location.pathname.split('/');
    const currentLangInPath = pathParts[1];

    let newPath: string;
    if (['en', 'ur'].includes(currentLangInPath)) {
      // If current path already includes a language, replace it
      pathParts[1] = lang;
      newPath = pathParts.join('/');
    } else {
      // If no language in path, add the new language
      newPath = `/${lang}${location.pathname}`;
    }

    window.location.href = `${newPath}${location.search}${location.hash}`;
  };

  return (
    <div className="language-toggle" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <button
        onClick={() => switchLanguage('en')}
        className={`button button--sm ${currentLang === 'en' ? 'button--primary' : 'button--secondary'}`}
        style={{
          minWidth: '60px',
          direction: 'ltr' // Keep button text LTR even in RTL context
        }}
        aria-label="Switch to English"
      >
        EN
      </button>
      <span style={{ opacity: 0.7 }}>|</span>
      <button
        onClick={() => switchLanguage('ur')}
        className={`button button--sm ${currentLang === 'ur' ? 'button--primary' : 'button--secondary'}`}
        style={{
          minWidth: '60px',
          direction: 'rtl' // Keep button text LTR even in RTL context
        }}
        aria-label="اردو میں تبدیل کریں"
      >
        اردو
      </button>
    </div>
  );
};

export default LanguageToggle;