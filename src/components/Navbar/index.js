import React from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function Navbar() {
  return (
    <nav className="navbar navbar--primary">
      <div className="navbar__inner">
        <div className="navbar__items">
          <Link className="navbar__brand" to={useBaseUrl('/')}>
            <b>Physical AI & Robotics</b>
          </Link>
          <Link className="navbar__item navbar__link" to="/docs/intro">
            Course
          </Link>
          <Link className="navbar__item navbar__link" to="/modules">
            Modules
          </Link>
        </div>

        <div className="navbar__items navbar__items--right">
          <Link
            className="navbar__item navbar__link"
            href="https://github.com/humonoid-robotics-book/physical-ai-humanoid-robotics"
          >
            GitHub
          </Link>
        </div>
      </div>
    </nav>
  );
}