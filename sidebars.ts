import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    'glossary',
    'course-overview',
    {
      type: 'link',
      label: 'Course Modules',
      href: '/modules',
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'ros2-fundamentals/index',
        'ros2-fundamentals/nodes-topics-services',
        'ros2-fundamentals/python-integration',
        'ros2-fundamentals/urdf',
        'ros2-fundamentals/conclusion',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'digital-twin-sim/index',
        'digital-twin-sim/physics-fundamentals',
        'digital-twin-sim/gazebo-simulation',
        'digital-twin-sim/unity-rendering',
        'digital-twin-sim/sensor-simulation',
        'digital-twin-sim/conclusion',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'isaac-ai-brain/index',
        'isaac-ai-brain/isaac-sim',
        'isaac-ai-brain/isaac-ros',
        'isaac-ai-brain/perception',
        'isaac-ai-brain/navigation',
        'isaac-ai-brain/conclusion',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Physical AI & Humanoid Robotics (Capstone)',
      items: [
        'physical-ai-hr/index',
        'physical-ai-hr/chapter-1-physical-ai',
        'physical-ai-hr/chapter-2-llm-planning',
        'physical-ai-hr/chapter-3-sim2real',
        'physical-ai-hr/chapter-4-complete-system',
        'physical-ai-hr/chapter-5-vla-integration',
        'physical-ai-hr/vlm-technical-reference',
        'physical-ai-hr/conclusion',
      ],
    },
  ],
};

export default sidebars;