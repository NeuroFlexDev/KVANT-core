import CheckboxField from '../../ElementUi/Checkbox/CheckboxField';
import styles from './compositionSection.module.css';
import { useFormSection } from '../../../contexts/FormContext';

interface SolutionData {
  [key: string]: boolean | null;
}

const initialCompositionData: SolutionData = {
  hasArchitectureSolution: null,
  hasConstructionSolution: null,
  hasIOS: null,
  powerEquipmentAndLighting: null,
  internalWaterSupply: null,
  automaticFireExtinguishing: null,
  internalFireWaterSupply: null,
  internalWaterDrainage: null,
  cableDuctSystem: null,
  heating: null,
  securityVideoSurveillance: null,
  conditioning: null,
  ventilation: null,
  collectiveCableTV: null,
  individualHeatPoint: null,
  securityAlarmSystem: null,
  accessControlSystem: null,
  localAreaNetwork: null,
  mgsStaffCallSystem: null,
  securityTVSystem: null,
  publicTelephoneNetwork: null,
  deratizationSystem: null,
  structuredCableSystem: null,
  radioSystem: null,
  timeSystem: null,
  automaticPowderFireExtinguishing: null,
  automaticGasFireExtinguishing: null,
  engineeringSystemsAutomation: null,
  fireAlarmSystem: null,
  evacuationManagementSystem: null,
  industrialSewage: null,
};

const fieldGroups = [
  {
    fields: [
      { type: 'checkbox', key: 'hasArchitectureSolution', label: 'Раздел - Архитектурные решения' },
      { type: 'checkbox', key: 'hasConstructionSolution', label: 'Раздел - Конструктивные решения' },
      { type: 'checkbox', key: 'hasIOS', label: 'Разделы ИОС | Подразделы' },
    ],
  },
  {
    fields: [
      { type: 'checkbox', key: 'powerEquipmentAndLighting', label: 'Силовое электрооборудование и электрическое освещение' },
      { type: 'checkbox', key: 'internalWaterSupply', label: 'Внутренние сети водоснабжения' },
      { type: 'checkbox', key: 'automaticFireExtinguishing', label: 'Сети автоматической установки пожаротушения' },
      { type: 'checkbox', key: 'internalFireWaterSupply', label: 'Внутренний противопожарный водопровод' },
      { type: 'checkbox', key: 'internalWaterDrainage', label: 'Внутренние сети водоотведения' },
      { type: 'checkbox', key: 'cableDuctSystem', label: 'Система кабельных каналов' },
      { type: 'checkbox', key: 'heating', label: 'Отопление,Теплоснабжение' },
      { type: 'checkbox', key: 'securityVideoSurveillance', label: 'Система охранного телевидения' },
      { type: 'checkbox', key: 'conditioning', label: 'Кондиционирование и холодоснабжение' },
      { type: 'checkbox', key: 'ventilation', label: 'Вентиляция общеобменная, противодымная' },
      { type: 'checkbox', key: 'collectiveCableTV', label: 'Система коллективного приема кабельного телевидения' },
      { type: 'checkbox', key: 'individualHeatPoint', label: 'Индивидуальный тепловой пункт' },
      { type: 'checkbox', key: 'securityAlarmSystem', label: 'Система охранно-тревожной сигнализации' },
      { type: 'checkbox', key: 'accessControlSystem', label: 'Система контроля и управление доступом' },
      { type: 'checkbox', key: 'localAreaNetwork', label: 'Система локальной вычислительной сети' },
      { type: 'checkbox', key: 'mgsStaffCallSystem', label: 'Тревожная сигнализация вызова персонала для МГН' },
      { type: 'checkbox', key: 'securityTVSystem', label: 'Система охранного телевидения' },
      { type: 'checkbox', key: 'publicTelephoneNetwork', label: 'Телефонная связь сети общего пользования' },
      { type: 'checkbox', key: 'deratizationSystem', label: 'Охранно-защитная дератизационная система' },
      { type: 'checkbox', key: 'structuredCableSystem', label: 'Структурированная кабельная система' },
      { type: 'checkbox', key: 'radioSystem', label: 'Радиофикация' },
      { type: 'checkbox', key: 'timeSystem', label: 'Система электрочасофикации' },
      { type: 'checkbox', key: 'automaticPowderFireExtinguishing', label: 'Установка порошкового пожаротушения автоматическая' },
      { type: 'checkbox', key: 'automaticGasFireExtinguishing', label: 'Установка газового пожаротушения автоматическая' },
      { type: 'checkbox', key: 'engineeringSystemsAutomation', label: 'Автоматизация и диспетчеризация инженерных систем' },
      { type: 'checkbox', key: 'fireAlarmSystem', label: 'Система пожарной сигнализации, Система противопожарной автоматики' },
      { type: 'checkbox', key: 'evacuationManagementSystem', label: 'Система оповещения и управления эвакуацией' },
      { type: 'checkbox', key: 'industrialSewage', label: 'Промышленная канализация' },
    ],
  },
];

export default function CompositionSection() {
  const { data: formData, setData } = useFormSection<SolutionData>('composition', initialCompositionData);

  const handleChange = (fieldKey: string) => (value: boolean) => {
    setData({
      [fieldKey]: value,
    } as Partial<SolutionData>);
  };

  return (
    <div className={styles.container}>
      {fieldGroups.map((group, index) => (
        <div key={index} className={styles.checkboxContainer}>
          {group.fields.map((field) => (
            field.type === 'checkbox' ? (
              <CheckboxField
                key={field.key}
                title={field.label}
                value={(formData[field.key] as boolean | null) ?? null}
                onChange={handleChange(field.key)}
              />
            ) : null
          ))}
        </div>
      ))}
    </div>
  );
}
