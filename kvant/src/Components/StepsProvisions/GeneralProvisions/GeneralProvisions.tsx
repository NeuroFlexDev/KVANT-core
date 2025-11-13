import { useEffect, useRef, useState } from 'react';

import styles from './generalProv.module.css';
import Card from '../../ElementUi/Card/Card';
import Select from '../../ElementUi/Select/Select';
import Input from '../../ElementUi/Input/Input';
import { useFormSection } from '../../../contexts/FormContext';
// иконки функционального назначения объекта
import zhiloy from '../../../assets/icons/ui/cards/zhiloy.svg';
import school from '../../../assets/icons/ui/cards/school.svg';
import garage from '../../../assets/icons/ui/cards/garage.svg';

const sections = [
  {
    title: 'Функциональное назначение объекта',
    className: styles.cardsContainer,
    items: [
      { id: 1, image: zhiloy, text: 'Жилое здание', primary: true },
      { id: 2, image: school, text: 'Общественное здание', primary: true },
      { id: 3, image: garage, text: 'Производственное здание', primary: true }
    ],
  }
];

interface GeneralFormData extends Record<string, unknown> {
  selectedCard: number | null;
  address: string | null;
  addressLocation: { lat: string; lon: string } | null;
  costIndex: string | null;
  landArea: string;
}

const defaultData: GeneralFormData = {
  selectedCard: null,
  address: null,
  addressLocation: null,
  costIndex: null,
  landArea: '',
};

type AddressValidationState = 'idle' | 'loading' | 'success' | 'error';

interface AddressSuggestion {
  id: string;
  label: string;
  lat: string;
  lon: string;
}

const MIN_ADDRESS_LENGTH = 3;
const AUTOCOMPLETE_DELAY_MS = 450;

export default function GeneralProvisionsPage() {
  const { data, setData } = useFormSection<GeneralFormData>('general', defaultData);
  const [addressQuery, setAddressQuery] = useState<string>(data.address ?? '');
  const [addressResults, setAddressResults] = useState<AddressSuggestion[]>([]);
  const [addressStatus, setAddressStatus] = useState<AddressValidationState>('idle');
  const [addressMessage, setAddressMessage] = useState<string | null>(null);
  const skipLookupRef = useRef(false);

  useEffect(() => {
    setAddressQuery(data.address ?? '');
  }, [data.address]);

  const indexOptions = [
    { value: 'q1-2024', label: '1 квартал 2024' },
    { value: 'q2-2024', label: '2 квартал 2024' },
    { value: 'q3-2024', label: '3 квартал 2024' },
    { value: 'q4-2024', label: '4 квартал 2024' },
  ];

  const handleSelect = (id: string | number) => {
    setData({ selectedCard: Number(id) });
  };

  const handleIndexChange = (value: string | null) => {
    setData({ costIndex: value });
  };

  const handleAreaChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const value = e.target.value;
    setData({ landArea: value });
  };

  const handleAddressInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const value = e.target.value;
    setAddressQuery(value);
    setAddressResults([]);
    setAddressStatus('idle');
    setAddressMessage(value.trim().length ? 'Введите минимум 3 символа для поиска.' : null);
    setData({
      address: value.length > 0 ? value : null,
      addressLocation: null,
    });
  };

  useEffect(() => {
    const trimmed = addressQuery.trim();

    if (skipLookupRef.current) {
      skipLookupRef.current = false;
      return;
    }

    if (!trimmed) {
      setAddressStatus('idle');
      setAddressMessage(null);
      setAddressResults([]);
      return;
    }

    if (trimmed.length < MIN_ADDRESS_LENGTH) {
      setAddressStatus('idle');
      setAddressResults([]);
      setAddressMessage('Введите минимум 3 символа для поиска.');
      return;
    }

    const controller = new AbortController();
    const timeoutId = window.setTimeout(async () => {
      setAddressStatus('loading');
      setAddressMessage('Ищем адрес в базе OSM…');

      try {
        const params = new URLSearchParams({
          format: 'json',
          addressdetails: '1',
          limit: '5',
          q: trimmed,
        });

        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?${params.toString()}`,
          {
            headers: {
              Accept: 'application/json',
              'User-Agent': 'kvant-core-local/1.0',
            },
            signal: controller.signal,
          },
        );

        if (!response.ok) {
          throw new Error('OSM request failed');
        }

        const payload = (await response.json()) as Array<{
          place_id?: number;
          display_name: string;
          lat: string;
          lon: string;
        }>;

        if (!Array.isArray(payload) || payload.length === 0) {
          setAddressStatus('error');
          setAddressMessage('Адрес не найден в OSM. Попробуйте уточнить запрос.');
          setAddressResults([]);
          return;
        }

        const formatted = payload.map((item) => ({
          id: String(item.place_id ?? `${item.lat}-${item.lon}`),
          label: item.display_name,
          lat: item.lat,
          lon: item.lon,
        }));

        setAddressResults(formatted);
        setAddressStatus('success');
        setAddressMessage('Выберите подходящий адрес из найденных результатов.');
      } catch (error) {
        if (controller.signal.aborted) {
          return;
        }
        console.error('OSM lookup failed', error);
        setAddressStatus('error');
        setAddressMessage('Не удалось проверить адрес через OSM. Повторите попытку позже.');
        setAddressResults([]);
      }
    }, AUTOCOMPLETE_DELAY_MS);

    return () => {
      controller.abort();
      clearTimeout(timeoutId);
    };
  }, [addressQuery]);

  const handleResultSelect = (suggestion: AddressSuggestion) => {
    skipLookupRef.current = true;
    setData({
      address: suggestion.label,
      addressLocation: { lat: suggestion.lat, lon: suggestion.lon },
    });
    setAddressQuery(suggestion.label);
    setAddressResults([]);
    setAddressStatus('success');
    setAddressMessage('Адрес подтвержден через OSM.');
  };

  const renderCoordinate = (value: string) => {
    const numeric = Number(value);
    return Number.isFinite(numeric) ? numeric.toFixed(5) : value;
  };

  return (
    <div className={styles.container}>
      {sections.map(({ title, className, items }) => (
        <section key={title} style={{ marginTop: 20 }}>
          <h2>{title}</h2>
          <div className={className}>
            {items.map(item => (
              <Card
                key={item.id}
                id={item.id}
                image={item.image}
                text={item.text}
                primary={item.primary}
                selected={data.selectedCard === item.id}
                onSelect={handleSelect}
              />
            ))}
          </div>
        </section>
      ))}
      <div className={styles.addressBlock}>
        <div className={styles.addressLabelRow}>
          <h2>Адрес объекта</h2>
          {data.addressLocation && (
            <span className={styles.addressCoordinates}>
              {renderCoordinate(data.addressLocation.lat)},&nbsp;
              {renderCoordinate(data.addressLocation.lon)}
            </span>
          )}
        </div>
        <div className={styles.addressInputRow}>
          <input
            type="text"
            value={addressQuery}
            onChange={handleAddressInputChange}
            placeholder="Например: г. Москва, ул. Пушкинская, д. 1"
            className={styles.addressInputField}
          />
        </div>
        {addressMessage && (
          <p
            className={`${styles.addressStatus} ${
              addressStatus === 'error'
                ? styles.addressStatusError
                : addressStatus === 'success'
                ? styles.addressStatusSuccess
                : ''
            }`}
          >
            {addressMessage}
          </p>
        )}
        {addressResults.length > 0 && (
          <div className={styles.addressResults}>
            {addressResults.map((result) => (
              <button
                key={result.id}
                type="button"
                className={styles.addressResultButton}
                onClick={() => handleResultSelect(result)}
              >
                <span>{result.label}</span>
                <span className={styles.addressResultCoords}>
                  {renderCoordinate(result.lat)}, {renderCoordinate(result.lon)}
                </span>
              </button>
            ))}
          </div>
        )}
      </div>
      <Select
        title='Индекс сметной стоимости'
        options={indexOptions}
        value={data.costIndex ? [data.costIndex] : []}
        onChange={(values) => handleIndexChange(values?.[0] ?? null)}
        placeholder="Например: 3 квартал 2024"
      />
      <div className={styles.inputContainer}>
        <h2>Площадь участка строительства в м²</h2>
        <Input 
          type="number" 
          placeholder="Например: 11303,0" 
          className={styles.inputFieldClassic}
          value={data.landArea}
          onChange={handleAreaChange}
        />
      </div>
    </div>
  );
}
