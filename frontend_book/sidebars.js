// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 * - create an ordered group of docs
 * - render a sidebar for each doc of that group
 * - provide next/previous navigation
 *
 * The sidebars can be generated from the filesystem, or explicitly defined here.
 *
 * Create as many sidebars as you want.
 */
const sidebars = {
  // Manual sidebar configuration for the ROS2 URDF book
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Introduction to ROS 2',
      items: [
        'introduction/what-is-ros2'
      ],
    },
    {
      type: 'category',
      label: 'ROS 2 Communication Model',
      items: [
        'communication-model/ros2-communication'
      ],
    },
    {
      type: 'category',
      label: 'Robot Structure with URDF',
      items: [
        'urdf-structure/understanding-urdf',
        'urdf-structure/advanced-urdf-concepts',
        'urdf-structure/urdf-in-practice',
        'urdf-structure/conclusion'
      ],
    },
    {
      type: 'category',
      label: 'The Digital Twin (Gazebo & Unity)',
      items: [
        'digital-twin/introduction',
        'digital-twin/physics-simulation',
        'digital-twin/sensor-simulation',
        'digital-twin/hri-unity'
      ],
    },
  ],
};

module.exports = sidebars;