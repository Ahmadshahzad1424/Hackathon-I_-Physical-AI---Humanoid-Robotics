import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './HeroSection.module.css';

const HeroSection = () => {
  return (
    <section className={clsx('landing-section', styles.heroSection)}>
      <div className={styles.heroContainer}>
        <h1 className={clsx('glow-text', styles.heroTitle)}>
          Physical AI & Humanoid Robotics
        </h1>
        <p className={styles.heroSubtitle}>
          Master the cutting-edge intersection of artificial intelligence and humanoid robotics with our comprehensive guide
        </p>
        <p className={styles.heroDescription}>
          Explore the future of embodied intelligence, from Vision-Language-Action models to advanced control systems,
          digital twins, and AI-powered robotic brains that enable truly autonomous humanoid systems.
        </p>
        <div className={styles.heroButtons}>
          <Link className={clsx('neon-button', styles.primaryButton)} to="/docs/intro">
            Start Reading
          </Link>
          <Link className={clsx('neon-button', 'neon-button-secondary', styles.secondaryButton)} to="#modules">
            Explore Modules
          </Link>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;