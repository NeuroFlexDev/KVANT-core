import React from 'react';
import styles from './numberField.module.css'

interface NumberFieldProps {
  title: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  disabled?: boolean;
  background?: string;
}

const NumberField: React.FC<NumberFieldProps> = ({
  title,
  value,
  onChange,
  placeholder,
  disabled = false,
  background
}) => {
  const getBackgroundColor = () => {
    if (background) return background;
    return disabled ? '#3A7F88' : '#F7F7F7';
  };

  return (
    <div className={styles.inputContainer}>
      <h2 className={styles.inputTitle}>{title}</h2>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className={styles.inputField}
        style={{
          backgroundColor: getBackgroundColor(),
          color: disabled ? '#FFFFFF' : '#000000',
          cursor: disabled ? 'not-allowed' : 'text'
        }}
      />
    </div>
  );
};

export default NumberField;