import React from 'react';
import styles from './checkboxTrue.module.css';

interface CheckboxTrueProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
}

export const CheckboxTrue: React.FC<CheckboxTrueProps> = ({
  checked,
  onChange,
  label,
  disabled = false
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!disabled) {
      onChange(e.target.checked);
    }
  };

  return (
    <label className={styles.label}>
      <input
        type="checkbox"
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        className={styles.hiddenInput}
      />
      <span className={`${styles.customCheckbox} ${checked ? styles.checked : ''}`} />
      {label && <span className={styles.labelText}>{label}</span>}
    </label>
  );
};