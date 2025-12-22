# Quickstart Guide: Physical AI & Humanoid Robotics Book Repository

## Repository Overview

This repository contains a modular textbook on Physical AI and Humanoid Robotics, structured as a GitHub-style documentation project. The content is organized into 4 modules with multiple pages each, designed to be read both on GitHub and as a deployed Docusaurus website.

## Repository Structure

```
physical-ai-and-humanoid-robotics/
├── docs/
│   ├── physical-ai-fundamentals/
│   │   ├── index.md
│   │   ├── principles.md
│   │   ├── applications.md
│   │   └── approaches.md
│   ├── ros2-integration/
│   │   ├── index.md
│   │   ├── basics.md
│   │   ├── packages.md
│   │   └── simulation.md
│   ├── simulation-environments/
│   │   ├── index.md
│   │   ├── gazebo.md
│   │   ├── unity.md
│   │   ├── comparison.md
│   │   └── advanced.md
│   └── isaac-vla-integration/
│       ├── index.md
│       ├── isaac-basics.md
│       ├── perception-manipulation.md
│       └── vla-integration.md
├── src/
├── static/
├── .github/
├── docusaurus.config.js
├── package.json
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## Getting Started

### Option 1: Browse Online
Visit the deployed Docusaurus site to navigate through the modules in a structured course format.

### Option 2: Read on GitHub
Browse the `docs/` folder to read the modules in sequence:
1. Start with `docs/physical-ai-fundamentals/index.md`
2. Continue in the order outlined in `docusaurus.config.js` sidebar

### Option 3: Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/[organization]/physical-ai-and-humanoid-robotics.git
   ```
2. Install dependencies:
   ```bash
   cd physical-ai-and-humanoid-robotics
   npm install
   ```
3. Start the local development server:
   ```bash
   npm start
   ```

## Module Navigation

The textbook is organized into 4 modules across the learning path:

1. **Physical AI Fundamentals** - Introduces core concepts
2. **ROS 2 Integration** - Covers robot operating system fundamentals
3. **Simulation Environments** - Explores simulation tools and techniques
4. **NVIDIA Isaac and VLA Integration** - Advanced integration topics

## Contributing

We welcome contributions to improve the textbook:
- For typos and small fixes: Open a pull request directly
- For substantial changes: Open an issue first to discuss
- See `CONTRIBUTING.md` for detailed guidelines

## Repository Guidelines

- Keep content in plain markdown format
- Reference diagrams and assets rather than embedding large files
- Maintain consistent formatting across all modules
- Follow the learning outcome structure for each page
- Ensure content is accessible to different skill levels