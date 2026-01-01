import React from 'react';
import clsx from 'clsx';
import { BentoGrid, BentoItem } from '../common/BentoGrid';
import styles from './ModulesGrid.module.css';

const ModulesGrid = () => {
  const modules = [
    {
      id: 'preface',
      title: 'Preface',
      description: 'Introduction to embodied intelligence and the fundamentals of Physical AI',
      icon: '📖'
    },
    {
      id: 'vla',
      title: 'Part 1: Vision-Language-Action (VLA)',
      description: 'Deep dive into multimodal AI systems that enable robots to perceive and act in the real world',
      icon: '👁️'
    },
    {
      id: 'ros2',
      title: 'Part 2: ROS 2 Communication',
      description: 'Building robust robot communication systems with ROS 2, DDS, and distributed control',
      icon: '📡'
    },
    {
      id: 'digital-twin',
      title: 'Part 3: Digital Twins & Simulation',
      description: 'Physics-based simulation with Gazebo and Unity for safe AI training and testing',
      icon: '🎮'
    },
    {
      id: 'ai-brain',
      title: 'Part 4: AI-Robot Brain',
      description: 'Advanced AI integration for perception, planning, learning, and control systems',
      icon: '🧠'
    },
    {
      id: 'robot-structure',
      title: 'Part 5: Robot Structure & Control',
      description: 'URDF, kinematics, dynamics, and control systems for humanoid robots',
      icon: '🦾'
    }
  ];

  return (
    <section id="modules" className={clsx('landing-section', styles.modulesGrid)}>
      <div className={styles.container}>
        <h2 className={clsx('landing-section-title', styles.sectionTitle)}>
          Book Modules
        </h2>
        <p className={styles.sectionDescription}>
          Explore our comprehensive curriculum covering all aspects of Physical AI and Humanoid Robotics
        </p>
        <BentoGrid className={styles.bentoGrid}>
          {modules.map((module, index) => (
            <BentoItem
              key={module.id}
              title={module.title}
              description={module.description}
              icon={module.icon}
              className={clsx('glow-element', styles.bentoItem)}
            />
          ))}
        </BentoGrid>
      </div>
    </section>
  );
};

export default ModulesGrid;