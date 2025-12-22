import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate from '@docusaurus/Translate';

import styles from './index.module.css';

function HomepageHeader() {
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <Heading as="h1" className={clsx('hero__title', styles.heroTitle)}>
            <Translate id="hero.title" description="Hero section title">
              Physical AI & Humanoid Robotics
            </Translate>
          </Heading>
          <p className={clsx('hero__subtitle', styles.heroSubtitle)}>
            <Translate id="hero.subtitle" description="Hero section subtitle">
              Comprehensive course from ROS 2 fundamentals to advanced humanoid AI integration
            </Translate>
          </p>
          <div className={styles.buttons}>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro">
              <Translate id="hero.button.start_learning" description="Hero section start learning button text">
                Start Learning
              </Translate>
            </Link>
            <Link
              className="button button--secondary button--lg"
              to="/docs/course-overview">
              <Translate id="hero.button.view_modules" description="Hero section view modules button text">
                View Modules
              </Translate>
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {i18n} = useDocusaurusContext();
  const currentLocale = i18n.currentLocale;
  let pageTitle = 'Physical AI & Humanoid Robotics';

  if (currentLocale === 'ur') {
    pageTitle = 'فزیکل ای آئی اور ہیومنوڈ روبوٹکس';
  }

  return (
    <Layout
      title={pageTitle}
      description="Comprehensive course on Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container padding-vert--lg">
            <div className="row">
              <div className="col col--4 padding-horiz--md">
                <div className={clsx(styles.featureCard)}>
                  <h3 className={styles.featureTitle}>
                    <Translate id="feature.physical_ai_principles.title" description="Physical AI Principles feature title">
                      Physical AI Principles
                    </Translate>
                  </h3>
                  <p className={styles.featureDescription}>
                    <Translate id="feature.physical_ai_principles.description" description="Physical AI Principles feature description">
                      Understand how intelligence emerges from the intimate coupling between agent, body, and environment in embodied systems.
                    </Translate>
                  </p>
                </div>
              </div>
              <div className="col col--4 padding-horiz--md">
                <div className={clsx(styles.featureCard)}>
                  <h3 className={styles.featureTitle}>
                    <Translate id="feature.simulation_environments.title" description="Simulation Environments feature title">
                      Simulation Environments
                    </Translate>
                  </h3>
                  <p className={styles.featureDescription}>
                    <Translate id="feature.simulation_environments.description" description="Simulation Environments feature description">
                      Master physics-based simulation using Gazebo and photorealistic rendering with Unity for comprehensive robot testing.
                    </Translate>
                  </p>
                </div>
              </div>
              <div className="col col--4 padding-horiz--md">
                <div className={clsx(styles.featureCard)}>
                  <h3 className={styles.featureTitle}>
                    <Translate id="feature.ai_integration.title" description="AI Integration feature title">
                      AI Integration
                    </Translate>
                  </h3>
                  <p className={styles.featureDescription}>
                    <Translate id="feature.ai_integration.description" description="AI Integration feature description">
                      Leverage NVIDIA Isaac for GPU-accelerated perception, navigation, and cognitive planning in robotic systems.
                    </Translate>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}