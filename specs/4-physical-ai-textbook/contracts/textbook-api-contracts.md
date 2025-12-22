# Textbook API Contracts

## Overview
These contracts define the interfaces for potential interactive components that could be integrated with the Physical AI & Humanoid Robotics textbook. These are conceptual contracts for future enhancements.

## Module Progress Tracking API

### GET /api/modules
Retrieve list of all modules in the textbook
- **Response**: Array of Module objects
- **Module Object**:
  - id: string
  - name: string
  - description: string
  - duration: number (weeks)
  - learningObjectives: string[]
  - prerequisites: string[]
  - status: "not-started" | "in-progress" | "completed"

### GET /api/modules/{moduleId}
Retrieve detailed information about a specific module
- **Parameters**: moduleId (string)
- **Response**: Module object with chapters array

### GET /api/chapters/{chapterId}
Retrieve content for a specific chapter
- **Parameters**: chapterId (string)
- **Response**: Chapter object with content sections and activities

### POST /api/progress/track
Update student progress
- **Request Body**:
  - module: string (moduleId)
  - chapter: string (chapterId)
  - section: string (sectionId)
  - status: "started" | "completed"
- **Response**: Success confirmation

## Activity Execution API

### POST /api/activities/{activityId}/execute
Execute a simulation or practical activity
- **Parameters**: activityId (string)
- **Request Body**: configuration for the activity
- **Response**: execution result and learning assessment

### GET /api/activities/{activityId}/results
Get results from a completed activity
- **Parameters**: activityId (string)
- **Response**: activity results and feedback

## Assessment API

### POST /api/assessments/{assessmentId}/submit
Submit answers for an assessment
- **Parameters**: assessmentId (string)
- **Request Body**: answers array
- **Response**: grading result and feedback

### GET /api/assessments/{assessmentId}/feedback
Get detailed feedback for an assessment
- **Parameters**: assessmentId (string)
- **Response**: detailed feedback and learning recommendations