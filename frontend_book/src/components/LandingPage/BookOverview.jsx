import React from 'react';
import clsx from 'clsx';
import styles from './BookOverview.module.css';

const BookOverview = () => {
  return (
    <section className={clsx('landing-section', styles.bookOverview)}>
      <div className={styles.container}>
        <h2 className={clsx('landing-section-title', styles.sectionTitle)}>
          What You'll Learn
        </h2>
        <div className={styles.overviewGrid}>
          <div className={clsx('landing-card', styles.overviewCard)}>
            <h3 className={clsx('glow-text', styles.cardTitle)}>Vision-Language-Action Models</h3>
            <p className={styles.cardDescription}>
              Master VLA systems that enable robots to perceive, understand, and act in real-world environments
              with unprecedented accuracy and adaptability.
            </p>
          </div>
          <div className={clsx('landing-card', styles.overviewCard)}>
            <h3 className={clsx('glow-text', styles.cardTitle)}>ROS 2 Communication Systems</h3>
            <p className={styles.cardDescription}>
              Build robust robot communication architectures using ROS 2, DDS, and distributed control systems
              for multi-agent coordination.
            </p>
          </div>
          <div className={clsx('landing-card', styles.overviewCard)}>
            <h3 className={clsx('glow-text', styles.cardTitle)}>Digital Twin Simulation</h3>
            <p className={styles.cardDescription}>
              Create physics-based digital twins using Gazebo and Unity for safe AI training and testing
              in realistic virtual environments.
            </p>
          </div>
          <div className={clsx('landing-card', styles.overviewCard)}>
            <h3 className={clsx('glow-text', styles.cardTitle)}>AI-Robot Brain Integration</h3>
            <p className={styles.cardDescription}>
              Develop advanced AI systems that integrate perception, planning, learning, and control
              for autonomous humanoid behavior.
            </p>
          </div>
        </div>
        <div className={styles.scopeSection}>
          <h3 className={clsx('glow-text', styles.scopeTitle)}>Book Scope</h3>
          <p className={styles.scopeDescription}>
            This comprehensive guide covers the complete stack of technologies needed to build intelligent
            humanoid robots. From foundational concepts in embodied AI to advanced implementations of
            control systems, you'll gain both theoretical understanding and practical skills needed to
            work with cutting-edge robotics systems.
          </p>
          <div className={styles.toolsGrid}>
            <div className={styles.toolItem}>ROS 2 (Robot Operating System)</div>
            <div className={styles.toolItem}>Gazebo Physics Simulation</div>
            <div className={styles.toolItem}>Unity 3D Engine</div>
            <div className={styles.toolItem}>PyTorch & TensorFlow</div>
            <div className={styles.toolItem}>OpenCV & Computer Vision</div>
            <div className={styles.toolItem}>Reinforcement Learning</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default BookOverview;