import { Fragment } from 'react';

import CheckboxField from '../../ElementUi/Checkbox/CheckboxField';
import Select from '../../ElementUi/Select/Select';
import styles from './engineeringSolution.module.css';
import { useFormSection } from '../../../contexts/FormContext';

interface SolutionData {
  [key: string]: string | boolean | null | string[];
}

const initialFormData: SolutionData = {
  hasModularShield: null,
  powerConductor: null,
  hasWaterManifold: null,
  airConditioningType: null,
  hasPumpStation: null,
  parkingHeatingType: null,
  hasHeatingManifold: null,
  ventilationType: null,
  hasSecurityPost: null,
  bathroomWallFinish: null,
  wallReinforcementMesh: null,
  generalWallFinish: null,
  wallPlaster: null,
  floorScreed: null,
  waterproofing: null,
  selfLevelingFloor: null,
  generalFloorFinish: null,
  steelThreshold: null,
  bathroomFloorFinish: null,
  baseboard: null,
  stretchCeiling: null,
  suspendedCeiling: null,
  doorUnit: null,
  sinkCabinet: null,
  windowPanel: null,
  sink: null,
  bath: null,
  faucet: null,
  showerTray: null,
  toilet: null,
  towelWarmer: null,
  socketNetwork: null,
  lightingNetwork: null,
  waterSupplyNetwork: null,
  drainageNetwork: null,
  heatingNetwork: null,
  ventilationNetwork: null,
  intercomSystem: null,
  conditioningNetwork: null,
  cableTV: null,
  structuredCableSystem: null,
};

const materialOptions = [
  { value: 'one', label: 'Вариант 1' },
  { value: 'two', label: 'Вариант 2' },
  { value: 'three', label: 'Вариант 3' },
  { value: 'four', label: 'Вариант 4' },
  { value: 'five', label: 'Вариант 5' },
];

const fieldGroups = [
  {
    title: 'Общие инженерные решения',
    fields: [
      { type: 'checkbox', key: 'hasModularShield', label: 'Модульный этажный щит типа УЭРМ' },
      { type: 'select', key: 'powerConductor', label: 'Проводник магистральных сетей электроснабжения' },
      { type: 'checkbox', key: 'hasWaterManifold', label: 'Коллекторно-лучевая разводка водоснабжения в МОП' },
      { type: 'select', key: 'airConditioningType', label: 'Тип системы кондиционирования жилой части' },
      { type: 'checkbox', key: 'hasPumpStation', label: 'Наличие насосной станции' },
      { type: 'select', key: 'parkingHeatingType', label: 'Тип отопления автостоянки' },
      { type: 'checkbox', key: 'hasHeatingManifold', label: 'Коллекторно-лучевая разводка отопления в МОП' },
      { type: 'select', key: 'ventilationType', label: 'Приточная вентиляция жилой части' },
      { type: 'checkbox', key: 'hasSecurityPost', label: 'Наличие помещения поста охраны' },
    ],
  },
  {
    title: 'Отделка квартир',
    fields: [
      { type: 'subtitle', label: 'Стены' },
      { type: 'checkbox', key: 'bathroomWallFinish', label: 'Финишное покрытие санузлов' },
      { type: 'checkbox', key: 'wallReinforcementMesh', label: 'Сетка для армирования' },
      { type: 'checkbox', key: 'generalWallFinish', label: 'Финишное покрытие (за исключением санузлов)' },
      { type: 'checkbox', key: 'wallPlaster', label: 'Штукатурка' },
      { type: 'subtitle', label: 'Полы' },
      { type: 'checkbox', key: 'floorScreed', label: 'Стяжка' },
      { type: 'checkbox', key: 'waterproofing', label: 'Гидроизоляция' },
      { type: 'checkbox', key: 'selfLevelingFloor', label: 'Наливной пол' },
      { type: 'checkbox', key: 'generalFloorFinish', label: 'Финишное покрытие (за исключением санузлов)' },
      { type: 'checkbox', key: 'steelThreshold', label: 'Порожек стальной' },
      { type: 'checkbox', key: 'bathroomFloorFinish', label: 'Финишное покрытие санузлов' },
      { type: 'checkbox', key: 'baseboard', label: 'Плинтус' },
      { type: 'subtitle', label: 'Потолки' },
      { type: 'checkbox', key: 'stretchCeiling', label: 'Потолок натяжной' },
      { type: 'checkbox', key: 'suspendedCeiling', label: 'Потолок подвесной' },
    ],
  },
  {
    title: 'Интерьерные решения',
    fields: [
      { type: 'checkbox', key: 'doorUnit', label: 'Дверной блок' },
      { type: 'checkbox', key: 'sinkCabinet', label: 'Тумба под раковину' },
      { type: 'checkbox', key: 'windowPanel', label: 'Подоконная панель' },
      { type: 'checkbox', key: 'sink', label: 'Раковина' },
      { type: 'checkbox', key: 'bath', label: 'Ванна' },
      { type: 'checkbox', key: 'faucet', label: 'Сместитель' },
      { type: 'checkbox', key: 'showerTray', label: 'Душевой поддон' },
      { type: 'checkbox', key: 'toilet', label: 'Унитаз в комплекте' },
      { type: 'checkbox', key: 'towelWarmer', label: 'Полотенцесушитель' },
    ],
  },
  {
    title: 'Инженерия квартир',
    fields: [
      { type: 'checkbox', key: 'socketNetwork', label: 'Розеточная сеть' },
      { type: 'checkbox', key: 'lightingNetwork', label: 'Сеть освещения' },
      { type: 'checkbox', key: 'waterSupplyNetwork', label: 'Сеть водоснабжения' },
      { type: 'checkbox', key: 'drainageNetwork', label: 'Сеть водоотведения' },
      { type: 'checkbox', key: 'heatingNetwork', label: 'Сеть отопления' },
      { type: 'checkbox', key: 'ventilationNetwork', label: 'Сеть вентиляции' },
      { type: 'checkbox', key: 'intercomSystem', label: 'Система домофонной связи' },
      { type: 'checkbox', key: 'conditioningNetwork', label: 'Сеть кондиционирования' },
      { type: 'checkbox', key: 'cableTV', label: 'Кабельное телевидение' },
      { type: 'checkbox', key: 'structuredCableSystem', label: 'Структурированная кабельная система (интернет)' },
    ],
  },
];

export default function EngineeringSolution() {
  const { data: formData, setData } = useFormSection<SolutionData>('engineering', initialFormData);

  const handleCheckboxChange = (field: string) => (value: boolean) => {
    setData({
      [field]: value,
    } as Partial<SolutionData>);
  };

  const handleSelectChange = (field: string) => (values: string[]) => {
    setData({
      [field]: values?.[0] ?? null,
    } as Partial<SolutionData>);
  };

  const renderField = (field: any) => {
    switch (field.type) {
      case 'checkbox':
        return (
          <CheckboxField
            key={field.key}
            title={field.label}
            value={(formData[field.key] as boolean | null) ?? null}
            onChange={handleCheckboxChange(field.key)}
            inline
          />
        );
      case 'select':
        return (
          <Select
            key={field.key}
            title={field.label}
            options={materialOptions}
            value={
              formData[field.key]
                ? [String(formData[field.key])]
                : []
            }
            onChange={handleSelectChange(field.key)}
            placeholder="Выберите нужное значение"
          />
        );
      case 'subtitle':
        return (
          <h1 key={field.label} className={styles.title} style={{ gridColumn: 'span 2' }}>
            {field.label}
          </h1>
        );
      default:
        return null;
    }
  };

  return (
    <div className={styles.container}>
      {fieldGroups.map((group, index) => (
        <Fragment key={index}>
          <h1 className={styles.title}>{group.title}</h1>
          <div className={styles.checkboxContainer}>
            {group.fields.map(renderField)}
          </div>
        </Fragment>
      ))}
    </div>
  );
}
