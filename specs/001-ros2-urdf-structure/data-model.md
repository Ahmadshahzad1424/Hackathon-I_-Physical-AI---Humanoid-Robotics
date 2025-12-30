# Data Model: ROS 2 for Physical AI & Humanoid Robotics - Robot Structure with URDF

## Documentation Structure

### Chapter Entity
- **Name**: String (required) - The chapter title
- **Description**: String - Brief overview of the chapter content
- **Sections**: Array of Section entities - The sections within the chapter
- **Examples**: Array of Example entities - Code/URDF examples in the chapter
- **Learning Objectives**: Array of String - What the user should learn

### Section Entity
- **Title**: String (required) - The section title
- **Content**: String - The main content of the section
- **Type**: Enum (text, code, diagram, exercise) - The type of content
- **Dependencies**: Array of String - Other sections this section depends on
- **Related Sections**: Array of String - Sections that complement this one

### Example Entity
- **Title**: String (required) - The example title
- **Description**: String - What the example demonstrates
- **Code**: String - The actual code or URDF content
- **Language**: String - The language/type (Python, URDF, bash, etc.)
- **Usage**: String - How to run or use the example
- **Expected Output**: String - What the user should see when running

## ROS 2 Specific Entities

### ROS 2 Node Entity
- **Name**: String (required) - The node name
- **Publisher Topics**: Array of Topic entities - Topics this node publishes to
- **Subscriber Topics**: Array of Topic entities - Topics this node subscribes to
- **Services**: Array of Service entities - Services this node provides or uses
- **Parameters**: Object - Configuration parameters for the node

### Topic Entity
- **Name**: String (required) - The topic name
- **Message Type**: String (required) - The message type (e.g., std_msgs/String)
- **Description**: String - What data flows through this topic
- **Publishers**: Array of Node names - Nodes that publish to this topic
- **Subscribers**: Array of Node names - Nodes that subscribe to this topic

### Service Entity
- **Name**: String (required) - The service name
- **Request Type**: String (required) - The request message type
- **Response Type**: String (required) - The response message type
- **Description**: String - What the service does

## URDF Specific Entities

### URDF Model Entity
- **Name**: String (required) - The robot name
- **Links**: Array of Link entities - The rigid bodies of the robot
- **Joints**: Array of Joint entities - The connections between links
- **Materials**: Array of Material entities - Visual materials used
- **Gazebo Plugins**: Array of String - Gazebo-specific plugins

### Link Entity
- **Name**: String (required) - The link name
- **Inertial**: Object - Mass, center of mass, and inertia properties
- **Visual**: Object - Visual representation (geometry, material)
- **Collision**: Object - Collision properties (geometry)
- **Parent Joint**: String - The joint that connects this link to its parent

### Joint Entity
- **Name**: String (required) - The joint name
- **Type**: Enum (revolute, continuous, prismatic, fixed, etc.) - The joint type
- **Parent**: String (required) - The parent link name
- **Child**: String (required) - The child link name
- **Origin**: Object - Position and orientation of the joint
- **Axis**: Object - Axis of rotation or translation
- **Limits**: Object - Joint limits (for revolute/prismatic joints)

### Material Entity
- **Name**: String (required) - The material name
- **Color**: Object - RGBA color values
- **Texture**: String - Path to texture file (optional)