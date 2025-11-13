import React, { useState, useEffect, useRef } from 'react';
import styles from './mainArchitecture.module.css';
import Input from '../../ElementUi/Input/Input';
import Select from '../../ElementUi/Select/Select';
import NumberFieldsGrid from '../../ElementUi/NumberFieldsGrid/NumberFieldsGrid';
import NumberField from '../../ElementUi/NumberField/NumberField';
import { CheckboxTrue } from '../../ElementUi/CheckboxTrue/Checkbox';
import CheckboxField from '../../ElementUi/Checkbox/CheckboxField';
import Slider from '../../ElementUi/Slider/Slider';
import { useFormSection } from '../../../contexts/FormContext';

interface ArchitectureFormData extends Record<string, unknown> {
  areaValue: string;
  selectedIndex: string[] | null;
  buildingCount: number;
  stilobatCount: number;
  annexCount: number;
  hasTechFloor: boolean;
  hasTechAttic: boolean;
  hasBasement: boolean;
  stilobatCalculated: boolean[];
  stilobatFloors: string[];
  stilobatAvgArea: string[];
  stilobatAvgHeight: string[];
  stilobatTotalArea: string[];
  stilobatGnsArea: string[];
  stilobatVolume: string[];
  annexCalculated: boolean[];
  annexFloors: string[];
  annexArea: string[];
  annexHeight: string[];
  annexTotalArea: string[];
  annexGnsArea: string[];
  annexVolume: string[];
  annexStairs: string[];
  sectionsCounts: number[];
  sectionCalculated: boolean[][];
  sectionAreas: string[][];
  undergroundCalculated: boolean;
  undergroundFloors: string;
  undergroundAvgArea: string;
  undergroundAvgHeight: string;
  undergroundStorageArea: string;
  undergroundTotalArea: string;
  hasUndergroundParking: boolean;
  objectCalculated: boolean;
  calculatedStairs: string;
  calculatedElevators: string;
  calculatedStaircases: string;
  calculatedPublicArea: string;
  calculatedPublicPurpose: string;
  calculatedPublicCount: string;
  calculatedAbovegroundVolume: string;
  calculatedResidents: string;
  calculatedUndergroundVolume: string;
  calculatedTotalArea: string;
  calculatedTotalVolume: string;
  calculatedResidentsCount: string;
}

const defaultArchitectureData: ArchitectureFormData = {
  areaValue: '',
  selectedIndex: null,
  buildingCount: 0,
  stilobatCount: 0,
  annexCount: 0,
  hasTechFloor: false,
  hasTechAttic: false,
  hasBasement: false,
  stilobatCalculated: [],
  stilobatFloors: [],
  stilobatAvgArea: [],
  stilobatAvgHeight: [],
  stilobatTotalArea: [],
  stilobatGnsArea: [],
  stilobatVolume: [],
  annexCalculated: [],
  annexFloors: [],
  annexArea: [],
  annexHeight: [],
  annexTotalArea: [],
  annexGnsArea: [],
  annexVolume: [],
  annexStairs: [],
  sectionsCounts: [],
  sectionCalculated: [],
  sectionAreas: [],
  undergroundCalculated: false,
  undergroundFloors: '',
  undergroundAvgArea: '',
  undergroundAvgHeight: '',
  undergroundStorageArea: '',
  undergroundTotalArea: '',
  hasUndergroundParking: false,
  objectCalculated: false,
  calculatedStairs: '',
  calculatedElevators: '',
  calculatedStaircases: '',
  calculatedPublicArea: '',
  calculatedPublicPurpose: '',
  calculatedPublicCount: '',
  calculatedAbovegroundVolume: '',
  calculatedResidents: '',
  calculatedUndergroundVolume: '',
  calculatedTotalArea: '',
  calculatedTotalVolume: '',
  calculatedResidentsCount: '',
};

export default function MainArchitecture() {
  const { data, setData } = useFormSection<ArchitectureFormData>('architecture', defaultArchitectureData);
  const isHydrated = useRef(false);
  const [areaValue, setAreaValue] = useState<string>('');
  const [selectedIndex, setSelectedIndex] = useState<string[] | null>(null);
  const [buildingCount, setBuildingCount] = useState(0);
  const [stilobatCount, setStilobatCount] = useState(0);
  const [annexCount, setAnnexCount] = useState(0);
  const [hasTechFloor, setHasTechFloor] = useState(false);
  const [hasTechAttic, setHasTechAttic] = useState(false);
  const [hasBasement, setHasBasement] = useState(false);
  
  // Состояния для стилобатов
  const [stilobatCalculated, setStilobatCalculated] = useState<boolean[]>([]);
  const [stilobatFloors, setStilobatFloors] = useState<string[]>([]);
  const [stilobatAvgArea, setStilobatAvgArea] = useState<string[]>([]);
  const [stilobatAvgHeight, setStilobatAvgHeight] = useState<string[]>([]);
  const [stilobatTotalArea, setStilobatTotalArea] = useState<string[]>([]);
  const [stilobatGnsArea, setStilobatGnsArea] = useState<string[]>([]);
  const [stilobatVolume, setStilobatVolume] = useState<string[]>([]);
  
  // Состояния для пристроек
  const [annexCalculated, setAnnexCalculated] = useState<boolean[]>([]);
  const [annexFloors, setAnnexFloors] = useState<string[]>([]);
  const [annexArea, setAnnexArea] = useState<string[]>([]);
  const [annexHeight, setAnnexHeight] = useState<string[]>([]);
  const [annexTotalArea, setAnnexTotalArea] = useState<string[]>([]);
  const [annexGnsArea, setAnnexGnsArea] = useState<string[]>([]);
  const [annexVolume, setAnnexVolume] = useState<string[]>([]);
  const [annexStairs, setAnnexStairs] = useState<string[]>([]);
  
  // Состояния для корпусов
  const [sectionsCounts, setSectionsCounts] = useState<number[]>([]);
  const [sectionCalculated, setSectionCalculated] = useState<boolean[][]>([]);
  const [sectionAreas, setSectionAreas] = useState<string[][]>([]);
  
  // Состояния для подземной части
  const [undergroundCalculated, setUndergroundCalculated] = useState(false);
  const [undergroundFloors, setUndergroundFloors] = useState('');
  const [undergroundAvgArea, setUndergroundAvgArea] = useState('');
  const [undergroundAvgHeight, setUndergroundAvgHeight] = useState('');
  const [undergroundStorageArea, setUndergroundStorageArea] = useState('');
  const [undergroundTotalArea, setUndergroundTotalArea] = useState('');
  const [hasUndergroundParking, setHasUndergroundParking] = useState(false);
  
  // Состояния для расчетных данных
  const [objectCalculated, setObjectCalculated] = useState(false);
  const [calculatedStairs, setCalculatedStairs] = useState('');
  const [calculatedElevators, setCalculatedElevators] = useState('');
  const [calculatedStaircases, setCalculatedStaircases] = useState('');
  const [calculatedPublicArea, setCalculatedPublicArea] = useState('');
  const [calculatedPublicPurpose, setCalculatedPublicPurpose] = useState('');
  const [calculatedPublicCount, setCalculatedPublicCount] = useState('');
  const [calculatedAbovegroundVolume, setCalculatedAbovegroundVolume] = useState('');
  const [calculatedResidents, setCalculatedResidents] = useState('');
  const [calculatedUndergroundVolume, setCalculatedUndergroundVolume] = useState('');
  const [calculatedTotalArea, setCalculatedTotalArea] = useState('');
  const [calculatedTotalVolume, setCalculatedTotalVolume] = useState('');
  const [calculatedResidentsCount, setCalculatedResidentsCount] = useState('');

  // Инициализация массивов при изменении количества
  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }
    setStilobatCalculated(Array(stilobatCount).fill(false));
    setStilobatFloors(Array(stilobatCount).fill(''));
    setStilobatAvgArea(Array(stilobatCount).fill(''));
    setStilobatAvgHeight(Array(stilobatCount).fill(''));
    setStilobatTotalArea(Array(stilobatCount).fill(''));
    setStilobatGnsArea(Array(stilobatCount).fill(''));
    setStilobatVolume(Array(stilobatCount).fill(''));
  }, [stilobatCount]);

  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }
    setAnnexCalculated(Array(annexCount).fill(false));
    setAnnexFloors(Array(annexCount).fill(''));
    setAnnexArea(Array(annexCount).fill(''));
    setAnnexHeight(Array(annexCount).fill(''));
    setAnnexTotalArea(Array(annexCount).fill(''));
    setAnnexGnsArea(Array(annexCount).fill(''));
    setAnnexVolume(Array(annexCount).fill(''));
    setAnnexStairs(Array(annexCount).fill(''));
  }, [annexCount]);

  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }
    const newSectionsCounts = Array(buildingCount).fill(0);
    const newSectionCalculated = Array(buildingCount).fill([]).map(() => []);
    const newSectionAreas = Array(buildingCount).fill([]).map(() => []);
    
    setSectionsCounts(newSectionsCounts);
    setSectionCalculated(newSectionCalculated);
    setSectionAreas(newSectionAreas);
  }, [buildingCount]);

  useEffect(() => {
    if (isHydrated.current) {
      return;
    }

    setAreaValue(data.areaValue ?? '');
    setSelectedIndex(data.selectedIndex ?? null);
    setBuildingCount(data.buildingCount ?? 0);
    setStilobatCount(data.stilobatCount ?? 0);
    setAnnexCount(data.annexCount ?? 0);
    setHasTechFloor(Boolean(data.hasTechFloor));
    setHasTechAttic(Boolean(data.hasTechAttic));
    setHasBasement(Boolean(data.hasBasement));

    setStilobatCalculated(Array.isArray(data.stilobatCalculated) ? [...data.stilobatCalculated] : []);
    setStilobatFloors(Array.isArray(data.stilobatFloors) ? [...data.stilobatFloors] : []);
    setStilobatAvgArea(Array.isArray(data.stilobatAvgArea) ? [...data.stilobatAvgArea] : []);
    setStilobatAvgHeight(Array.isArray(data.stilobatAvgHeight) ? [...data.stilobatAvgHeight] : []);
    setStilobatTotalArea(Array.isArray(data.stilobatTotalArea) ? [...data.stilobatTotalArea] : []);
    setStilobatGnsArea(Array.isArray(data.stilobatGnsArea) ? [...data.stilobatGnsArea] : []);
    setStilobatVolume(Array.isArray(data.stilobatVolume) ? [...data.stilobatVolume] : []);

    setAnnexCalculated(Array.isArray(data.annexCalculated) ? [...data.annexCalculated] : []);
    setAnnexFloors(Array.isArray(data.annexFloors) ? [...data.annexFloors] : []);
    setAnnexArea(Array.isArray(data.annexArea) ? [...data.annexArea] : []);
    setAnnexHeight(Array.isArray(data.annexHeight) ? [...data.annexHeight] : []);
    setAnnexTotalArea(Array.isArray(data.annexTotalArea) ? [...data.annexTotalArea] : []);
    setAnnexGnsArea(Array.isArray(data.annexGnsArea) ? [...data.annexGnsArea] : []);
    setAnnexVolume(Array.isArray(data.annexVolume) ? [...data.annexVolume] : []);
    setAnnexStairs(Array.isArray(data.annexStairs) ? [...data.annexStairs] : []);

    setSectionsCounts(Array.isArray(data.sectionsCounts) ? [...data.sectionsCounts] : []);
    setSectionCalculated(
      Array.isArray(data.sectionCalculated)
        ? data.sectionCalculated.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );
    setSectionAreas(
      Array.isArray(data.sectionAreas)
        ? data.sectionAreas.map((row) => (Array.isArray(row) ? [...row] : []))
        : [],
    );

    setUndergroundCalculated(Boolean(data.undergroundCalculated));
    setUndergroundFloors(data.undergroundFloors ?? '');
    setUndergroundAvgArea(data.undergroundAvgArea ?? '');
    setUndergroundAvgHeight(data.undergroundAvgHeight ?? '');
    setUndergroundStorageArea(data.undergroundStorageArea ?? '');
    setUndergroundTotalArea(data.undergroundTotalArea ?? '');
    setHasUndergroundParking(Boolean(data.hasUndergroundParking));

    setObjectCalculated(Boolean(data.objectCalculated));
    setCalculatedStairs(data.calculatedStairs ?? '');
    setCalculatedElevators(data.calculatedElevators ?? '');
    setCalculatedStaircases(data.calculatedStaircases ?? '');
    setCalculatedPublicArea(data.calculatedPublicArea ?? '');
    setCalculatedPublicPurpose(data.calculatedPublicPurpose ?? '');
    setCalculatedPublicCount(data.calculatedPublicCount ?? '');
    setCalculatedAbovegroundVolume(data.calculatedAbovegroundVolume ?? '');
    setCalculatedResidents(data.calculatedResidents ?? '');
    setCalculatedUndergroundVolume(data.calculatedUndergroundVolume ?? '');
    setCalculatedTotalArea(data.calculatedTotalArea ?? '');
    setCalculatedTotalVolume(data.calculatedTotalVolume ?? '');
    setCalculatedResidentsCount(data.calculatedResidentsCount ?? '');

    isHydrated.current = true;
  }, [data]);

  useEffect(() => {
    if (!isHydrated.current) {
      return;
    }

    const payload: ArchitectureFormData = {
      areaValue,
      selectedIndex,
      buildingCount,
      stilobatCount,
      annexCount,
      hasTechFloor,
      hasTechAttic,
      hasBasement,
      stilobatCalculated,
      stilobatFloors,
      stilobatAvgArea,
      stilobatAvgHeight,
      stilobatTotalArea,
      stilobatGnsArea,
      stilobatVolume,
      annexCalculated,
      annexFloors,
      annexArea,
      annexHeight,
      annexTotalArea,
      annexGnsArea,
      annexVolume,
      annexStairs,
      sectionsCounts,
      sectionCalculated,
      sectionAreas,
      undergroundCalculated,
      undergroundFloors,
      undergroundAvgArea,
      undergroundAvgHeight,
      undergroundStorageArea,
      undergroundTotalArea,
      hasUndergroundParking,
      objectCalculated,
      calculatedStairs,
      calculatedElevators,
      calculatedStaircases,
      calculatedPublicArea,
      calculatedPublicPurpose,
      calculatedPublicCount,
      calculatedAbovegroundVolume,
      calculatedResidents,
      calculatedUndergroundVolume,
      calculatedTotalArea,
      calculatedTotalVolume,
      calculatedResidentsCount,
    };

    setData(payload);
  }, [
    areaValue,
    selectedIndex,
    buildingCount,
    stilobatCount,
    annexCount,
    hasTechFloor,
    hasTechAttic,
    hasBasement,
    stilobatCalculated,
    stilobatFloors,
    stilobatAvgArea,
    stilobatAvgHeight,
    stilobatTotalArea,
    stilobatGnsArea,
    stilobatVolume,
    annexCalculated,
    annexFloors,
    annexArea,
    annexHeight,
    annexTotalArea,
    annexGnsArea,
    annexVolume,
    annexStairs,
    sectionsCounts,
    sectionCalculated,
    sectionAreas,
    undergroundCalculated,
    undergroundFloors,
    undergroundAvgArea,
    undergroundAvgHeight,
    undergroundStorageArea,
    undergroundTotalArea,
    hasUndergroundParking,
    objectCalculated,
    calculatedStairs,
    calculatedElevators,
    calculatedStaircases,
    calculatedPublicArea,
    calculatedPublicPurpose,
    calculatedPublicCount,
    calculatedAbovegroundVolume,
    calculatedResidents,
    calculatedUndergroundVolume,
    calculatedTotalArea,
    calculatedTotalVolume,
    calculatedResidentsCount,
    setData,
  ]);

  const handleAreaChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setAreaValue(e.target.value);
  };

  const handleIndexChange = (value: string[] | null) => {
    setSelectedIndex(value);
  };

  const handleBuildingCountChange = (value: number) => {
    setBuildingCount(value);
  };

  const handleSectionCountChange = (index: number, value: number) => {
    const newSectionsCounts = [...sectionsCounts];
    newSectionsCounts[index] = value;
    setSectionsCounts(newSectionsCounts);
    
    const newSectionAreas = [...sectionAreas];
    newSectionAreas[index] = Array(value).fill('');
    setSectionAreas(newSectionAreas);
    
    const newSectionCalculated = [...sectionCalculated];
    newSectionCalculated[index] = Array(value).fill(false);
    setSectionCalculated(newSectionCalculated);
  };

  const materialOptionsA = [
    { value: '1', label: '1' },
    { value: '2', label: '2' },
    { value: '3', label: '3' },
    { value: '4', label: '4' },
    { value: '5', label: '5' },
    { value: '6', label: '6' },
    { value: '7', label: '7' },
    { value: '8', label: '8' },
    { value: '9', label: '9' },
    { value: '10', label: '10' },
    { value: '11', label: '11' },
    { value: '12', label: '12' },
  ];

  const renderStilobaty = () => {
    const elements = [];
    for (let i = 0; i < stilobatCount; i++) {
      elements.push(
        <div key={`stilobat-container-${i}`} className={styles.stilobatContainer}>
          <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left' }}>
            Стилобат {i + 1}
          </h2>
          <CheckboxTrue 
            checked={stilobatCalculated[i] || false}
            onChange={(checked) => {
              const newCalculated = [...stilobatCalculated];
              newCalculated[i] = checked;
              setStilobatCalculated(newCalculated);
            }}
            label="Расчетные данные"
          />
          <NumberField 
            title="Количество этажей"
            value={stilobatFloors[i] || ''}
            onChange={(value) => {
              const newFloors = [...stilobatFloors];
              newFloors[i] = value;
              setStilobatFloors(newFloors);
            }}
            placeholder="1"
          />
          <NumberField 
            title="Средняя площадь этажа в м²"
            value={stilobatAvgArea[i] || ''}
            onChange={(value) => {
              const newAvgArea = [...stilobatAvgArea];
              newAvgArea[i] = value;
              setStilobatAvgArea(newAvgArea);
            }}
            placeholder="1"
          />
          <NumberField 
            title="Средняя высота этажа в м"
            value={stilobatAvgHeight[i] || ''}
            onChange={(value) => {
              const newAvgHeight = [...stilobatAvgHeight];
              newAvgHeight[i] = value;
              setStilobatAvgHeight(newAvgHeight);
            }}
            placeholder="1"
          />
          <NumberField 
            title="Общая площадь в м²"
            value={stilobatTotalArea[i] || '1'}
            onChange={(value) => {
              const newTotalArea = [...stilobatTotalArea];
              newTotalArea[i] = value;
              setStilobatTotalArea(newTotalArea);
            }}
            placeholder="1"
            disabled
          />
          <NumberField 
            title="Площадь ГНС в м²"
            value={stilobatGnsArea[i] || '1'}
            onChange={(value) => {
              const newGnsArea = [...stilobatGnsArea];
              newGnsArea[i] = value;
              setStilobatGnsArea(newGnsArea);
            }}
            placeholder="1"
            disabled
          />
          <NumberField 
            title="Строительный объем в м³"
            value={stilobatVolume[i] || '1'}
            onChange={(value) => {
              const newVolume = [...stilobatVolume];
              newVolume[i] = value;
              setStilobatVolume(newVolume);
            }}
            placeholder="1"
            disabled
          />
        </div>
      );
      
      if (stilobatCount % 2 !== 0 && i === stilobatCount - 1) {
        elements.push(<div key={`stilobat-empty-${i}`}></div>);
      }
    }
    return elements;
  };

  const renderAnnexes = () => {
    const elements = [];
    for (let i = 0; i < annexCount; i++) {
      elements.push(
        <div key={`annex-container-${i}`} className={styles.annexContainer}>
          <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left' }}>
            Пристройка {i + 1}
          </h2>
          <CheckboxTrue 
            checked={annexCalculated[i] || false}
            onChange={(checked) => {
              const newCalculated = [...annexCalculated];
              newCalculated[i] = checked;
              setAnnexCalculated(newCalculated);
            }}
            label="Расчетные данные"
          />
          <NumberField 
            title="Количество этажей"
            value={annexFloors[i] || ''}
            onChange={(value) => {
              const newFloors = [...annexFloors];
              newFloors[i] = value;
              setAnnexFloors(newFloors);
            }}
            placeholder="1"
          />
          <NumberField 
            title="Площадь этажа в м²"
            value={annexArea[i] || ''}
            placeholder='1'
            onChange={(value) => {
              const newArea = [...annexArea];
              newArea[i] = value;
              setAnnexArea(newArea);
            }}
          />
          <NumberField 
            title="Средняя высота этажа в м"
            value={annexHeight[i] || ''}
            placeholder='1'
            onChange={(value) => {
              const newHeight = [...annexHeight];
              newHeight[i] = value;
              setAnnexHeight(newHeight);
            }}
          />
          <NumberField 
            title="Общая площадь в м²"
            value={annexTotalArea[i] || '1'}
            placeholder='1'
            onChange={(value) => {
              const newTotalArea = [...annexTotalArea];
              newTotalArea[i] = value;
              setAnnexTotalArea(newTotalArea);
            }}
            disabled
          />
          <NumberField 
            title="Площадь ГНС в м²"
            value={annexGnsArea[i] || '1'}
            placeholder='1'
            onChange={(value) => {
              const newGnsArea = [...annexGnsArea];
              newGnsArea[i] = value;
              setAnnexGnsArea(newGnsArea);
            }}
            disabled
          />
          <NumberField 
            title="Строительный объем в м³"
            value={annexVolume[i] || '1'}
            placeholder='1'
            onChange={(value) => {
              const newVolume = [...annexVolume];
              newVolume[i] = value;
              setAnnexVolume(newVolume);
            }}
            disabled
          />
          <NumberField 
            title="Количество лестничных клеток"
            value={annexStairs[i] || '1'}
            placeholder='1'
            onChange={(value) => {
              const newStairs = [...annexStairs];
              newStairs[i] = value;
              setAnnexStairs(newStairs);
            }}
            disabled
          />
        </div>
      );
      
      if (annexCount % 2 !== 0 && i === annexCount - 1) {
        elements.push(<div key={`annex-empty-${i}`}></div>);
      }
    }
    return elements;
  };

  const renderBuildings = () => {
    const elements = [];
    
    elements.push(
      <CheckboxField
        key="tech-floor"
        title="Технический этаж" 
        value={hasTechFloor} 
        onChange={setHasTechFloor} 
        inline={true}
      />
    );

    elements.push(
      <CheckboxField
        key="tech-attic"
        title="Технический чердак или техническое пространство" 
        value={hasTechAttic} 
        onChange={setHasTechAttic} 
      />
    );

    elements.push(
      <CheckboxField
        key="basement"
        title="Цокольный этаж" 
        value={hasBasement} 
        onChange={setHasBasement} 
        inline={true}
      />
    );

    elements.push(<div key="empty-1"></div>);

    for (let i = 0; i < buildingCount; i++) {
      elements.push(
        <h1 key={`building-title-${i}`} style={{ textAlign: 'left' }} className={styles.title}>
          Корпус {i + 1}
        </h1>
      );

      elements.push(<div key={`empty-building-${i}`}></div>);

      elements.push(
        <NumberField 
          key={`sections-count-${i}`}
          title="Количество секций"
          value={String(sectionsCounts[i]) || '0'}
          onChange={(value) => handleSectionCountChange(i, parseInt(value) || 0)}
          placeholder="1"
        />
      );

      elements.push(<div key={`empty-sections-${i}`}></div>);

      if (sectionsCounts[i] > 0) {
        for (let j = 0; j < sectionsCounts[i]; j++) {
          elements.push(
            <div key={`section-container-${i}-${j}`} className={styles.sectionContainer}>
              <h2 style={{ fontFamily: 'Montserrat', textAlign: 'left' }}>
                Секция {j + 1}
              </h2>
              <CheckboxTrue 
                checked={sectionCalculated[i]?.[j] || false}
                onChange={(checked) => {
                  const newCalculated = [...sectionCalculated];
                  if (!newCalculated[i]) newCalculated[i] = [];
                  newCalculated[i][j] = checked;
                  setSectionCalculated(newCalculated);
                }}
                label="Расчетные данные"
              />
              <NumberField 
                title="Площадь этажа в м²"
                value={sectionAreas[i]?.[j] || '1'}
                placeholder='1'
                onChange={(value) => {
                  const newAreas = [...sectionAreas];
                  if (!newAreas[i]) newAreas[i] = [];
                  newAreas[i][j] = value;
                  setSectionAreas(newAreas);
                }}
              />
            </div>
          );

          if (sectionsCounts[i] % 2 !== 0 && j === sectionsCounts[i] - 1) {
            elements.push(<div key={`section-empty-${i}-${j}`}></div>);
          }
        }
      }
    }

    return elements;
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Основные архитектурные решения</h1>
      <div className={styles.inputContainer}>
        <h2 style={{ fontFamily: 'Montserrat' }}>Площадь застройки в м²</h2>
        <Input 
          type="number" 
          placeholder="Например: 11303,0" 
          className={styles.inputFieldClassic}
          value={areaValue}
          onChange={handleAreaChange}
        />
      </div>

      <div className={styles.gridContainer}>
        <div className={styles.inputContainer}>
          <h2 style={{ fontFamily: 'Montserrat' }}>Количество корпусов в объекте капитального строительства</h2>
          <Input 
            type="number" 
            placeholder="Например: 2" 
            className={styles.inputFieldClassic}
            value={String(buildingCount)}
            onChange={(e) => handleBuildingCountChange(parseInt(e.target.value) || 0)}
          />
        </div>
        <Select 
          title='Корпуса, расположенные на подземной автостоянке'
          options={materialOptionsA}
          value={selectedIndex}
          onChange={handleIndexChange}
          placeholder="Выберите нужное значение"
          multiple={true}
          inlineOptions={true}
        />
        <div className={styles.inputContainer}>
          <h2 style={{ fontFamily: 'Montserrat' }}>Количество стилобатов</h2>
          <Input 
            type="number" 
            placeholder="Например: 2" 
            className={styles.inputFieldClassic}
            value={String(stilobatCount)}
            onChange={(e) => setStilobatCount(parseInt(e.target.value) || 0)}
          />
        </div>
        <Select 
          title='Корпуса, связанные с стилобатом'
          options={materialOptionsA}
          value={selectedIndex}
          onChange={handleIndexChange}
          placeholder="Выберите нужное значение"
          multiple={true}
          inlineOptions={true}
        />
        <div className={styles.inputContainer}>
          <h2 style={{ fontFamily: 'Montserrat' }}>Количество пристроенных помещений</h2>
          <Input 
            type="number" 
            placeholder="Например: 1" 
            className={styles.inputFieldClassic}
            value={String(annexCount)}
            onChange={(e) => setAnnexCount(parseInt(e.target.value) || 0)}
          />
        </div>
        <Select 
          title='Корпуса, связанные с пристроенными помещениями'
          options={materialOptionsA}
          value={selectedIndex}
          onChange={handleIndexChange}
          placeholder="Выберите нужное значение"
          multiple={true}
          inlineOptions={true}
        />
      </div>

      <NumberFieldsGrid title="Стилобатная часть">
        {renderStilobaty()}
      </NumberFieldsGrid>

      <NumberFieldsGrid title="Пристроенные помещения общественного назначения">
        {renderAnnexes()}
      </NumberFieldsGrid>

      <NumberFieldsGrid title="Наземная часть корпусов">
        {renderBuildings()}
      </NumberFieldsGrid>

       <NumberFieldsGrid title="Подземная часть корпусов">
        <CheckboxTrue 
          checked={undergroundCalculated}
          onChange={setUndergroundCalculated}
          label="Расчетные данные"
        />
        <div></div>
        <NumberField 
          title="Количество этажей"
          value={undergroundFloors}
          onChange={setUndergroundFloors}
          placeholder="1"
        />
        <div></div>

        <NumberField 
          title="Средняя площадь этажа в м²"
          value={undergroundAvgArea}
          placeholder='1'
          onChange={setUndergroundAvgArea}
        />
        <div></div>

        <NumberField 
          title="Средняя высота этажа в м²"
          value={undergroundAvgHeight}
          placeholder='1'
          onChange={setUndergroundAvgHeight}
        />
        <div></div>

        <NumberField 
          title="Общая площадь кладовых помещений в м²"
          value={undergroundStorageArea || '1'}
          placeholder='1'
          onChange={setUndergroundStorageArea}
          disabled
        />
        <div></div>

        <CheckboxField 
          key="underground-parking"
          title="Наличие встроенной подземной стоянки автомобилей закрытого типа" 
          value={hasUndergroundParking} 
          onChange={setHasUndergroundParking} 
          inline={true}
        />
        <div></div>

        <NumberField 
          title="Общая площадь в м²"
          value={undergroundTotalArea || '1'}
          placeholder='1'
          onChange={setUndergroundTotalArea}
          disabled
        />
      </NumberFieldsGrid>

      <h2 style={{ fontFamily: 'Montserrat' }}>Площади и типы фасадов</h2>
      <Slider 
        title1="Глухая часть фасадов"
        title2="Светопрозрачные конструкции фасадов"
        sliderTitles1={[
          'Панель ж/б',
          'Кирпичная кладка',
          'Мокрый фасад (штукатурка)',
          'Плитка',
          'Кассеты металлические стальные',
          'Фиброцементные панели',
          'Кассеты композитные',
          'С стеклофибробетон'
        ]}
        sliderTitles2={[
          'Стеклопакет (в ПВХ раме)',
          'Стеклопакет (в алюминиевой раме)',
          'Входные группы'
        ]}
      />

      <CheckboxTrue 
        checked={objectCalculated}
        onChange={setObjectCalculated}
        label="Расчетные данные по объекту"
      />

       <NumberFieldsGrid title="Расчетные данные по объекту">
        <NumberField 
          title="Количество незадымляемых лестничных клеток, обслуживающих надземную часть"
          value={calculatedStairs || '1'}
          placeholder='1'
          onChange={setCalculatedStairs}
          disabled
        />

        <NumberField 
          title="Количество лифтов в здании (Надземной части, стилобатной части, пристроенных помещений)"
          value={calculatedElevators || '1'}
          placeholder='1'
          onChange={setCalculatedElevators}
          disabled
        />

        <NumberField 
          title="Количество лестничных клеток, обслуживающие надземную часть"
          value={calculatedStaircases || '1'}
          placeholder='1'
          onChange={setCalculatedStaircases}
          disabled
        />

        <NumberField 
          title="Суммарная площадь общественных помещений на объекте"
          value={calculatedPublicArea || '1'}
          placeholder='1'
          onChange={setCalculatedPublicArea}
          disabled
        />

        <NumberField 
          title="Назначение встроенных общественных помещений"
          value={calculatedPublicPurpose || '1'}
          placeholder='1'
          onChange={setCalculatedPublicPurpose}
          disabled
        />

        <NumberField 
          title="Количество общественных помещений"
          value={calculatedPublicCount || '1'}
          placeholder='1'
          onChange={setCalculatedPublicCount}
          disabled
        />

        <NumberField 
          title="Строительный объем надземной части здания"
          value={calculatedAbovegroundVolume || '1'}
          placeholder='1'
          onChange={setCalculatedAbovegroundVolume}
          disabled
        />

        <NumberField 
          title="Количество жителей объекта"
          value={calculatedResidents || '1'}
          placeholder='1'
          onChange={setCalculatedResidents}
          disabled
        />

        <NumberField 
          title="Строительный объем подземной части здания"
          value={calculatedUndergroundVolume || '1'}
          placeholder='1'
          onChange={setCalculatedUndergroundVolume}
          disabled
        />
        <div></div>

        <NumberField 
          title="Общая площадь объекта"
          value={calculatedTotalArea || '1'}
          placeholder='1'
          onChange={setCalculatedTotalArea}
          disabled
        /><div></div>

        <NumberField 
          title="Строительный объем объекта"
          value={calculatedTotalVolume || '1'}
          placeholder='1'
          onChange={setCalculatedTotalVolume}
          disabled
        /><div></div>

        <NumberField 
          title="Количество жителей объекта"
          value={calculatedResidentsCount || '1'}
          placeholder='1'
          onChange={setCalculatedResidentsCount}
          disabled
        />
      </NumberFieldsGrid>
    </div>
  );
}
