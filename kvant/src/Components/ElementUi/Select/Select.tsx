import React, { useState, useRef, useEffect } from 'react';
import styles from './select.module.css';
import arrow from '../../../assets/icons/ui/cards/arrow.svg';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps {
  title?: string;
  options: SelectOption[];
  value: string[] | null;
  onChange: (value: string[]) => void;
  placeholder?: string;
  className?: string;
  multiple?: boolean;
  inlineOptions?: boolean;
}

const Select: React.FC<SelectProps> = ({
  title,
  options,
  value = [],
  onChange,
  placeholder = 'Выберите...',
  className = '',
  multiple = false,
  inlineOptions = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const selectRef = useRef<HTMLDivElement>(null);
  
  const handleToggle = () => setIsOpen(!isOpen);
  
  const handleSelect = (selectedValue: string) => {
    if (multiple) {
      const newValue = value ? [...value] : [];
      const valueIndex = newValue.indexOf(selectedValue);
      
      if (valueIndex > -1) {
        newValue.splice(valueIndex, 1);
      } else {
        newValue.push(selectedValue);
      }
      
      onChange(newValue);
    } else {
      onChange([selectedValue]);
      setIsOpen(false);
    }
  };
  
  const handleClickOutside = (event: MouseEvent) => {
    if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  };
  
  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const selectedLabels = value 
    ? options
        .filter(option => value.includes(option.value))
        .map(option => option.label)
        .join(', ')
    : '';

  return (
    <div 
      ref={selectRef}
      className={`${styles.selectContainer} ${className}`}
    >
      {title && <div className={styles.title}>{title}</div>}
      <div 
        className={`${styles.select} ${isOpen ? styles.open : ''}`}
        onClick={handleToggle}
      >
        <div className={styles.selectedValue}>
          {selectedLabels || placeholder}
        </div>
        <div className={styles.arrow}>
          <img src={arrow} alt="↓" />
        </div>
      </div>
      
      {isOpen && (
        <div className={`${styles.optionsList} ${inlineOptions ? styles.inlineOptions : ''}`}>
          {options.map(option => (
            <div
              key={option.value}
              className={`${styles.option} ${
                value && value.includes(option.value) ? styles.selected : ''
              }`}
              onClick={() => handleSelect(option.value)}
            >
              {option.label}
              {multiple && value && value.includes(option.value) && (
                <span className={styles.checkmark}></span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Select;