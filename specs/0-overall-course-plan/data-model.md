# Data Model: Overall Course Structure

## Repository Structure

### Course Entity
- **id**: String (e.g., "physical-ai-humanoid-robotics")
- **title**: String ("Physical AI & Humanoid Robotics")
- **description**: String (overview of the complete course)
- **modules**: Array<Module> (ordered list of 4 modules)
- **duration**: Number (13 weeks total)
- **prerequisites**: Array<String> (basic programming and robotics knowledge)
- **targetAudience**: Array<String> (students, AI developers, robotics enthusiasts)
- **repositoryStructure**: String (GitHub-style with docs/ folders)
- **deployment**: String ("GitHub Pages with Docusaurus")

### Module Entity
- **id**: String (unique identifier for each module)
- **title**: String (module name)
- **sequence**: Number (1-4, order in course)
- **duration**: Number (weeks for this module)
- **learningObjectives**: Array<String> (what learners will achieve)
- **prerequisites**: Array<String> (knowledge from previous modules)
- **dependencies**: Array<Module> (modules this one depends on)
- **pages**: Array<Page> (content pages in this module)
- **glossary**: Array<String> (key terms introduced)
- **resources**: Array<String> (required tools, software)

### Page Entity
- **id**: String (unique identifier for the page)
- **title**: String (page title)
- **module**: Module (reference to parent module)
- **sequence**: Number (order within module)
- **contentType**: String ("concept", "tutorial", "reference", "comparison")
- **content**: String (markdown content)
- **learningOutcomes**: Array<String> (specific to this page)
- **crossReferences**: Array<Page> (links to related content in other modules)
- **prerequisites**: Array<String> (specific knowledge required)

### CrossModuleReference Entity
- **sourceModule**: Module (module containing the reference)
- **targetModule**: Module (module being referenced)
- **sourcePage**: Page (page making the reference)
- **targetPage**: Page (page being referenced)
- **relationship**: String ("prerequisite", "builds-on", "comparison", "integration")
- **description**: String (why this reference exists)

### LearningPath Entity
- **id**: String (unique identifier)
- **name**: String (e.g., "Complete Course", "ROS Specialization", etc.)
- **modules**: Array<Module> (sequence of modules in this path)
- **prerequisites**: Array<String> (knowledge needed to start path)
- **outcomes**: Array<String> (what learner achieves by completing path)

## Module Specifications

### Module 1: The Robotic Nervous System (ROS 2)
- **ID**: "ros2-fundamentals" 
- **Title**: "The Robotic Nervous System (ROS 2)"
- **Sequence**: 1
- **Duration**: 3 weeks
- **Learning Objectives**:
  - Understand ROS 2 nodes, topics, services, and actions
  - Create and run basic ROS 2 packages
  - Understand how Python agents interact with ROS controllers
  - Work with URDF for robot description
- **Dependencies**: None (prerequisite module)
- **Prerequisites**: Basic programming knowledge
- **Pages**: 3-4 pages covering fundamentals, communication, Python integration, and robot description

### Module 2: The Digital Twin (Gazebo & Unity)
- **ID**: "digital-twin-sim"
- **Title**: "The Digital Twin (Gazebo & Unity)"
- **Sequence**: 2
- **Duration**: 4 weeks
- **Learning Objectives**:
  - Understand physics simulation concepts (gravity, collisions, contact forces)
  - Configure and use Gazebo for robot simulation
  - Use Unity for high-fidelity rendering and interaction
  - Simulate sensors (LiDAR, depth cameras, IMUs) in both platforms
- **Dependencies**: Module 1 (ROS 2 fundamentals)
- **Prerequisites**: Understanding of ROS 2 concepts
- **Pages**: 4-5 pages covering physics, Gazebo, Unity, and sensor simulation

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- **ID**: "isaac-ai-brain"
- **Title**: "The AI-Robot Brain (NVIDIA Isaac™)"
- **Sequence**: 3
- **Duration**: 3 weeks
- **Learning Objectives**:
  - Understand NVIDIA Isaac Sim for photorealistic simulation
  - Use Isaac ROS for perception and navigation workloads
  - Implement VSLAM, perception, and navigation with Isaac
  - Configure Nav2 for humanoid locomotion path planning
- **Dependencies**: Modules 1 and 2 (ROS 2 and simulation)
- **Prerequisites**: Understanding of ROS 2 and simulation concepts
- **Pages**: 3-4 pages covering Isaac Sim, Isaac ROS, perception, and navigation

### Module 4: Physical AI & Humanoid Robotics (Capstone)
- **ID**: "physical-ai-hr"
- **Title**: "Physical AI & Humanoid Robotics"
- **Sequence**: 4
- **Duration**: 3 weeks
- **Learning Objectives**:
  - Integrate concepts from all previous modules
  - Design and implement a humanoid robot system
  - Apply Physical AI and embodied intelligence principles
  - Complete a capstone project combining all technologies
- **Dependencies**: Modules 1, 2, and 3
- **Prerequisites**: Understanding of all previous concepts
- **Pages**: 3-4 pages covering integration, application, and capstone project

## Validation Rules

### Course Validation
- Course must have exactly 4 modules in sequence 1-4
- Total duration must be approximately 13 weeks
- Target audience must be consistent across modules
- Repository structure must follow GitHub-style conventions

### Module Validation
- Each module must have a unique ID
- Sequence numbers must be consecutive (1-4)
- Each module must have 1-5 learning objectives
- Dependencies must form a valid directed acyclic graph
- Prerequisites must be fulfilled by earlier modules

### Cross-Module Reference Validation
- Reference must point to an existing module/page
- Relationship type must be one of: "prerequisite", "builds-on", "comparison", "integration"
- Description must explain the relevance of the reference
- Circular dependencies must be avoided

### Page Validation
- Each page must belong to exactly 1 module
- Sequence numbers must be consecutive within a module
- Content must be valid markdown
- Cross-references must point to existing pages
- Prerequisites must be satisfied by earlier content