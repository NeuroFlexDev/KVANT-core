import styles from './summaryInfo.module.css';
import Card from '../../ElementUi/Card/Card';
import { CheckboxTrue } from '../../ElementUi/CheckboxTrue/Checkbox';
import Select from '../../ElementUi/Select/Select';
import NumberField from '../../ElementUi/NumberField/NumberField';
import { useFormSection } from '../../../contexts/FormContext';

const sections = [
  {
    title: 'Сейсмичность региона строительства',
    className: styles.cardsContainer,
    items: [
      { id: 1, description: 'Менее 7 баллов', primary: true },
      { id: 2, description: '7 баллов', primary: true },
      { id: 3, description: '8 баллов', primary: true },
      { id: 4, description: '9 баллов', primary: true },
      { id: 5, description: '10 баллов', primary: true },
    ],
  },
  {
    title: 'Тип грунта',
    className: styles.cardsContainer,
    items: [
      { id: 6, description: 'Сыпучий грунт', primary: true },
      { id: 7, description: 'Скальная порода', primary: true },
    ],
  },
  {
    title: 'Тип ограждающие конструкции котлована',
    className: styles.cardsContainer,
    items: [
      { id: 8, description: 'Отсутствие ограждающей конструкции', primary: true },
      { id: 9, description: 'Шпунт (опоры Ларсена, трубы)', primary: true },
      { id: 10, description: 'Стена в грунте', primary: true },
    ],
  },
  {
    title: 'Тип фундамента',
    className: styles.cardsContainer,
    items: [
      { id: 11, description: 'Монолитная плита на естественном основании', primary: true },
      { id: 12, description: 'Свайное поле (заливные сваи)', primary: true },
      { id: 13, description: 'Свайное поле (забивные сваи)', primary: true },
    ],
  },
  {
    title: 'Конструктивная схема',
    className: styles.cardsContainer,
    items: [
      { id: 14, description: 'Монолитно-кирпичный', primary: true },
      { id: 15, description: 'Монолитно-каркасный', primary: true },
      { id: 16, description: 'Монолитный', primary: true },
      { id: 17, description: 'Кирпичный', primary: true },
      { id: 18, description: 'Панелевый', primary: true },
    ],
  },
];

interface SummaryFormData extends Record<string, unknown> {
  cardSelections: Record<string, number>;
  hasSink: boolean;
  selectedMaterials: string[];
  fireCompartmentsCount: string;
  fireHazardClass: string;
  fireResistanceLimit: string;
  fireResistanceDegree: string;
}

const defaultSummaryData: SummaryFormData = {
  cardSelections: {},
  hasSink: false,
  selectedMaterials: [],
  fireCompartmentsCount: '',
  fireHazardClass: '',
  fireResistanceLimit: '',
  fireResistanceDegree: '',
};

export default function SummaryInfo() {
  const { data, setData } = useFormSection<SummaryFormData>('summary', defaultSummaryData);

  const cardSelections = data.cardSelections ?? {};
  const selectedMaterials = data.selectedMaterials ?? [];

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

  const handleSelect = (sectionTitle: string, id: number) => {
    setData((prev) => ({
      ...prev,
      cardSelections: {
        ...(prev.cardSelections ?? {}),
        [sectionTitle]: id,
      },
    }));
  };

  const handleNumberFieldChange = (field: keyof Pick<
    SummaryFormData,
    'fireCompartmentsCount' | 'fireHazardClass' | 'fireResistanceLimit' | 'fireResistanceDegree'
  >) => (value: string) => {
    setData({
      [field]: value,
    } as Partial<SummaryFormData>);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Основные конструктивные решения</h1>

      <div className={styles.cardsContainerMain}>
        {sections.map(({ title, className, items }) => (
          <section key={title} style={{ marginTop: 20 }}>
            <h2>{title}</h2>
            <div className={className}>
              {items.map((item) => (
              <Card
                key={item.id}
                id={item.id}
                text={item.description}
                primary={item.primary}
                selected={cardSelections[title] === item.id}
                onSelect={(id) => handleSelect(title, Number(id))}
              />
              ))}
            </div>
          </section>
        ))}
      </div>

      <h1 className={styles.title}>Параметры пожарной безопасности</h1>
      <div className={styles.checkboxContainer}>
        <CheckboxTrue
          checked={data.hasSink}
          onChange={(checked) => setData({ hasSink: checked })}
          label="Расчетные данные"
        />
        <Select
          title="Здания/секции для выделения в самостоятельный отсек"
          options={materialOptionsA}
          value={selectedMaterials}
          onChange={(values) => setData({ selectedMaterials: values })}
          placeholder="Выберите нужное значение"
          multiple
          inlineOptions
        />
        <div className={styles.numberFieldContainer}>
          <NumberField
            title="Количество пожарных отсеков надземной части объекта"
            value={data.fireCompartmentsCount}
            onChange={handleNumberFieldChange('fireCompartmentsCount')}
            placeholder=""
            background="#FFFFFF"
          />
          <NumberField
            title="Класс конструктивной пожарной опасности отсека"
            value={data.fireHazardClass}
            onChange={handleNumberFieldChange('fireHazardClass')}
            placeholder=""
            background="#FFFFFF"
          />
          <NumberField
            title="Предел огнестойкости основных строительных конструкций"
            value={data.fireResistanceLimit}
            onChange={handleNumberFieldChange('fireResistanceLimit')}
            placeholder=""
            background="#FFFFFF"
          />
          <NumberField
            title="Степень огнестойкости пожарного отсека"
            value={data.fireResistanceDegree}
            onChange={handleNumberFieldChange('fireResistanceDegree')}
            placeholder=""
            background="#FFFFFF"
          />
        </div>
      </div>
    </div>
  );
}
