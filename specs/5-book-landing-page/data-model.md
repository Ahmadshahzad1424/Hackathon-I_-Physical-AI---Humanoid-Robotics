# Data Model: High-Conversion UI/UX Starting Page for Physical AI & Humanoid Robotics Book

## Entities

### Book
- **name**: String - The title of the book
- **description**: String - Brief overview of the book content
- **theme**: String - The main theme (Physical AI & Humanoid Robotics)
- **learningOutcomes**: Array<String> - What readers will learn
- **scope**: String - What topics are covered in the book
- **tools**: Array<String> - Tools and technologies covered
- **skillsGained**: Array<String> - Skills readers will acquire

### Module
- **id**: String - Unique identifier for the module
- **title**: String - Title of the module/chapter
- **description**: String - Brief description of the module content
- **order**: Number - Display order in the sequence
- **topics**: Array<String> - Main topics covered in the module

### User
- **id**: String - Unique identifier for the user
- **type**: String - Type of user (developer, student, enthusiast)
- **interests**: Array<String> - Specific interests in AI/robotics topics

### CTA (Call-to-Action)
- **id**: String - Unique identifier for the CTA
- **text**: String - Text displayed on the button (e.g., "Read the Book", "Explore Modules")
- **target**: String - Where the CTA navigates to
- **style**: Object - Styling properties (color, size, etc.)

## Relationships

- **Book** contains multiple **Module** entities (1 to many)
- **User** interacts with **Book** and **Module** entities
- **Book** has multiple **CTA** entities for navigation

## State Transitions

- **Module** can be in states: visible, hidden (based on user preferences or filtering)

## Validation Rules

- Book name must not be empty
- Module titles must be unique within a book
- Learning outcomes array must contain at least one item
- Module descriptions must not exceed 200 characters
- CTA text must be non-empty and less than 50 characters