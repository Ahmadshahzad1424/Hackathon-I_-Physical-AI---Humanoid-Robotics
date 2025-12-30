---
sidebar_position: 2
---

# Advanced URDF Concepts

## Links and Visual Properties

Links are the fundamental building blocks of a robot in URDF. Each link represents a rigid body part of the robot.

### Visual Elements

The visual element defines how a link appears in simulation and visualization tools:

```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <!-- Can be box, cylinder, sphere, or mesh -->
    <box size="1 1 1"/>
  </geometry>
  <material name="red">
    <color rgba="1 0 0 1"/>
  </material>
</visual>
```

### Collision Elements

Collision elements define the shape used for physics simulation:

```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="1 1 1"/>
  </geometry>
</collision>
```

### Inertial Elements

Inertial elements define the physical properties for dynamics simulation:

```xml
<inertial>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <mass value="1.0"/>
  <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
</inertial>
```

## Joint Types and Properties

Joints define the connection between links and their possible movements.

### Fixed Joints

Fixed joints connect two links rigidly:

```xml
<joint name="fixed_joint" type="fixed">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 1" rpy="0 0 0"/>
</joint>
```

### Revolute Joints

Revolute joints allow rotation around a single axis:

```xml
<joint name="revolute_joint" type="revolute">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
</joint>
```

### Continuous Joints

Continuous joints allow unlimited rotation around an axis:

```xml
<joint name="continuous_joint" type="continuous">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
</joint>
```

## Coordinate Frames and Transforms

Each link has its own coordinate frame. The origin in joints defines the transform between parent and child frames:

- **xyz**: Translation in meters
- **rpy**: Rotation in radians (roll, pitch, yaw)

## URDF Best Practices

1. **Use meaningful names**: Name links and joints descriptively
2. **Proper mass properties**: Estimate realistic masses and inertias
3. **Collision vs. visual**: Use simpler shapes for collision to improve performance
4. **Validate your URDF**: Check for proper connections and valid XML

## Summary

Advanced URDF concepts provide the tools to create detailed and accurate robot descriptions. Understanding links, joints, and coordinate frames is essential for creating functional humanoid robot models.