---
sidebar_position: 3
---

# URDF in Practice: Loading and Using Robot Descriptions

## Loading URDF in ROS 2

Once you have a URDF file, you need to load it into your ROS 2 system. This is typically done using the `robot_state_publisher` package.

### Robot State Publisher

The `robot_state_publisher` reads a URDF from a parameter, listens to joint information on the `/joint_states` topic, and publishes the 3D poses of the robot links to the `/tf` topic.

```xml
<!-- Example launch file to load URDF -->
<launch>
  <!-- Load the URDF into the parameter server -->
  <param name="robot_description"
         value="$(find-pkg-share my_robot_description)/urdf/my_robot.urdf"/>

  <!-- Start robot state publisher -->
  <node pkg="robot_state_publisher"
        exec="robot_state_publisher"
        name="robot_state_publisher">
    <param name="robot_description"
           value="$(find-pkg-share my_robot_description)/urdf/my_robot.urdf"/>
  </node>
</launch>
```

### Using xacro

For complex robots, URDF files can become very large and repetitive. Xacro (XML Macros) helps by providing macros, properties, and mathematical expressions:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="simple_humanoid">

  <!-- Define properties -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="base_width" value="0.2" />
  <xacro:property name="base_length" value="0.3" />
  <xacro:property name="base_height" value="0.1" />

  <!-- Macro for creating a wheel -->
  <xacro:macro name="wheel" params="prefix parent *origin">
    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="${parent}"/>
      <child link="${prefix}_wheel_link"/>
      <xacro:insert_block name="origin"/>
      <axis xyz="0 1 0"/>
    </joint>

    <link name="${prefix}_wheel_link">
      <visual>
        <geometry>
          <cylinder radius="0.05" length="0.02"/>
        </geometry>
        <material name="black">
          <color rgba="0 0 0 1"/>
        </material>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="0.05" length="0.02"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.1"/>
        <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.002"/>
      </inertial>
    </link>
  </xacro:macro>

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="${base_width} ${base_length} ${base_height}"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
  </link>

</robot>
```

## Working with TF (Transforms)

URDF combined with joint states allows the robot_state_publisher to publish transforms between robot links. These transforms are essential for:

- Robot visualization
- Path planning
- Sensor fusion
- Control algorithms

### TF Tree Visualization

You can visualize the TF tree using:
```bash
ros2 run tf2_tools view_frames
```

This generates a PDF showing all the transforms in your robot.

## URDF and Simulation

### Gazebo Integration

To use your URDF in Gazebo simulation, you need to add Gazebo-specific extensions:

```xml
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
</gazebo>

<!-- For joints -->
<gazebo>
  <joint name="joint_name" type="revolute">
    <axis>
      <xyz>0 0 1</xyz>
    </axis>
  </joint>
</gazebo>
```

## Validation and Debugging

### Checking URDF Validity

Use the check_urdf command to validate your URDF:
```bash
check_urdf /path/to/robot.urdf
```

This will show you the kinematic chain and any errors in your URDF.

### Common Issues and Solutions

1. **Missing joints**: Every link except the base should be connected by joints
2. **Invalid masses**: All links should have proper mass values
3. **Incorrect origins**: Joint origins should properly connect parent and child links
4. **Inconsistent naming**: Link and joint names should be consistent

## Summary

Using URDF in practice involves loading the robot description into ROS 2, using tools like robot_state_publisher to publish transforms, and potentially using xacro to simplify complex robot descriptions. Proper validation and debugging are essential for creating functional robot models.