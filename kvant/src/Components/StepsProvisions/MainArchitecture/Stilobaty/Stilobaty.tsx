import React from 'react';
import styles from '../mainArchitecture.module.css';
import NumberField from '../../../ElementUi/NumberField/NumberField';
import { CheckboxTrue } from '../../../ElementUi/CheckboxTrue/Checkbox';
import CheckboxField from '../../../ElementUi/Checkbox/CheckboxField';
import Input from '../../../ElementUi/Input/Input';
import Select from '../../../ElementUi/Select/Select';

interface StilobatyProps {
  stilobatCount: number;
  stilobatCalculated: boolean[];
  stilobatFloors: string[];
  stilobatAvgArea: string[];
  stilobatAvgHeight: string[];
  stilobatTotalArea: string[];
  stilobatGnsArea: string[];
  stilobatVolume: string[];
  stilobatStairs: string[];
  stilobatSmokelessStairs: string[];
  stilobatLifts: string[];
  hasGarbageChute: boolean;
  publicPremisesCount: string;
  publicPremisesPurpose: string[] | null;
  onStilobatCalculatedChange: (value: boolean[]) => void;
  onStilobatFloorsChange: (value: string[]) => void;
  onStilobatAvgAreaChange: (value: string[]) => void;
  onStilobatAvgHeightChange: (value: string[]) => void;
  onStilobatTotalAreaChange: (value: string[]) => void;
  onStilobatGnsAreaChange: (value: string[]) => void;
  onStilobatVolumeChange: (value: string[]) => void;
  onStilobatStairsChange: (value: string[]) => void;
  onStilobatSmokelessStairsChange: (value: string[]) => void;
  onStilobatLiftsChange: (value: string[]) => void;
  onHasGarbageChuteChange: (value: boolean) => void;
  onPublicPremisesCountChange: (value: string) => void;
  onPublicPremisesPurposeChange: (value: string[] | null) => void;
}

const Stilobaty: React.FC<StilobatyProps> = ({
  stilobatCount,
  stilobatCalculated,
  stilobatFloors,
  stilobatAvgArea,
  stilobatAvgHeight,
  stilobatTotalArea,
  stilobatGnsArea,
  stilobatVolume,
  stilobatStairs,
  stilobatSmokelessStairs,
  stilobatLifts,
  hasGarbageChute,
  publicPremisesCount,
  publicPremisesPurpose,
  onStilobatCalculatedChange,
  onStilobatFloorsChange,
  onStilobatAvgAreaChange,
  onStilobatAvgHeightChange,
  onStilobatTotalAreaChange,
  onStilobatGnsAreaChange,
  onStilobatVolumeChange,
  onStilobatStairsChange,
  onStilobatSmokelessStairsChange,
  onStilobatLiftsChange,
  onHasGarbageChuteChange,
  onPublicPremisesCountChange,
  onPublicPremisesPurposeChange,
}) => {
  const handleStilobatCalculatedChange = (index: number, checked: boolean) => {
    const newCalculated = [...stilobatCalculated];
    newCalculated[index] = checked;
    onStilobatCalculatedChange(newCalculated);
  };

  const handleStilobatFloorsChange = (index: number, value: string) => {
    const newFloors = [...stilobatFloors];
    newFloors[index] = value;
    onStilobatFloorsChange(newFloors);
  };

  const handleStilobatAvgAreaChange = (index: number, value: string) => {
    const newAvgArea = [...stilobatAvgArea];
    newAvgArea[index] = value;
    onStilobatAvgAreaChange(newAvgArea);
  };

  const handleStilobatAvgHeightChange = (index: number, value: string) => {
    const newAvgHeight = [...stilobatAvgHeight];
    newAvgHeight[index] = value;
    onStilobatAvgHeightChange(newAvgHeight);
  };

  const handleStilobatTotalAreaChange = (index: number, value: string) => {
    const newTotalArea = [...stilobatTotalArea];
    newTotalArea[index] = value;
    onStilobatTotalAreaChange(newTotalArea);
  };

  const handleStilobatGnsAreaChange = (index: number, value: string) => {
    const newGnsArea = [...stilobatGnsArea];
    newGnsArea[index] = value;
    onStilobatGnsAreaChange(newGnsArea);
  };

  const handleStilobatVolumeChange = (index: number, value: string) => {
    const newVolume = [...stilobatVolume];
    newVolume[index] = value;
    onStilobatVolumeChange(newVolume);
  };

  const handleStilobatStairsChange = (index: number, value: string) => {
    const newStairs = [...stilobatStairs];
    newStairs[index] = value;
    onStilobatStairsChange(newStairs);
  };

  const handleStilobatSmokelessStairsChange = (index: number, value: string) => {
    const newSmokelessStairs = [...stilobatSmokelessStairs];
    newSmokelessStairs[index] = value;
    onStilobatSmokelessStairsChange(newSmokelessStairs);
  };

  const handleStilobatLiftsChange = (index: number, value: string) => {
    const newLifts = [...stilobatLifts];
    newLifts[index] = value;
    onStilobatLiftsChange(newLifts);
  };

  const elements = [];
  for (let i = 0; i < stilobatCount; i++) {
    elements.push(
      <div key={`stilobat-container-${i}`} className={styles.stilobatContainer}>
        <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left' }}>
          Стилобат {i + 1}
        </h2>
        <CheckboxTrue 
          key={`stilobat-calculated-${i}`}
          checked={stilobatCalculated[i] || false}
          onChange={(checked: boolean) => handleStilobatCalculatedChange(i, checked)}
          label="Расчетные данные"
        />
        <NumberField 
          key={`stilobat-floors-${i}`}
          title="Количество этажей"
          value={stilobatFloors[i] || ''}
          onChange={(value: string) => handleStilobatFloorsChange(i, value)}
          placeholder="1"
        />
        <NumberField 
          key={`stilobat-avg-area-${i}`}
          title="Средняя площадь этажа в м²"
          value={stilobatAvgArea[i] || ''}
          onChange={(value: string) => handleStilobatAvgAreaChange(i, value)}
          placeholder="1"
        />
        <NumberField 
          key={`stilobat-avg-height-${i}`}
          title="Средняя высота этажа в м"
          value={stilobatAvgHeight[i] || ''}
          onChange={(value: string) => handleStilobatAvgHeightChange(i, value)}
          placeholder="1"
        />
        <NumberField 
          key={`stilobat-total-area-${i}`}
          title="Общая площадь в м²"
          value={stilobatTotalArea[i] || ''}
          onChange={(value: string) => handleStilobatTotalAreaChange(i, value)}
          placeholder="1"
          disabled
        />
        <NumberField 
          key={`stilobat-gns-area-${i}`}
          title="Площадь ГНС в м²"
          value={stilobatGnsArea[i] || ''}
          onChange={(value: string) => handleStilobatGnsAreaChange(i, value)}
          placeholder="1"
          disabled
        />
        <NumberField 
          key={`stilobat-volume-${i}`}
          title="Строительный объем в м³"
          value={stilobatVolume[i] || ''}
          onChange={(value: string) => handleStilobatVolumeChange(i, value)}
          placeholder="1"
          disabled
        />
        <NumberField 
          key={`stilobat-stairs-${i}`}
          title="Количество лестничных клеток"
          value={stilobatStairs[i] || ''}
          onChange={(value: string) => handleStilobatStairsChange(i, value)}
          placeholder="1"
          disabled
        />
        <NumberField 
          key={`stilobat-smokeless-stairs-${i}`}
          title="Количество незадымляемых лестничных клеток"
          value={stilobatSmokelessStairs[i] || ''}
          onChange={(value: string) => handleStilobatSmokelessStairsChange(i, value)}
          placeholder="1"
          disabled
        />
        <NumberField 
          key={`stilobat-lifts-${i}`}
          title="Количество лифтов"
          value={stilobatLifts[i] || ''}
          onChange={(value: string) => handleStilobatLiftsChange(i, value)}
          placeholder="1"
          disabled
        />
      </div>
    );
    
    if (stilobatCount % 2 !== 0 && i === stilobatCount - 1) {
      elements.push(<div key={`stilobat-empty-${i}`}></div>);
    }
  }

  // Выносим общий блок вопросов за пределы цикла
  if (stilobatCount > 0) {
    elements.push(
      <div key="final-stillobat-question" className={styles.finalCorpusQuestion} style={{ gridColumn: 'span 2' }}>
        <div className={styles.leftPart}>
          <CheckboxField
            key="atrium"
            title="Атриум" 
            value={hasGarbageChute} 
            onChange={onHasGarbageChuteChange} 
            inline={true}
          />

          <CheckboxField
            key="light-lantern"
            title="Световой фонарь" 
            value={hasGarbageChute} 
            onChange={onHasGarbageChuteChange} 
            inline={true}
          />

          <div key="public-premises-count">
            <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left', fontSize: '20px' }}>Количество общественных помещений</h2>
            <Input 
              type="number" 
              placeholder="Например: 2" 
              className={styles.inputFieldClassic}
              value={publicPremisesCount}
              onChange={(e: { target: { value: string; }; }) => onPublicPremisesCountChange(e.target.value)}
            />
          </div>
        </div>

        <div className={styles.rightPart}>
          <div key="escalators-count">
            <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left', fontSize: '20px', marginBlockStart: 0 }}>Количество эскалаторов / траволаторов</h2>
            <Input 
              type="number" 
              placeholder="Например: 2" 
              className={styles.inputFieldClassic}
              value={publicPremisesCount}
              onChange={(e: { target: { value: string; }; }) => onPublicPremisesCountChange(e.target.value)}
            />
          </div>

          <Select
            key="public-premises-purpose"
            title="Назначение общественных помещений"
            options={[]}
            value={publicPremisesPurpose}
            onChange={onPublicPremisesPurposeChange}
            placeholder="Выберите нужное значение"
            multiple
          />
        </div>
      </div>
    );
  }

  return <>{elements}</>;
};

export default Stilobaty;