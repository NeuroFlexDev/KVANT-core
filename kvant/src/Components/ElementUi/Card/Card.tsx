import React, { useState } from 'react';
import styles from './card.module.css';

interface CardProps {
  id: string | number;
  image?: string;
  selectedImage?: string;
  text: string;
  description?: string;
  primary?: boolean;
  selected?: boolean;
  onSelect: (id: string | number) => void;
}

const Card: React.FC<CardProps> = ({
  id,
  image,
  selectedImage,
  text,
  description,
  primary = false,
  selected = false,
  onSelect
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const handleClick = () => {
    onSelect(id);
  };

  return (
    <div
      className={`${styles.card}
                  ${primary ? styles.primaryBorder : styles.defaultBorder}
                  ${selected ? styles.selected : ''}
                  ${isHovered && !selected ? styles.hovered : ''}`}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {image && (
        <div className={styles.imageContainer}>
          <img
            src={
              (selected && selectedImage) ||
              (isHovered && selectedImage) ||
              image
            }
            alt={text}
            className={styles.image}
          />
        </div>
      )}

      <div className={styles.content}>
        <h3 className={primary ? styles.title : styles.secondaryTitle}>{text}</h3>
        {description && <p className={primary ? styles.description : styles.secondaryDescription}>{description}</p>}
      </div>
    </div>
  );
};

export default Card;