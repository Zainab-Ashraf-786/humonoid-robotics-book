# Data Model: GitHub-Style Textbook Repository

## Repository Structure

### Repository Entity
- **name**: String (e.g., "physical-ai-and-humanoid-robotics")
- **description**: String (repository description)
- **license**: String (license type)
- **readme**: README (main landing page)
- **docs**: Array<Module> (documentation modules)
- **config**: DocusaurusConfig (site configuration)
- **assets**: Array<Asset> (diagrams, images, etc.)

### README Entity
- **title**: String (repository title)
- **description**: String (brief overview)
- **tableOfContents**: Array<String> (list of modules)
- **gettingStarted**: String (initial setup instructions)
- **navigation**: String (how to navigate the content)
- **contributing**: String (how to contribute)

### Module Entity
- **id**: String (unique identifier for the module)
- **title**: String (module name)
- **summary**: String (brief description of the module)
- **learningOutcomes**: Array<String> (what learners will achieve)
- **pages**: Array<Page> (ordered list of pages in the module)
- **order**: Number (position in sequence among modules)
- **prerequisites**: Array<String> (required prior knowledge)
- **assets**: Array<Asset> (module-specific assets)

### Page Entity
- **id**: String (unique identifier for the page)
- **title**: String (page title)
- **module**: Module (reference to parent module)
- **sequence**: Number (order within module)
- **content**: String (markdown content)
- **learningObjectives**: Array<String> (specific to this page)
- **codeExamples**: Array<CodeExample> (code snippets)
- **diagrams**: Array<Diagram> (diagrams referenced in content)

### CodeExample Entity
- **id**: String (unique identifier)
- **language**: String (programming language)
- **code**: String (the actual code)
- **description**: String (what the code demonstrates)
- **page**: Page (reference to parent page)
- **sequence**: Number (order within page)

### Diagram Entity
- **id**: String (unique identifier)
- **filename**: String (file path)
- **title**: String (description of the diagram)
- **type**: String (svg, png, jpeg, etc.)
- **size**: Number (file size in bytes)
- **page**: Page (reference to parent page)

### DocusaurusConfig Entity
- **title**: String (site title)
- **tagline**: String (site tagline)
- **url**: String (deployment URL)
- **baseUrl**: String (base path)
- **organizationName**: String (GitHub org/user)
- **projectName**: String (repository name)
- **themeConfig**: ThemeConfig (theme-specific configuration)
- **sidebarConfig**: SidebarConfig (navigation configuration)

### ThemeConfig Entity
- **navbar**: NavbarConfig (navigation bar settings)
- **footer**: FooterConfig (footer settings)
- **prism**: PrismConfig (code highlighting settings)

### SidebarConfig Entity
- **items**: Array<SidebarItem> (navigation items)
- **collapsible**: Boolean (whether sections can be collapsed)

### SidebarItem Entity
- **type**: String (doc, link, category, etc.)
- **label**: String (display name)
- **id**: String (reference to document)
- **items**: Array<SidebarItem> (sub-items if category)

## Module Specifications

### Module 1: Physical AI Fundamentals
- **ID**: "physical-ai-fundamentals"
- **Title**: "Physical AI Fundamentals"
- **Summary**: "Introduction to Physical AI principles and embodied intelligence"
- **Learning Outcomes**:
  - Understand the fundamental concepts of Physical AI
  - Explain how embodied intelligence differs from traditional AI  
  - Identify applications of Physical AI in robotics
  - Compare Physical AI to traditional AI approaches
- **Pages**: 3-4 pages covering principles, applications, and implementation approaches

### Module 2: ROS 2 Integration
- **ID**: "ros2-integration" 
- **Title**: "ROS 2 Integration"
- **Summary**: "Building and simulating ROS 2 packages and robots"
- **Learning Outcomes**:
  - Create ROS 2 packages for robot control
  - Implement basic robot simulation in ROS 2
  - Understand ROS 2 communication patterns
  - Build basic robot behaviors using ROS 2
- **Pages**: 3-4 pages covering ROS 2 basics, package creation, and simulation

### Module 3: Simulation Environments
- **ID**: "simulation-environments"
- **Title**: "Simulation Environments"
- **Summary**: "ROS 2 packages and robots in simulation environments"
- **Learning Outcomes**:
  - Set up and configure simulation environments
  - Develop robots in simulation for testing
  - Compare strengths of different simulation platforms
  - Implement physics-based robot interactions
- **Pages**: 4-5 pages covering different simulation tools and applications

### Module 4: NVIDIA Isaac and VLA Integration
- **ID**: "isaac-vla-integration"
- **Title**: "NVIDIA Isaac and VLA Integration"
- **Summary**: "AI-driven perception, manipulation, and VLA in humanoid robots"
- **Learning Outcomes**:
  - Use NVIDIA Isaac for perception pipelines
  - Implement manipulation tasks using Isaac tools
  - Integrate Vision-Language-Action in humanoid robots
  - Complete a capstone project combining all concepts
- **Pages**: 3-4 pages covering Isaac basics, perception/manipulation, and VLA integration

## Validation Rules

### Repository Validation
- Repository name must follow GitHub conventions (alphanumeric, hyphens only)
- README must exist and contain essential information
- License file must be present
- Documentation must be in docs/ folder

### Module Validation
- Each module must have a unique ID
- Module title must be descriptive and unique
- Summary must be between 10-200 characters
- Must have 1-5 learning outcomes
- Order must be sequential (1, 2, 3, 4)
- Each module must have at least 1 page

### Page Validation
- Each page must belong to exactly 1 module
- Title must be descriptive and unique within module
- Sequence numbers must be consecutive within a module
- Content must be valid markdown
- Learning objectives must be specific and measurable

### Asset Validation
- Asset filenames must follow naming conventions
- File sizes must be optimized (under 500KB for images)
- Assets must be referenced in at least one page
- External asset references must be valid URLs