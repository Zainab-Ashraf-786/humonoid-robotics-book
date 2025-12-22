import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './modules.module.css';

function ModuleCard({ number, titleKey, subtitleKey, descriptionKey, link, icon }) {
  let title, subtitle, description;

  // Determine translations based on the specific keys
  if (titleKey === 'module.01.title') {
    title = <Translate id="module.01.title">The Robotic Nervous System</Translate>;
    subtitle = <Translate id="module.01.subtitle">(ROS 2 Fundamentals)</Translate>;
    description = <Translate id="module.01.description">Master nodes, topics, services, and URDF. Learn the middleware that connects robot components.</Translate>;
  } else if (titleKey === 'module.02.title') {
    title = <Translate id="module.02.title">The Digital Twin</Translate>;
    subtitle = <Translate id="module.02.subtitle">(Gazebo & Unity)</Translate>;
    description = <Translate id="module.02.description">Simulate physics, gravity, and collisions. Build virtual environments for testing.</Translate>;
  } else if (titleKey === 'module.03.title') {
    title = <Translate id="module.03.title">The AI-Robot Brain</Translate>;
    subtitle = <Translate id="module.03.subtitle">(NVIDIA Isaac™)</Translate>;
    description = <Translate id="module.03.description">Explore photorealistic simulation, VSLAM, and GPU-accelerated perception.</Translate>;
  } else if (titleKey === 'module.04.title') {
    title = <Translate id="module.04.title">Physical AI & Humanoid Robotics</Translate>;
    subtitle = <Translate id="module.04.subtitle">(Integration & Deployment)</Translate>;
    description = <Translate id="module.04.description">Combine all concepts to design complete humanoid robot systems with embodied intelligence.</Translate>;
  }

  return (
    <Link to={link} className={clsx(styles.moduleCardLink)}>
      <div className={clsx(styles.moduleCard)}>
        <div className={clsx(styles.cardHeader)}>
          <div className={clsx(styles.icon)}>{icon}</div>
          <div className={clsx(styles.moduleInfo)}>
            <span className={clsx(styles.moduleNumber)}>
              <Translate id="module">Module</Translate> {number}
            </span>
            <h3 className={clsx(styles.cardTitle)}>
              {title}
            </h3>
            <p className={clsx(styles.cardSubtitle)}>
              {subtitle}
            </p>
          </div>
        </div>
        <div className={clsx(styles.cardBody)}>
          <p className={clsx(styles.cardDescription)}>
            {description}
          </p>
        </div>
        <div className={clsx(styles.cardFooter)}>
          <span className={clsx(styles.learnMoreText)}>
            <Translate id="explore_module">Explore Module</Translate> →
          </span>
        </div>
      </div>
    </Link>
  );
}

export default function ModulesPage() {
  const { siteConfig } = useDocusaurusContext();

  const modules = [
    {
      number: '01',
      titleKey: 'module.01.title',
      subtitleKey: 'module.01.subtitle',
      descriptionKey: 'module.01.description',
      link: '/docs/ros2-fundamentals',
      icon: '🔌'
    },
    {
      number: '02',
      titleKey: 'module.02.title',
      subtitleKey: 'module.02.subtitle',
      descriptionKey: 'module.02.description',
      link: '/docs/digital-twin-sim',
      icon: '🏗️'
    },
    {
      number: '03',
      titleKey: 'module.03.title',
      subtitleKey: 'module.03.subtitle',
      descriptionKey: 'module.03.description',
      link: '/docs/isaac-ai-brain',
      icon: '🧠'
    },
    {
      number: '04',
      titleKey: 'module.04.title',
      subtitleKey: 'module.04.subtitle',
      descriptionKey: 'module.04.description',
      link: '/docs/physical-ai-hr',
      icon: '🤖'
    }
  ];

  return (
    <Layout
      title={`${translate({id: 'modules.page.title', message: 'Course Modules'})} | ${siteConfig.title}`}
      description={translate({id: 'modules.page.description', message: 'Overview of all modules in the Physical AI & Humanoid Robotics course'})}>
      <main className={styles.modulesPage}>
        <div className={styles.headerSection}>
          <Heading as="h1" className={clsx(styles.pageTitle)}>
            <Translate id="modules.page.title">Modules</Translate>
          </Heading>
          <p className={clsx(styles.pageSubtitle)}>
            <Translate id="modules.page.subtitle">A progressive learning path from ROS 2 fundamentals to advanced Physical AI integration</Translate>
          </p>
        </div>

        <div className={clsx(styles.modulesGrid)}>
          {modules.map((module, index) => (
            <ModuleCard
              key={index}
              number={module.number}
              titleKey={module.titleKey}
              subtitleKey={module.subtitleKey}
              descriptionKey={module.descriptionKey}
              link={module.link}
              icon={module.icon}
            />
          ))}
        </div>

        <div className={styles.bottomSection}>
          <div className={styles.divider}></div>
          <p className={styles.nextSteps}>
            {translate({id: 'modules.start.message', message: 'Start with Module 1 to build your foundation in ROS 2 concepts and robotics communication.'})}
            {' '}
            <Link to="/docs/ros2-fundamentals">
              {translate({id: 'modules.start.link.text', message: 'Module 1'})}
            </Link>
          </p>
        </div>
      </main>
    </Layout>
  );
}