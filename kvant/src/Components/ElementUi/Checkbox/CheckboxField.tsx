import React from 'react';
import styles from './checkboxField.module.css';

interface CheckboxFieldProps {
  title: string;
  value: boolean | null;
  onChange: (value: boolean) => void;
  inline?: boolean;
  className?: string;
}

const CheckboxField: React.FC<CheckboxFieldProps> = ({
  title,
  value,
  onChange,
  inline = false,
  className = ''
}) => {
  return (
    <div className={`${styles.container} ${inline ? styles.inline : styles.block} ${className}`}>
      <div className={styles.title}>{title}</div>
      
      <div className={styles.options}>
        <button
          type="button"
          className={`${styles.button} ${value === true ? styles.active : ''}`}
          onClick={() => onChange(true)}
        >
          Да
        </button>
        
        <button
          type="button"
          className={`${styles.button} ${value === false ? styles.active : ''}`}
          onClick={() => onChange(false)}
        >
          Нет
        </button>
      </div>
    </div>
  );
};

export default CheckboxField;