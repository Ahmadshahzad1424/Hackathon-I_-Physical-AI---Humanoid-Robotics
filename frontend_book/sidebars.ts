import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics',
      collapsible: false,
      items: [
        // PREFACE
        {
          type: 'category',
          label: 'PREFACE',
          items: [
            {
              type: 'doc',
              id: 'intro',
              label: 'Preface: From Digital AI to Physical Intelligence'
            }
          ]
        },

        // --------------------------------------------------------
        // MODULE 1: The Robotic Nervous System (ROS 2)
        // --------------------------------------------------------
        {
          type: 'category',
          label: 'Module 1: The Robotic Nervous System (ROS 2)',
          items: [
            {
              type: 'category',
              label: 'Chapter 1: Introduction to ROS 2 for Physical AI',
              items: ['introduction/what-is-ros2']
            },
            {
              type: 'category',
              label: 'Chapter 2: ROS 2 Communication Model',
              items: ['communication-model/ros2-communication']
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

        // --------------------------------------------------------
        // MODULE 2: The Digital Twin
        // --------------------------------------------------------
        {
          type: 'category',
          label: 'Module 2: The Digital Twin',
          items: [
            {
              type: 'category',
              label: 'Chapter 4: Introduction to Digital Twins',
              items: ['digital-twin/introduction']
            },
            {
              type: 'category',
              label: 'Chapter 5: Physics Simulation with Gazebo',
              items: ['digital-twin/physics-simulation']
            },
            {
              type: 'category',
              label: 'Chapter 6: Sensors and Environment Simulation',
              items: ['digital-twin/sensor-simulation']
            },
            {
              type: 'category',
              label: 'Chapter 7: Human-Robot Interaction with Unity',
              items: ['digital-twin/hri-unity']
            }
          ]
        },

        // --------------------------------------------------------
        // MODULE 3: The AI-Robot Brain
        // --------------------------------------------------------
        {
          type: 'category',
          label: 'Module 3: The AI-Robot Brain',
          items: [
            {
              type: 'category',
              label: 'Chapter 8: The Role of Perception in Physical AI',
              items: ['ai-robot-brain/introduction']
            },
            {
              type: 'category',
              label: 'Chapter 9: NVIDIA Isaac Sim and Synthetic Data',
              items: ['ai-robot-brain/isaac-sim']
            },
            {
              type: 'category',
              label: 'Chapter 10: Isaac ROS and Accelerated Perception',
              items: ['ai-robot-brain/isaac-ros']
            },
            {
              type: 'category',
              label: 'Chapter 11: Navigation and Planning with Nav2',
              items: ['ai-robot-brain/nav2-navigation']
            }
          ]
        },

        // --------------------------------------------------------
        // MODULE 4: Vision-Language-Action (VLA)
        // --------------------------------------------------------
        {
          type: 'category',
          label: 'Module 4: Vision-Language-Action (VLA)',
          items: [
            {
              type: 'category',
              label: 'Chapter 12: Introduction to Vision-Language-Action',
              items: [
                'vla/intro',
                'vla/concepts',
                'vla/embodied-intelligence',
                'vla/index'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 13: Voice-to-Action Pipelines',
              items: [
                'vla/voice-to-action',
                'vla/voice-challenges',
                'vla/speech-pipeline',
                'vla/whisper-integration',
                'vla/nlg-processing'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 14: Cognitive Planning with LLMs',
              items: [
                'vla/cognitive-planning',
                'vla/llm-translation',
                'vla/ros2-actions'
              ]
            },
            {
              type: 'category',
              label: 'Chapter 15: Capstone – The Autonomous Humanoid',
              items: [
                'vla/capstone',
                'vla/conclusion'
              ]
            }
          ]
        }
      ]
    }
  ],
};

export default sidebars;