import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './CTAButtons.module.css';

const CTAButtons = () => {
  return (
    <section className={clsx('landing-section', styles.ctaSection)}>
      <div className={styles.container}>
        <h2 className={clsx('landing-section-title', styles.sectionTitle)}>
          Ready to Start Your Journey?
        </h2>
        <p className={styles.sectionDescription}>
          Begin exploring the future of Physical AI and Humanoid Robotics today
        </p>
        <div className={styles.buttonsContainer}>
          <Link className={clsx('neon-button', styles.primaryButton)} to="/docs/intro">
            Read the Book
          </Link>
          <Link className={clsx('neon-button', 'neon-button-secondary', styles.secondaryButton)} to="#modules">
            Explore Modules
          </Link>
        </div>
      </div>
    </section>
  );
};

export default CTAButtons;