# Quickstart Guide: Physical AI & Humanoid Robotics Course

## Course Overview

This comprehensive course covers Physical AI and humanoid robotics through 4 progressive modules. Designed as a GitHub-style textbook repository deployed with Docusaurus, it provides a structured learning path from ROS 2 fundamentals to advanced AI integration.

## Learning Path

The course is organized into 4 sequential modules with cumulative knowledge building:

1. **Module 1: The Robotic Nervous System (ROS 2)** (Weeks 1-3)
   - Foundation: ROS 2 concepts, communication patterns, Python integration
   - Prerequisites: Basic programming knowledge
   - Outcome: Understanding of ROS 2 as robot middleware

2. **Module 2: The Digital Twin (Gazebo & Unity)** (Weeks 4-7)
   - Foundation: Physics simulation, Gazebo, Unity, sensor simulation
   - Prerequisites: Module 1 completion
   - Outcome: Ability to simulate robots and sensors in virtual environments

3. **Module 3: The AI-Robot Brain (NVIDIA Isaac™)** (Weeks 8-10)
   - Foundation: Isaac Sim, Isaac ROS, perception, navigation
   - Prerequisites: Modules 1 & 2 completion
   - Outcome: Understanding of AI-driven perception and navigation

4. **Module 4: Physical AI & Humanoid Robotics (Capstone)** (Weeks 11-13)
   - Foundation: Integration of all previous concepts
   - Prerequisites: Modules 1, 2 & 3 completion
   - Outcome: Complete humanoid robot system with embodied intelligence

## Repository Structure

```
physical-ai-humanoid-robotics/
├── docs/
│   ├── ros2-fundamentals/          # Module 1
│   │   ├── index.md
│   │   ├── nodes-topics-services.md
│   │   └── ...
│   ├── digital-twin-sim/           # Module 2
│   │   ├── index.md
│   │   ├── physics-fundamentals.md
│   │   └── ...
│   ├── isaac-ai-brain/             # Module 3
│   │   ├── index.md
│   │   ├── isaac-sim.md
│   │   └── ...
│   └── physical-ai-hr/             # Module 4
│       ├── index.md
│       ├── integration.md
│       └── ...
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
Visit the deployed Docusaurus site to navigate through modules sequentially or access specific topics.

### Option 2: Read on GitHub
Browse the `docs/` folder to read modules in sequence:
1. Start with `docs/ros2-fundamentals/index.md`
2. Proceed in order: digital-twin-sim → isaac-ai-brain → physical-ai-hr

### Option 3: Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/[organization]/physical-ai-humanoid-robotics.git
   ```
2. Install dependencies:
   ```bash
   cd physical-ai-humanoid-robotics
   npm install
   ```
3. Start the local development server:
   ```bash
   npm start
   ```

## Prerequisites

Before starting the course, ensure you have:
- Basic programming knowledge (Python preferred)
- Understanding of fundamental robotics concepts
- Access to appropriate computing resources for simulation
- Familiarity with Git and GitHub

## Module Dependencies

- **Module 2** requires completion of **Module 1**
- **Module 3** requires completion of **Modules 1 & 2**  
- **Module 4** requires completion of **Modules 1, 2 & 3**

Each module explicitly lists the prerequisite knowledge required to succeed.

## Technical Requirements

### Module 1 (ROS 2):
- Linux environment (Ubuntu 20.04/22.04)
- ROS 2 Humble Hawksbill
- Python 3.8+

### Module 2 (Simulation):
- Gazebo Garden or compatible version
- Unity Hub with Unity 2021.3 LTS or newer
- Unity Robotics Package

### Module 3 (AI):
- NVIDIA Isaac Sim
- Isaac ROS packages
- CUDA-compatible GPU with 4GB+ VRAM

### All Modules:
- GitHub repository access
- Docusaurus documentation browser
- Markdown editor for content contribution

## Learning Outcomes

After completing all 4 modules, you will:

1. Master ROS 2 as a robot middleware system
2. Create and simulate complex robotic systems with Gazebo and Unity
3. Implement AI-driven perception and navigation with NVIDIA Isaac
4. Integrate Physical AI and embodied intelligence in humanoid robots
5. Build complete humanoid robot systems combining all technologies
6. Understand the complete pipeline from simulation to deployment

## Getting Help

- Use the navigation sidebar to find relevant modules
- Check the glossary for technical terms
- Review prerequisite modules if concepts are unclear
- Use the community forum for advanced questions
- Refer to official documentation for detailed technical information