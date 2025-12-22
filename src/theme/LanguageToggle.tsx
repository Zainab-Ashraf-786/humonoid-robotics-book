import React from "react";
import { useLocation } from "@docusaurus/router";
import { translate } from "@docusaurus/Translate";

export default function LanguageToggle() {
  const location = useLocation();

  // Determine current language from URL or default to 'en'
  const isUrdu = location.pathname.startsWith('/ur/');

  // Function to toggle language
  const toggleLang = () => {
    if (isUrdu) {
      // Switch to English
      window.location.pathname = location.pathname.replace(/^\/ur\//, '/') || '/';
    } else {
      // Switch to Urdu
      window.location.pathname = `/ur${location.pathname}`;
    }
  };

  return (
    <button
      className="navbar__link langToggleBtn"
      onClick={toggleLang}
      aria-label={translate({
        id: 'theme.navbar.langToggle.ariaLabel',
        message: `Switch language to ${isUrdu ? 'English' : 'Urdu'}`
      })}
      title={translate({
        id: 'theme.navbar.langToggle.title',
        message: `Switch language to ${isUrdu ? 'English' : 'Urdu'}`
      })}
    >
      {isUrdu ? 'EN' : 'اردو'}
    </button>
  );
}