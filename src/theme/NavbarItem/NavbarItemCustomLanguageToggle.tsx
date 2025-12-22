import React from 'react';
import clsx from 'clsx';
import LanguageToggle from '../../theme/LanguageToggle';

export default function NavbarItemCustomLanguageToggle(props) {
  return (
    <div className={clsx('navbar__item', props.className)}>
      <LanguageToggle />
    </div>
  );
}