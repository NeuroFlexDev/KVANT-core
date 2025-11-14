import React from 'react';
import styles from '../mainArchitecture.module.css';
import NumberField from '../../../ElementUi/NumberField/NumberField';
import { CheckboxTrue } from '../../../ElementUi/CheckboxTrue/Checkbox';
import CheckboxField from '../../../ElementUi/Checkbox/CheckboxField';
import Input from '../../../ElementUi/Input/Input';
import Select from '../../../ElementUi/Select/Select';

interface BuildingsProps {
  buildingCount: number;
  sectionsCounts: number[];
  sectionCalculated: boolean[][];
  sectionAreas: string[][];
  sectionFloors: string[][];
  sectionFirstFloorHeight: string[][];
  sectionTypicalFloorHeight: string[][];
  sectionTotalArea: string[][];
  sectionGnsArea: string[][];
  sectionVolume: string[][];
  sectionFireHeight: string[][];
  sectionStaircases: string[][];
  sectionSmokelessStaircases: string[][];
  sectionElevators: string[][];
  hasTechFloor: boolean;
  hasBasement: boolean;
  hasTechAttic: boolean;
  hasGarbageChute: boolean;
  publicPremisesCount: string;
  totalPublicArea: string;
  hasQuartergraphy: boolean;
  totalApartmentArea: string;
  oneRoomCount: string;
  twoRoomCount: string;
  threeRoomCount: string;
  fourRoomCount: string;
  moreThanFourRoomCount: string;
  penthouseCount: string;
  studioCount: string;
  hasExploitedRoof: boolean;
  publicPremisesPurpose: string[] | null;
  onSectionCountChange: (index: number, value: number) => void;
  onSectionCalculatedChange: (value: boolean[][]) => void;
  onSectionAreasChange: (value: string[][]) => void;
  onSectionFloorsChange: (value: string[][]) => void;
  onSectionFirstFloorHeightChange: (value: string[][]) => void;
  onSectionTypicalFloorHeightChange: (value: string[][]) => void;
  onSectionTotalAreaChange: (value: string[][]) => void;
  onSectionGnsAreaChange: (value: string[][]) => void;
  onSectionVolumeChange: (value: string[][]) => void;
  onSectionFireHeightChange: (value: string[][]) => void;
  onSectionStaircasesChange: (value: string[][]) => void;
  onSectionSmokelessStaircasesChange: (value: string[][]) => void;
  onSectionElevatorsChange: (value: string[][]) => void;
  onHasTechFloorChange: (value: boolean) => void;
  onHasBasementChange: (value: boolean) => void;
  onHasTechAtticChange: (value: boolean) => void;
  onHasGarbageChuteChange: (value: boolean) => void;
  onPublicPremisesCountChange: (value: string) => void;
  onTotalPublicAreaChange: (value: string) => void;
  onHasQuartergraphyChange: (value: boolean) => void;
  onTotalApartmentAreaChange: (value: string) => void;
  onOneRoomCountChange: (value: string) => void;
  onTwoRoomCountChange: (value: string) => void;
  onThreeRoomCountChange: (value: string) => void;
  onFourRoomCountChange: (value: string) => void;
  onMoreThanFourRoomCountChange: (value: string) => void;
  onPenthouseCountChange: (value: string) => void;
  onStudioCountChange: (value: string) => void;
  onHasExploitedRoofChange: (value: boolean) => void;
  onPublicPremisesPurposeChange: (value: string[] | null) => void;
}

const Buildings: React.FC<BuildingsProps> = ({
  buildingCount,
  sectionsCounts,
  sectionCalculated,
  sectionAreas,
  sectionFloors,
  sectionFirstFloorHeight,
  sectionTypicalFloorHeight,
  sectionTotalArea,
  sectionGnsArea,
  sectionVolume,
  sectionFireHeight,
  sectionStaircases,
  sectionSmokelessStaircases,
  sectionElevators,
  hasTechFloor,
  hasBasement,
  hasTechAttic,
  hasGarbageChute,
  publicPremisesCount,
  totalPublicArea,
  hasQuartergraphy,
  totalApartmentArea,
  oneRoomCount,
  twoRoomCount,
  threeRoomCount,
  fourRoomCount,
  moreThanFourRoomCount,
  penthouseCount,
  studioCount,
  hasExploitedRoof,
  publicPremisesPurpose,
  onSectionCountChange,
  onSectionCalculatedChange,
  onSectionAreasChange,
  onSectionFloorsChange,
  onSectionFirstFloorHeightChange,
  onSectionTypicalFloorHeightChange,
  onSectionTotalAreaChange,
  onSectionGnsAreaChange,
  onSectionVolumeChange,
  onSectionFireHeightChange,
  onSectionStaircasesChange,
  onSectionSmokelessStaircasesChange,
  onSectionElevatorsChange,
  onHasTechFloorChange,
  onHasBasementChange,
  onHasTechAtticChange,
  onHasGarbageChuteChange,
  onPublicPremisesCountChange,
  onTotalPublicAreaChange,
  onHasQuartergraphyChange,
  onTotalApartmentAreaChange,
  onOneRoomCountChange,
  onTwoRoomCountChange,
  onThreeRoomCountChange,
  onFourRoomCountChange,
  onMoreThanFourRoomCountChange,
  onPenthouseCountChange,
  onStudioCountChange,
  onHasExploitedRoofChange,
  onPublicPremisesPurposeChange,
}) => {
  const handleSectionCalculatedChange = (buildingIndex: number, sectionIndex: number, checked: boolean) => {
    const newCalculated = [...sectionCalculated];
    if (!newCalculated[buildingIndex]) newCalculated[buildingIndex] = [];
    newCalculated[buildingIndex][sectionIndex] = checked;
    onSectionCalculatedChange(newCalculated);
  };

  const handleSectionAreasChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newAreas = [...sectionAreas];
    if (!newAreas[buildingIndex]) newAreas[buildingIndex] = [];
    newAreas[buildingIndex][sectionIndex] = value;
    onSectionAreasChange(newAreas);
  };

  const handleSectionFloorsChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newFloors = [...sectionFloors];
    if (!newFloors[buildingIndex]) newFloors[buildingIndex] = [];
    newFloors[buildingIndex][sectionIndex] = value;
    onSectionFloorsChange(newFloors);
  };

  const handleSectionFirstFloorHeightChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newFirstFloorHeight = [...sectionFirstFloorHeight];
    if (!newFirstFloorHeight[buildingIndex]) newFirstFloorHeight[buildingIndex] = [];
    newFirstFloorHeight[buildingIndex][sectionIndex] = value;
    onSectionFirstFloorHeightChange(newFirstFloorHeight);
  };

  const handleSectionTypicalFloorHeightChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newTypicalFloorHeight = [...sectionTypicalFloorHeight];
    if (!newTypicalFloorHeight[buildingIndex]) newTypicalFloorHeight[buildingIndex] = [];
    newTypicalFloorHeight[buildingIndex][sectionIndex] = value;
    onSectionTypicalFloorHeightChange(newTypicalFloorHeight);
  };

  const handleSectionTotalAreaChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newTotalArea = [...sectionTotalArea];
    if (!newTotalArea[buildingIndex]) newTotalArea[buildingIndex] = [];
    newTotalArea[buildingIndex][sectionIndex] = value;
    onSectionTotalAreaChange(newTotalArea);
  };

  const handleSectionGnsAreaChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newGnsArea = [...sectionGnsArea];
    if (!newGnsArea[buildingIndex]) newGnsArea[buildingIndex] = [];
    newGnsArea[buildingIndex][sectionIndex] = value;
    onSectionGnsAreaChange(newGnsArea);
  };

  const handleSectionVolumeChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newVolume = [...sectionVolume];
    if (!newVolume[buildingIndex]) newVolume[buildingIndex] = [];
    newVolume[buildingIndex][sectionIndex] = value;
    onSectionVolumeChange(newVolume);
  };

  const handleSectionFireHeightChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newFireHeight = [...sectionFireHeight];
    if (!newFireHeight[buildingIndex]) newFireHeight[buildingIndex] = [];
    newFireHeight[buildingIndex][sectionIndex] = value;
    onSectionFireHeightChange(newFireHeight);
  };

  const handleSectionStaircasesChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newStaircases = [...sectionStaircases];
    if (!newStaircases[buildingIndex]) newStaircases[buildingIndex] = [];
    newStaircases[buildingIndex][sectionIndex] = value;
    onSectionStaircasesChange(newStaircases);
  };

  const handleSectionSmokelessStaircasesChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newSmokelessStaircases = [...sectionSmokelessStaircases];
    if (!newSmokelessStaircases[buildingIndex]) newSmokelessStaircases[buildingIndex] = [];
    newSmokelessStaircases[buildingIndex][sectionIndex] = value;
    onSectionSmokelessStaircasesChange(newSmokelessStaircases);
  };

  const handleSectionElevatorsChange = (buildingIndex: number, sectionIndex: number, value: string) => {
    const newElevators = [...sectionElevators];
    if (!newElevators[buildingIndex]) newElevators[buildingIndex] = [];
    newElevators[buildingIndex][sectionIndex] = value;
    onSectionElevatorsChange(newElevators);
  };

  const elements = [];
    
  elements.push(
    <div key="tech-checkboxes-row" className={styles.techCheckboxRow}>
      <CheckboxField
        key="tech-floor"
        title="Технический этаж" 
        value={hasTechFloor} 
        onChange={onHasTechFloorChange} 
        inline={true}
      />
      <CheckboxField
        key="basement"
        title="Цокольный этаж" 
        value={hasBasement} 
        onChange={onHasBasementChange} 
        inline={true}
      />
    </div>
  );

  elements.push(
    <CheckboxField
      key="tech-attic"
      title="Технический чердак или техническое пространство" 
      value={hasTechAttic} 
      onChange={onHasTechAtticChange} 
    />
  );

  for (let i = 0; i < buildingCount; i++) {
    elements.push(
      <div key={`building-container-${i}`} className={styles.buildingContainer}>
        <h1 style={{ textAlign: 'left' }} className={styles.title}>
          Корпус {i + 1}
        </h1>
        
        <NumberField 
          key={`sections-count-${i}`}
          title="Количество секций"
          value={String(sectionsCounts[i] || 0)}
          onChange={(value: string) => onSectionCountChange(i, parseInt(value) || 0)}
          placeholder="1"
        />

        {sectionsCounts[i] > 0 && (
          <div className={styles.sectionsGrid}>
            {Array.from({ length: sectionsCounts[i] }, (_, j) => (
              <div key={`section-container-${i}-${j}`} className={styles.sectionContainer}>
                <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left' }}>
                  Секция {j + 1}
                </h2>
                <CheckboxTrue 
                  key={`section-calculated-${i}-${j}`}
                  checked={sectionCalculated[i]?.[j] || false}
                  onChange={(checked: boolean) => handleSectionCalculatedChange(i, j, checked)}
                  label="Расчетные данные"
                />
                <NumberField 
                  key={`section-areas-${i}-${j}`}
                  title="Площадь этажа в м²"
                  value={sectionAreas[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionAreasChange(i, j, value)}
                />
                <NumberField 
                  key={`section-floors-${i}-${j}`}
                  title="Количество этажей секции (без учета стилобата/с учетом)"
                  value={sectionFloors[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionFloorsChange(i, j, value)}
                />
                <NumberField 
                  key={`section-first-floor-height-${i}-${j}`}
                  title="Высота первого этажа в м"
                  value={sectionFirstFloorHeight[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionFirstFloorHeightChange(i, j, value)}
                />
                <NumberField 
                  key={`section-typical-floor-height-${i}-${j}`}
                  title="Высота типового этажа в м"
                  value={sectionTypicalFloorHeight[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionTypicalFloorHeightChange(i, j, value)}
                />
                <NumberField 
                  key={`section-total-area-${i}-${j}`}
                  title="Общая площадь в м²"
                  value={sectionTotalArea[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionTotalAreaChange(i, j, value)}
                  disabled
                />
                <NumberField 
                  key={`section-gns-area-${i}-${j}`}
                  title="Площадь ГНС в м²"
                  value={sectionGnsArea[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionGnsAreaChange(i, j, value)}
                  disabled
                />
                <NumberField 
                  key={`section-volume-${i}-${j}`}
                  title="Строительный объем в м³"
                  value={sectionVolume[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionVolumeChange(i, j, value)}
                  disabled
                />
                <NumberField 
                  key={`section-fire-height-${i}-${j}`}
                  title="Пожарно-техническая высота в м"
                  value={sectionFireHeight[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionFireHeightChange(i, j, value)}
                  disabled
                />
                <NumberField 
                  key={`section-staircases-${i}-${j}`}
                  title="Количество лестничных клеток"
                  value={sectionStaircases[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionStaircasesChange(i, j, value)}
                  disabled
                />
                <NumberField 
                  key={`section-smokeless-staircases-${i}-${j}`}
                  title="Количество незадымляемых лестничных клеток"
                  value={sectionSmokelessStaircases[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionSmokelessStaircasesChange(i, j, value)}
                  disabled
                />
                <NumberField 
                  key={`section-elevators-${i}-${j}`}
                  title="Количество лифтов"
                  value={sectionElevators[i]?.[j] || ''}
                  placeholder='1'
                  onChange={(value: string) => handleSectionElevatorsChange(i, j, value)}
                  disabled
                />
              </div>
            ))}
            {sectionsCounts[i] % 2 !== 0 && <div key={`section-empty-${i}`}></div>}
          </div>
        )}
      </div>
    );
  }

  elements.push(
    <div key="final-corpus-question" className={styles.finalCorpusQuestion} style={{ gridColumn: 'span 2' }}>
      <div className={styles.leftPart}>
        <CheckboxField
          key="garbage-chute"
          title="Наличие мусоропровода" 
          value={hasGarbageChute} 
          onChange={onHasGarbageChuteChange} 
          inline={true}
        />

        <div key="public-premises-count">
          <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left', fontSize: '20px' }}>Количество встроенных общественных помещений в корпусах</h2>
          <Input 
            type="number" 
            placeholder="Например: 2" 
            className={styles.inputFieldClassic}
            value={publicPremisesCount}
            onChange={(e: { target: { value: string; }; }) => onPublicPremisesCountChange(e.target.value)}
          />
        </div>

        <div key="total-public-area">
          <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left', fontSize: '20px' }}>Суммарная площадь общественных помещений</h2>
          <Input 
            type="number" 
            placeholder="Например: 2" 
            className={styles.inputFieldClassic}
            value={totalPublicArea}
            onChange={(e: { target: { value: string; }; }) => onTotalPublicAreaChange(e.target.value)}
          />
        </div>

        <CheckboxField
          key="quartergraphy"
          title="Наличие сведений по квартирографии" 
          value={hasQuartergraphy} 
          onChange={onHasQuartergraphyChange} 
          inline={false}
        />

        <div key="total-apartment-area">
          <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left', fontSize: '20px' }}>Общая площадь квартир</h2>
          <Input 
            type="number" 
            placeholder="Например: 2" 
            className={styles.inputFieldClassic}
            value={totalApartmentArea}
            onChange={(e: { target: { value: string; }; }) => onTotalApartmentAreaChange(e.target.value)}
          />
        </div>

        <NumberField 
          key="one-room-count"
          title="Количество 1-комнатных квартир"
          value={oneRoomCount}
          placeholder='1'
          onChange={onOneRoomCountChange}
        />
        <NumberField 
          key="three-room-count"
          title="Количество 3-комнатных квартир"
          value={threeRoomCount}
          placeholder='1'
          onChange={onThreeRoomCountChange}
        />
        <NumberField 
          key="more-than-four-room-count"
          title="Количество квартир с более 4-комнат"
          value={moreThanFourRoomCount}
          placeholder='1'
          onChange={onMoreThanFourRoomCountChange}
        />
        <NumberField 
          key="penthouse-count"
          title="Количество пентхаусов"
          value={penthouseCount}
          placeholder='1'
          onChange={onPenthouseCountChange}
        />
      </div>

      <div className={styles.rightPart}>
        <CheckboxField
          key="exploited-roof"
          title="Наличие эксплуатируемой кровли" 
          value={hasExploitedRoof} 
          onChange={onHasExploitedRoofChange} 
          inline={true}
        />

        <Select
          key="public-premises-purpose"
          title="Назначение встроенных общественных помещений в корпусах"
          options={[]}
          value={publicPremisesPurpose}
          onChange={onPublicPremisesPurposeChange}
          placeholder="Выберите нужное значение"
          multiple
        />

        <NumberField 
          key="two-room-count"
          title="Количество 2-комнатных квартир"
          value={twoRoomCount}
          placeholder='1'
          onChange={onTwoRoomCountChange}
        />
        <NumberField 
          key="four-room-count"
          title="Количество 4-комнатных квартир"
          value={fourRoomCount}
          placeholder='1'
          onChange={onFourRoomCountChange}
        />
        <NumberField 
          key="studio-count"
          title="Количество студий"
          value={studioCount}
          placeholder='1'
          onChange={onStudioCountChange}
        />
      </div>
    </div>
  );

  return <>{elements}</>;
};

export default Buildings;