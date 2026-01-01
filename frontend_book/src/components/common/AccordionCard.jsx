import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './AccordionCard.module.css';

// AccordionCard component for displaying expandable content sections
const AccordionCard = ({ title, children, defaultOpen = false, className = '' }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={clsx('accordion-card', styles.accordionCard, className)}>
      <div
        className={clsx('accordion-header', styles.accordionHeader, { [styles.active]: isOpen })}
        onClick={toggleAccordion}
      >
        <h3 className={clsx('glow-text', styles.accordionTitle)}>{title}</h3>
        <div className={clsx('accordion-icon', styles.accordionIcon, { [styles.rotated]: isOpen })}>
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M4 6L8 10L12 6"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
      </div>
      <div
        className={clsx('accordion-content', styles.accordionContent, { [styles.expanded]: isOpen })}
        style={{
          maxHeight: isOpen ? styles.expandedMaxHeight || '500px' : '0',
          opacity: isOpen ? '1' : '0'
        }}
      >
        <div className={styles.accordionContentInner}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default AccordionCard;