import React, { useState, useRef, useEffect } from 'react';
import styles from './numberFieldsGrid.module.css';
import openIcon from '../../../assets/icons/ui/cards/open.svg';

interface NumberFieldsGridProps {
  children: React.ReactNode;
  title?: string;
}

const NumberFieldsGrid: React.FC<NumberFieldsGridProps> = ({ children, title }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [hasScroll, setHasScroll] = useState(false);
  const gridRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (gridRef.current) {
      setHasScroll(gridRef.current.scrollHeight > gridRef.current.clientHeight);
    }
  }, [children]);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={styles.container}>
      {title && <div className={styles.header}>
        <p className={styles.title}>{title}</p>
      </div>}
      <div 
        ref={gridRef}
        className={`${styles.gridContainer} ${isExpanded ? styles.expanded : ''}`}
      >
        {children}
      </div>
      {hasScroll && (
        <button className={styles.expandButton} onClick={toggleExpand}>
          {/* {isExpanded ? 'Свернуть' : 'Расширить'} */}
          <img src={openIcon} alt="Расширить" />
        </button>
      )}
    </div>
  );
};

export default NumberFieldsGrid;