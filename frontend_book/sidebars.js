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
  // Main sidebar configuration organized by modules
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics',
      collapsible: false,
      items: [
        {
          type: 'category',
          label: 'PREFACE',
          items: [
            'intro'
          ]
        },
        {
          type: 'category',
          label: 'Part 1: The Robotic Nervous System (ROS 2)',
          items: [
            {
              type: 'category',
              label: 'Chapter 1: Introduction to ROS 2 for Physical AI',
              items: [
                'introduction/what-is-ros2'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 2: ROS 2 Communication Model',
              items: [
                'communication-model/ros2-communication'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 3: Robot Structure and Control with URDF',
              items: [
                'urdf-structure/understanding-urdf',
                'urdf-structure/advanced-urdf-concepts',
                'urdf-structure/urdf-in-practice',
                'urdf-structure/conclusion'
              ]
            }
          ]
        },
        {
          type: 'category',
          label: 'Part 2: The Digital Twin',
          items: [
            {
              type: 'category',
              label: 'Chapter 4: Introduction to Digital Twins',
              items: [
                'digital-twin/introduction'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 5: Physics Simulation with Gazebo',
              items: [
                'digital-twin/physics-simulation'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 6: Sensors and Environment Simulation',
              items: [
                'digital-twin/sensor-simulation'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 7: Human-Robot Interaction with Unity',
              items: [
                'digital-twin/hri-unity'
              ]
            }
          ]
        },
        {
          type: 'category',
          label: 'Part 3: The AI-Robot Brain',
          items: [
            {
              type: 'category',
              label: 'Chapter 8: The Role of Perception in Physical AI',
              items: [
                'ai-robot-brain/introduction'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 9: NVIDIA Isaac Sim and Synthetic Data',
              items: [
                'ai-robot-brain/isaac-sim'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 10: Isaac ROS and Accelerated Perception',
              items: [
                'ai-robot-brain/isaac-ros'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 11: Navigation and Planning with Nav2',
              items: [
                'ai-robot-brain/nav2-navigation'
              ]
            }
          ]
        },
        {
          type: 'category',
          label: 'Part 4: Vision-Language-Action (VLA)',
          items: [
            {
              type: 'category',
              label: 'Chapter 12: Introduction to Vision-Language-Action',
              items: [
                'vla/intro'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 13: Voice-to-Action Pipelines',
              items: [
                'vla/voice-to-action'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 14: Cognitive Planning with LLMs',
              items: [
                'vla/cognitive-planning'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 15: Capstone – The Autonomous Humanoid',
              items: [
                'vla/capstone'
              ]
            }
          ]
        }
      ]
    }
  ],
};

module.exports = sidebars;