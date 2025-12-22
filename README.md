# Physical AI & Humanoid Robotics Course

This repository contains a comprehensive 4-module course covering Physical AI and humanoid robotics through progressive learning from ROS 2 fundamentals to advanced humanoid AI integration. Designed as a GitHub-style textbook repository deployed with Docusaurus.

## Course Overview

This comprehensive course covers Physical AI and humanoid robotics through 4 progressive modules:

1. **Module 1: The Robotic Nervous System (ROS 2)** - Foundation in ROS 2 concepts, communication patterns, and Python integration
2. **Module 2: The Digital Twin (Gazebo & Unity)** - Physics simulation, Gazebo, Unity, and sensor simulation
3. **Module 3: The AI-Robot Brain (NVIDIA Isaac™)** - Isaac Sim, Isaac ROS, perception, and navigation
4. **Module 4: Physical AI & Humanoid Robotics (Capstone)** - Integration of all previous concepts in humanoid robotics, including LLM-based cognitive planning

## Repository Structure

```
physical-ai-humanoid-robotics/
├── docs/                    # Module documentation
│   ├── ros2-fundamentals/   # Module 1: The Robotic Nervous System (ROS 2)
│   │   ├── index.md
│   │   ├── nodes-topics-services.md
│   │   ├── python-integration.md
│   │   ├── urdf.md
│   │   └── conclusion.md
│   ├── digital-twin-sim/    # Module 2: The Digital Twin (Gazebo & Unity)
│   │   ├── index.md
│   │   ├── physics-fundamentals.md
│   │   ├── gazebo-simulation.md
│   │   ├── unity-rendering.md
│   │   ├── sensor-simulation.md
│   │   └── conclusion.md
│   ├── isaac-ai-brain/      # Module 3: The AI-Robot Brain (NVIDIA Isaac™)
│   │   ├── index.md
│   │   ├── isaac-sim.md
│   │   ├── isaac-ros.md
│   │   ├── perception.md
│   │   ├── navigation.md
│   │   └── conclusion.md
│   └── physical-ai-hr/      # Module 4: Physical AI & Humanoid Robotics (Capstone)
│       ├── index.md
│       ├── chapter-1-physical-ai.md
│       ├── chapter-2-llm-planning.md
│       ├── chapter-3-sim2real.md
│       ├── chapter-4-complete-system.md
│       └── conclusion.md
├── specs/                   # Implementation specifications for all modules
│   ├── 1-ros2-fundamentals/
│   ├── 2-digital-twin-sim/
│   ├── 3-isaac-ai-brain/
│   ├── 4-physical-ai-hr/
│   └── 0-overall-course-plan/
├── src/                     # Source code and examples
├── static/                  # Static assets
├── blog/                    # Course updates and announcements
├── history/                 # Historical records and prompt history
├── .github/                 # GitHub templates and workflows
├── docusaurus.config.ts     # Site configuration
├── sidebars.ts              # Navigation structure
├── package.json             # Dependencies and scripts
├── course-overview.md       # Complete course structure and overview
└── README.md               # This file
```

## Getting Started

### Local Development

```sh
npm install
npm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```sh
npm run build
```

This command generates static content into the `build` directory and can be served using any static content hosting service.

## Learning Path

1. Start with [Module 1: The Robotic Nervous System (ROS 2)](./docs/ros2-fundamentals/)
2. Proceed to [Module 2: The Digital Twin (Gazebo & Unity)](./docs/digital-twin-sim/)
3. Continue with [Module 3: The AI-Robot Brain (NVIDIA Isaac™)](./docs/isaac-ai-brain/)
4. Complete with [Module 4: Physical AI & Humanoid Robotics (Capstone)](./docs/physical-ai-hr/)

Each module builds upon the previous one, so following the sequence is recommended for optimal learning. For a complete overview of the entire course structure and integration points, see [course-overview.md](./docs/course-overview.md).

## Course Philosophy: Physical AI & Embodied Intelligence

This course is grounded in Physical AI principles, where intelligence emerges from the interaction between agent, body, and environment. Key principles include:

- **Embodied Cognition**: Cognition is deeply rooted in the body's interactions with the physical world
- **Morphological Computation**: The body's physical form contributes to computation
- **Situatedness**: Intelligence cannot be separated from its environmental context
- **Emergence**: Complex behaviors emerge from simple local interactions

## Contributing

We welcome contributions to improve the textbook:
- For typos and small fixes: Open a pull request directly
- For substantial changes: Open an issue first to discuss
- See CONTRIBUTING.md for detailed guidelines

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Deployment

Using SSH:

```sh
USE_SSH=true npm run deploy
```

Not using SSH:

```sh
GIT_USER=<Your GitHub username> npm run deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.