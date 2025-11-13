import React, { useState, useEffect, useRef } from 'react';
import styles from './slider.module.css';

interface SliderProps {
  title1: string;
  title2: string;
  sliderTitles1: string[];
  sliderTitles2: string[];
}

const Slider: React.FC<SliderProps> = ({ 
  title1, 
  title2,
  sliderTitles1,
  sliderTitles2 
}) => {
  const totalSliders = sliderTitles1.length + sliderTitles2.length;
  const [values, setValues] = useState<number[]>(() =>
    Array(totalSliders).fill(0)
  );
  const [total, setTotal] = useState<number>(0);
  const sliderRefs = useRef<Array<HTMLInputElement | null>>([]);

  useEffect(() => {
    const sum = values.reduce((acc, val) => acc + val, 0);
    setTotal(sum);
  }, [values]);

  const handleChange = (index: number, value: number) => {
    const currentTotal = values.reduce((acc, val) => acc + val, 0);
    const currentValue = values[index];
    const availablePoints = 100 - (currentTotal - currentValue);
    
    const newValue = Math.min(value, availablePoints);
    const clampedValue = Math.max(0, newValue);

    const newValues = [...values];
    newValues[index] = clampedValue;
    setValues(newValues);
    
    if (sliderRefs.current[index]) {
      const thumb = sliderRefs.current[index].nextElementSibling;
      if (thumb) {
        const inputWidth = sliderRefs.current[index].offsetWidth;
        const thumbPosition = (clampedValue / 100) * inputWidth;
        (thumb as HTMLElement).style.left = `${thumbPosition}px`;
      }
    }
  };

  // стартовая позиция ползунков
  useEffect(() => {
    sliderRefs.current.forEach((ref, index) => {
      if (ref) {
        const thumb = ref.nextElementSibling;
        if (thumb) {
          const inputWidth = ref.offsetWidth;
          const thumbPosition = (values[index] / 100) * inputWidth;
          (thumb as HTMLElement).style.left = `${thumbPosition}px`;
        }
      }
    });
  }, [values]);

  return (
    <div className={styles.container}>
      <h2 className={styles.groupTitle}>{title1}</h2>
      <div className={styles.group}>
        {sliderTitles1.map((title, index) => (
          <div key={index} className={styles.sliderItem}>
            <div className={styles.sliderHeader}>
              <h3>{title}</h3>
              <span>{values[index]}/100</span>
            </div>
            <div className={styles.sliderContainer}>
              <div className={styles.sliderTrack}></div>
              <div 
                className={styles.sliderFill} 
                style={{ width: `${values[index]}%` }}
              ></div>
              <input
                ref={(el) => {
                  sliderRefs.current[index] = el;
                }}
                type="range"
                min="0"
                max="100"
                value={values[index]}
                onChange={(e) => handleChange(index, parseInt(e.target.value))}
                className={styles.sliderInput}
              />
              <div className={styles.sliderThumb}></div>
            </div>
          </div>
        ))}
      </div>

      <h2 className={styles.groupTitle}>{title2}</h2>
      <div className={styles.group}>
        {sliderTitles2.map((title, index) => {
          const globalIndex = sliderTitles1.length + index;
          return (
            <div key={globalIndex} className={styles.sliderItem}>
              <div className={styles.sliderHeader}>
                <h3 className={styles.sliderTitle}>{title}</h3>
                <span className={styles.sliderValue}>{values[globalIndex]}/100</span>
              </div>
              <div className={styles.sliderContainer}>
                <div className={styles.sliderTrack}></div>
                <div 
                  className={styles.sliderFill} 
                  style={{ width: `${values[globalIndex]}%` }}
                ></div>
                <input
                  ref={(el) => {
                    sliderRefs.current[globalIndex] = el;
                  }}
                  type="range"
                  min="0"
                  max="100"
                  value={values[globalIndex]}
                  onChange={(e) => handleChange(globalIndex, parseInt(e.target.value))}
                  className={styles.sliderInput}
                />
                <div className={styles.sliderThumb}></div>
              </div>
            </div>
          );
        })}
      </div>

      <div className={styles.sliderItemResult}>
        <div className={styles.sliderHeader}>
          <h3 className={styles.groupTitleResult}>Итог</h3>
          <span style={{ color: total < 100 ? '#EF4444' : '' }}>
            {total}/100%
          </span>
        </div>
        <div className={styles.sliderContainer}>
          <div className={styles.sliderTrack}></div>
          <div 
            className={styles.sliderFill} 
            style={{ 
              width: `${total}%`,
            }}
          ></div>
          <div 
            className={styles.sliderThumb} 
            style={{ 
              left: `${total}%`,
            }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default Slider;
