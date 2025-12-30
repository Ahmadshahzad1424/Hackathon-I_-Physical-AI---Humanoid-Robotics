---
sidebar_position: 1
---

# Robot Structure with URDF

## Understanding URDF for Humanoid Robots

URDF (Unified Robot Description Format) is an XML format used to describe the physical structure of robots in ROS. For humanoid robots, URDF is essential for:

- Describing the robot's kinematic chain
- Defining joint limits and properties
- Specifying visual and collision properties
- Enabling simulation and control

## Basic URDF Structure

A URDF file contains elements that describe the robot:

### Links
Links represent rigid bodies in the robot. Each link has:
- Visual properties (for display)
- Collision properties (for physics simulation)
- Inertial properties (for dynamics)

### Joints
Joints connect links together and define the kinematic relationship between them:
- Joint type (revolute, continuous, prismatic, fixed, etc.)
- Joint limits (for revolute and prismatic joints)
- Joint axis and origin

## Example URDF for a Simple Humanoid Robot

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Neck joint -->
  <joint name="neck_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="10" velocity="1"/>
  </joint>
</robot>
```

## Links, Joints, and Coordinate Frames

### Links
Links define the rigid bodies of the robot. Each link should have:
- A unique name
- Visual elements (how it looks)
- Collision elements (for physics)
- Inertial elements (for dynamics)

### Joints
Joints define how links move relative to each other:
- **Fixed**: No movement between links
- **Revolute**: Single axis rotation with limits
- **Continuous**: Single axis rotation without limits
- **Prismatic**: Single axis translation with limits
- **Planar**: Movement on a plane
- **Floating**: 6 DOF movement

### Coordinate Frames
Each link has its own coordinate frame. The origin of joints defines how the frames are related.

## How URDF Enables Control, Sensing, and Digital Twins

### Control
URDF provides:
- Kinematic chain information for inverse kinematics
- Joint limits for safe operation
- Mass properties for dynamics

### Sensing
URDF enables:
- Sensor placement in the robot structure
- Transform relationships between sensors and robot parts
- Simulation of sensor data

### Digital Twins
URDF allows:
- Accurate simulation of the physical robot
- Testing of control algorithms in simulation
- Visualization of robot state

## Simulation Readiness

To make your URDF ready for simulation:

1. **Complete kinematic chain**: Ensure all parts are connected
2. **Proper mass properties**: Include realistic inertial parameters
3. **Collision geometry**: Define collision shapes for physics
4. **Joint limits**: Set appropriate limits for safety
5. **Gazebo plugins**: Add simulation-specific elements if needed

## URDF Best Practices for Humanoid Robots

1. **Start simple**: Begin with basic shapes and add complexity gradually
2. **Use proper naming conventions**: Use descriptive names for links and joints
3. **Include all necessary transforms**: Ensure TF tree is complete
4. **Validate your URDF**: Use tools like `check_urdf` to verify correctness
5. **Consider manufacturing constraints**: Design joints that can be physically realized

## Summary

URDF is fundamental to humanoid robotics in ROS. It provides the necessary description of robot structure that enables simulation, control, and visualization. Properly designed URDF files are essential for creating functional humanoid robot systems.