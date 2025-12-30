import React from 'react';
import clsx from 'clsx';
import styles from './BentoGrid.module.css';

// BentoGrid component for displaying modules in a grid layout
const BentoGrid = ({ children, className = '' }) => {
  return (
    <div className={clsx('bento-grid', styles.bentoGrid, className)}>
      {children}
    </div>
  );
};

// BentoItem component for individual items in the grid
const BentoItem = ({
  title,
  description,
  icon,
  className = '',
  onClick
}) => {
  const handleClick = () => {
    if (onClick) {
      onClick();
    }
  };

  return (
    <div
      className={clsx('bento-item', styles.bentoItem, className)}
      onClick={handleClick}
    >
      <div className={styles.bentoItemHeader}>
        {icon && <div className={styles.bentoItemIcon}>{icon}</div>}
        <h3 className={clsx('glow-text', styles.bentoItemTitle)}>{title}</h3>
      </div>
      <p className={styles.bentoItemDescription}>{description}</p>
    </div>
  );
};

export { BentoGrid, BentoItem };