# Data Model: Book Structure for Physical AI & Humanoid Robotics

## Book Structure Entity

### Entity: BookPart
- **name**: String (e.g., "Preface", "VLA", "ROS 2", "Digital Twins", "AI-Robot Brain", "Robot Structure")
- **order**: Integer (1-6) - Determines the sequence of parts in the book
- **chapters**: Array of Chapter entities
- **description**: String - Brief description of the part's content focus

### Entity: Chapter
- **name**: String (e.g., "Introduction to ROS 2", "Physics Simulation with Gazebo")
- **number**: Integer (sequential within each part)
- **subtopics**: Array of Subtopic entities
- **part**: Reference to BookPart entity
- **label**: String - Display label for navigation

### Entity: Subtopic
- **name**: String (e.g., "What is ROS 2", "Advanced URDF Concepts")
- **path**: String (e.g., "introduction/what-is-ros2", "urdf-structure/advanced-urdf-concepts")
- **chapter**: Reference to Chapter entity
- **title**: String - Title of the documentation page

## Sidebar Configuration Structure

### Docusaurus Sidebar Object
- **type**: String ("category")
- **label**: String - Display name for the navigation item
- **collapsible**: Boolean (default: true) - Whether the section can be collapsed
- **collapsed**: Boolean (default: false) - Whether the section is collapsed by default
- **items**: Array of (SidebarItem | SidebarCategory) - Child navigation items

### SidebarItem
- **type**: String ("doc", "link", etc.)
- **id**: String - Reference to the documentation file
- **label**: String - Display name (optional, uses document title if not provided)

### SidebarCategory
- **type**: String ("category")
- **label**: String - Display name for the category
- **items**: Array of (SidebarItem | SidebarCategory) - Child items
- **collapsible**: Boolean - Whether this category can be collapsed
- **collapsed**: Boolean - Whether this category is collapsed by default

## Relationships
- BookPart contains multiple Chapters (1 to many)
- Chapter contains multiple Subtopics (1 to many)
- Subtopic belongs to one Chapter
- Chapter belongs to one BookPart
- Sidebar configuration represents the hierarchical structure of BookPart → Chapter → Subtopic