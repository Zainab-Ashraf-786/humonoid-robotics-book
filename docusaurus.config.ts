import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Comprehensive course from ROS 2 fundamentals to advanced humanoid AI integration',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://your-docusaurus-site.example.com',
  baseUrl: '/',

  organizationName: 'humonoid-robotics-book',
  projectName: 'physical-ai-humanoid-robotics',

  onBrokenLinks: 'throw',
  customFields: {
    clerkPublishableKey: 'pk_test_cGxlYXNlZC1yYWNjb29uLTIxLmNsZXJrLmFjY291bnRzLmRldiQ',
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/ZainabFullStackLearner/humonoid-robotics-book/edit/main/',
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],
  
  i18n: {
    defaultLocale: 'en',
    locales: ['en','ur'],// Only English for now, add 'ur' when translations are ready
    localeConfigs: {
      en: {
        label: 'English',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
      },
    },
  },

  themes: ['@docusaurus/theme-live-codeblock'],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Physical AI & Robotics',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: '/docs/intro',
          label: 'Course',
          position: 'left',
        },
        {
          to: '/modules',
          label: 'Modules',
          position: 'left',
        },
        {
          href: 'https://github.com/ZainabFullStackLearner/humonoid-robotics-book',
          label: 'GitHub',
          position: 'right',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          type: 'custom-auth',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Course',
          items: [
            {
              label: 'Overview',
              to: '/docs/intro',
            },
            {
              label: 'Module 1',
              to: '/docs/ros2-fundamentals',
            },
            {
              label: 'Module 2',
              to: '/docs/digital-twin-sim',
            },
            {
              label: 'Module 3',
              to: '/docs/isaac-ai-brain',
            },
            {
              label: 'Module 4',
              to: '/docs/physical-ai-hr',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS Documentation',
              href: 'https://docs.ros.org/',
            },
            {
              label: 'NVIDIA Isaac',
              href: 'https://developer.nvidia.com/isaac',
            },
            {
              label: 'Gazebo Simulation',
              href: 'https://gazebosim.org/',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/ZainabFullStackLearner/humonoid-robotics-book',
            },
          ],
        },
      ],
      copyright: `<div style="font-size: 0.85rem;">Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Course. Built with Docusaurus.</div>`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;