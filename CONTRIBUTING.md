# Contribution Guidelines

Thank you for your interest in contributing to the Physical AI & Humanoid Robotics course! This document provides guidelines and instructions for contributing to this educational resource.

## Table of Contents
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Content Standards](#content-standards)
- [Technical Requirements](#technical-requirements)
- [Style Guide](#style-guide)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)

## Ways to Contribute

There are several ways you can contribute to this course:

- **Content Improvements**: Correcting errors, improving explanations, adding examples
- **Module Content**: Creating new sections, tutorials, or exercises
- **Technical Fixes**: Updating code examples, fixing broken links
- **Translation**: Translating content to other languages
- **Feedback**: Reporting issues or suggesting improvements
- **Documentation**: Improving READMEs, guides, or setup instructions

## Getting Started

1. **Fork the repository**: Create your own copy of the repository on GitHub
2. **Clone your fork**: `git clone https://github.com/YOUR-USERNAME/physical-ai-humanoid-robotics.git`
3. **Create a branch**: `git checkout -b feature/your-feature-name`
4. **Make your changes**: Follow the content standards and style guide below
5. **Test your changes**: If applicable, run local tests to ensure everything works
6. **Commit and push**: Make atomic commits with clear messages
7. **Open a Pull Request**: Submit your changes for review

## Content Standards

### Technical Accuracy
- All technical content must align with official documentation for ROS 2, Gazebo, NVIDIA Isaac, Unity, and other covered technologies
- Include citations or references to official documentation when possible
- Test code examples to ensure they work as described
- Verify mathematical formulas and technical concepts

### Educational Value
- Explain concepts clearly and progressively
- Use practical examples related to humanoid robotics where applicable
- Include learning objectives for each section
- Provide clear explanations of complex concepts
- Use consistent terminology throughout the course

### Organization
- Follow the established module structure
- Use the frontmatter templates provided in `docs/_templates/`
- Maintain consistent navigation and cross-references between modules
- Ensure each section builds logically on previous content

## Technical Requirements

### For Code Examples
- Use Python 3.8+ or the minimum supported version for the technology
- Include proper error handling in examples
- Use meaningful variable and function names
- Include comments explaining complex code
- Ensure examples work in the documented environment

### For Documentation
- Use Markdown format with appropriate frontmatter
- Include proper headings hierarchy (H1, H2, H3, etc.)
- Use syntax highlighting for code blocks
- Optimize images for web delivery
- Use relative links for internal navigation

### For Simulations and Examples
- Ensure examples work with the specified versions of ROS, Gazebo, Unity, Isaac, etc.
- Include clear setup instructions
- Provide troubleshooting tips
- Indicate system requirements clearly

## Style Guide

### Writing Style
- Use clear, concise language appropriate for the target audience
- Write in active voice when possible
- Be inclusive and avoid jargon without explanation
- Use consistent terminology across all modules
- Write in American English spelling

### Code Style
- Follow the official style guide for the language being used (PEP 8 for Python, etc.)
- Use consistent indentation (2 spaces for YAML, 4 spaces for Python/C++)
- Name variables and functions descriptively
- Avoid magic numbers; use named constants instead
- Include docstrings for functions and classes when appropriate

### Markdown Style
- Use sentence case for headers (capitalize only the first word and proper nouns)
- Use proper heading hierarchy (# through ######)
- Use backticks for `inline code` and code blocks for multi-line code
- Use descriptive alt text for images
- Use meaningful link text instead of raw URLs

## Pull Request Process

1. **Ensure all tests pass**: If applicable, make sure all automated checks pass
2. **Update documentation**: If your changes affect user-facing functionality, update relevant documentation
3. **Follow commit conventions**: Use descriptive commit messages in present tense (e.g. "Add explanation for ROS 2 topics" not "Added...")
4. **Submit for review**: Create a pull request with a clear title and description
5. **Address feedback**: Be responsive to reviewer comments and make requested changes
6. **Wait for merge**: Once approved, a maintainer will merge your changes

### Pull Request Guidelines
- Keep pull requests focused on a single feature or issue
- Provide a clear description of what your changes do and why they're needed
- Include links to related issues if applicable
- Update the pull request if you make changes after submitting

## Community Guidelines

### Be Respectful
- Respect all contributors regardless of their experience level
- Provide constructive feedback and be open to receiving it
- Remember that this is an educational resource used by people from diverse backgrounds

### Focus on Quality
- Prioritize educational value and technical accuracy
- Ensure contributions benefit the broader learner community
- Maintain high standards for content quality

### Collaborate Effectively
- Communicate clearly in issues and pull requests
- Be patient with questions from beginners
- Help maintain a welcoming environment for all contributors

## Questions?

If you have questions about contributing that aren't addressed in this document, feel free to open an issue for discussion.

---

Thank you for helping to improve the Physical AI & Humanoid Robotics course for all learners!