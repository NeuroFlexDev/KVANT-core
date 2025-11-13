import React from 'react';
import styles from './footer.module.css';

interface FooterProps {
  currentStep: number;
  totalSteps: number;
  onStepChange: (step: number) => void;
  onSave?: () => void;
  onCalculate?: () => void;
  saveDisabled?: boolean;
  calculateDisabled?: boolean;
}

const Footer: React.FC<FooterProps> = ({
  currentStep,
  totalSteps,
  onStepChange,
  onSave,
  onCalculate,
  saveDisabled = false,
  calculateDisabled = false
}) => {
  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      onStepChange(currentStep + 1);
    }
  };

  const handleBack = () => {
    console.log(currentStep);
    if (currentStep > 0) {
      onStepChange(currentStep - 1);
    }
  };

  return (
    <footer className={styles.footer}>
      <div className={styles.buttonGroup}>
        <button
          className={styles.button}
          onClick={onSave}
          disabled={saveDisabled}
          type="button"
        >
          Сохранить
        </button>
        <button
          className={styles.button}
          onClick={onCalculate}
          disabled={calculateDisabled}
          type="button"
        >
          Рассчитать
        </button>
      </div>
      
      <div className={styles.buttonGroup}>
        <button
          className={styles.button}
          onClick={handleBack}
          disabled={currentStep === 0}
          type="button"
        >
          Назад
        </button>
        <button
          className={styles.button}
          onClick={handleNext}
          disabled={currentStep === totalSteps - 1}
          type="button"
        >
          Далее
        </button>
      </div>
    </footer>
  );
};

export default Footer;