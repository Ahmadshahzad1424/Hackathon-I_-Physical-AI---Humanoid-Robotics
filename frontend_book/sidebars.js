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
    'intro',
    {
      type: 'category',
      label: 'Module 1 - ROS 2 & URDF Structure',
      items: [
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
        }
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - Digital Twin (Gazebo & Unity)',
      items: [
        {
          type: 'category',
          label: 'The Digital Twin',
          items: [
            'digital-twin/introduction',
            'digital-twin/physics-simulation',
            'digital-twin/sensor-simulation',
            'digital-twin/hri-unity'
          ],
        }
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - AI-Robot Brain (NVIDIA Isaac)',
      items: [
        {
          type: 'category',
          label: 'The AI-Robot Brain',
          items: [
            'ai-robot-brain/introduction',
            'ai-robot-brain/isaac-sim',
            'ai-robot-brain/isaac-ros',
            'ai-robot-brain/nav2-navigation'
          ],
        }
      ],
    },
    {
      type: 'category',
      label: 'Module 4 - Vision-Language-Action (VLA)',
      items: [
        {
          type: 'category',
          label: 'Vision-Language-Action Overview',
          items: [
            'vla/index',
            'vla/intro',
            'vla/concepts',
            'vla/embodied-intelligence',
            'vla/architecture'
          ],
        },
        {
          type: 'category',
          label: 'Voice-to-Action Systems',
          items: [
            'vla/voice-to-action',
            'vla/whisper-integration',
            'vla/speech-pipeline',
            'vla/voice-challenges'
          ],
        },
        {
          type: 'category',
          label: 'Cognitive Planning with LLMs',
          items: [
            'vla/cognitive-planning',
            'vla/llm-translation',
            'vla/ros2-actions',
            'vla/nlg-processing'
          ],
        },
        {
          type: 'category',
          label: 'Capstone: Autonomous Humanoid',
          items: [
            'vla/capstone',
            'vla/perception-system',
            'vla/navigation-system',
            'vla/manipulation-system',
            'vla/integration-overview'
          ],
        },
        {
          type: 'category',
          label: 'Implementation & Best Practices',
          items: [
            'vla/edge-cases',
            'vla/implementation-guidelines',
            'vla/conclusion'
          ],
        }
      ],
    },
  ],
};

module.exports = sidebars;