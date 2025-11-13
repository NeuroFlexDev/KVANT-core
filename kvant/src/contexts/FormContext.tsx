import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';
import type { ReactNode } from 'react';

import { questionnaireApi } from '../api/questionnaire';
import type { QuestionnaireFormDetail, QuestionnaireSection } from '../api/questionnaire';

export type SectionKey =
  | 'general'
  | 'architecture'
  | 'summary'
  | 'engineering'
  | 'composition';

export interface SectionState {
  title?: string | null;
  orderIndex: number;
  data: Record<string, unknown>;
  isCompleted: boolean;
  completedAt: string | null;
  dirty: boolean;
}

export const SECTION_ORDER: SectionKey[] = [
  'general',
  'architecture',
  'summary',
  'engineering',
  'composition',
];

const SECTION_DEFAULT_TITLES: Record<SectionKey, string> = {
  general: 'Общие сведения',
  architecture: 'Архитектурные параметры',
  summary: 'Сводные показатели',
  engineering: 'Инженерные решения',
  composition: 'Состав разделов',
};

const createDefaultSectionState = (key: SectionKey): SectionState => ({
  title: SECTION_DEFAULT_TITLES[key],
  orderIndex: SECTION_ORDER.indexOf(key),
  data: {},
  isCompleted: false,
  completedAt: null,
  dirty: false,
});

interface FormContextValue {
  form?: QuestionnaireFormDetail;
  sections: Record<SectionKey, SectionState>;
  isLoading: boolean;
  isSaving: boolean;
  currentStep: number;
  refresh: () => Promise<void>;
  updateSection: (
    sectionKey: SectionKey,
    updater:
      | Record<string, unknown>
      | ((prev: Record<string, unknown>) => Record<string, unknown>),
  ) => void;
  setSectionCompletion: (sectionKey: SectionKey, isCompleted: boolean) => void;
  saveSection: (sectionKey: SectionKey) => Promise<void>;
  saveAllSections: () => Promise<void>;
  goToStep: (step: number) => Promise<void>;
}

const FormContext = createContext<FormContextValue | undefined>(undefined);

const mergeSectionData = (
  base: Record<string, unknown>,
  patch: Record<string, unknown>,
): Record<string, unknown> => ({
  ...base,
  ...patch,
});

const normaliseSection = (section: QuestionnaireSection): SectionState => ({
  title: section.title ?? SECTION_DEFAULT_TITLES[section.section_key as SectionKey] ?? section.title,
  orderIndex:
    section.order_index ??
    SECTION_ORDER.indexOf(section.section_key as SectionKey),
  data: section.data ?? {},
  isCompleted: section.is_completed,
  completedAt: section.completed_at ?? null,
  dirty: false,
});

const buildSectionState = (
  apiSections: QuestionnaireSection[],
): Record<SectionKey, SectionState> => {
  const state: Record<SectionKey, SectionState> = SECTION_ORDER.reduce(
    (acc, key) => {
      acc[key] = createDefaultSectionState(key);
      return acc;
    },
    {} as Record<SectionKey, SectionState>,
  );

  apiSections.forEach((section) => {
    const key = section.section_key as SectionKey;
    if (SECTION_ORDER.includes(key)) {
      state[key] = normaliseSection(section);
    }
  });

  return state;
};

const hasMeaningfulData = (value: Record<string, unknown> | undefined | null): boolean => {
  if (!value) {
    return false;
  }

  return Object.values(value).some((entry) => {
    if (entry === null || entry === undefined) {
      return false;
    }
    if (typeof entry === 'string') {
      return entry.trim().length > 0;
    }
    if (Array.isArray(entry)) {
      return entry.length > 0;
    }
    if (typeof entry === 'object') {
      return Object.keys(entry as Record<string, unknown>).length > 0;
    }
    return true;
  });
};

interface FormProviderProps {
  formId: number;
  children: ReactNode;
}

export const FormProvider = ({ formId, children }: FormProviderProps) => {
  const [form, setForm] = useState<QuestionnaireFormDetail | undefined>();
  const [sections, setSections] = useState<Record<SectionKey, SectionState>>(
    () => buildSectionState([]),
  );
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<number>(0);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await questionnaireApi.getForm(formId);
      setForm(data);
      setSections(buildSectionState(data.sections));
      setCurrentStep(data.current_step ?? 0);
    } finally {
      setIsLoading(false);
    }
  }, [formId]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const updateSection: FormContextValue['updateSection'] = useCallback(
    (sectionKey, updater) => {
      setSections((prev) => {
        const section = prev[sectionKey] ?? createDefaultSectionState(sectionKey);
        const nextData =
          typeof updater === 'function'
            ? updater(section.data)
            : mergeSectionData(section.data, updater);
        return {
          ...prev,
          [sectionKey]: {
            ...section,
            data: nextData,
            dirty: true,
          },
        };
      });
    },
    [],
  );

  const setSectionCompletion = useCallback(
    (sectionKey: SectionKey, isCompleted: boolean) => {
      setSections((prev) => {
        const section = prev[sectionKey] ?? createDefaultSectionState(sectionKey);
        return {
          ...prev,
          [sectionKey]: {
            ...section,
            isCompleted,
            completedAt: isCompleted ? section.completedAt : null,
            dirty: true,
          },
        };
      });
    },
    [],
  );

  const saveSection = useCallback(
    async (sectionKey: SectionKey) => {
      const sectionState = sections[sectionKey];
      if (!sectionState) {
        return;
      }

      const hasData = hasMeaningfulData(sectionState.data);
      const nextIsCompleted = hasData ? true : sectionState.isCompleted;
      const nextCompletedAt =
        nextIsCompleted && !sectionState.isCompleted
          ? new Date().toISOString()
          : sectionState.completedAt ?? undefined;

      setIsSaving(true);
      try {
        const updated = await questionnaireApi.upsertSection(formId, sectionKey, {
          title: sectionState.title ?? SECTION_DEFAULT_TITLES[sectionKey],
          order_index: sectionState.orderIndex,
          data: sectionState.data,
          is_completed: nextIsCompleted,
          completed_at: nextCompletedAt,
        });

        setSections((prev) => ({
          ...prev,
          [sectionKey]: {
            title:
              updated.title ??
              prev[sectionKey]?.title ??
              SECTION_DEFAULT_TITLES[sectionKey],
            orderIndex:
              updated.order_index ??
              prev[sectionKey]?.orderIndex ??
              SECTION_ORDER.indexOf(sectionKey),
            data: updated.data ?? {},
            isCompleted: updated.is_completed,
            completedAt: updated.completed_at ?? null,
            dirty: false,
          },
        }));

        setForm((prev) =>
          prev
            ? {
                ...prev,
                updated_at: updated.updated_at,
              }
            : prev,
        );
      } finally {
        setIsSaving(false);
      }
    },
    [formId, sections],
  );

  const saveAllSections = useCallback(async () => {
    for (const key of SECTION_ORDER) {
      if (sections[key]?.dirty) {
        // eslint-disable-next-line no-await-in-loop
        await saveSection(key);
      }
    }
  }, [saveSection, sections]);

  const goToStep = useCallback(
    async (step: number) => {
      setCurrentStep(step);
      setForm((prev) =>
        prev
          ? {
              ...prev,
              current_step: step,
            }
          : prev,
      );
      try {
        await questionnaireApi.updateForm(formId, { current_step: step });
      } catch (error) {
        console.error('Не удалось обновить шаг формы', error);
      }
    },
    [formId],
  );

  const value = useMemo<FormContextValue>(
    () => ({
      form,
      sections,
      isLoading,
      isSaving,
      currentStep,
      refresh,
      updateSection,
      setSectionCompletion,
      saveSection,
      saveAllSections,
      goToStep,
    }),
    [
      form,
      sections,
      isLoading,
      isSaving,
      currentStep,
      refresh,
      updateSection,
      setSectionCompletion,
      saveSection,
      saveAllSections,
      goToStep,
    ],
  );

  return <FormContext.Provider value={value}>{children}</FormContext.Provider>;
};

export const useFormContext = (): FormContextValue => {
  const context = useContext(FormContext);
  if (!context) {
    throw new Error('useFormContext must be used within FormProvider');
  }
  return context;
};

export const useFormSection = <T extends Record<string, unknown>>(
  sectionKey: SectionKey,
  defaults: T,
) => {
  const { sections, updateSection, setSectionCompletion, saveSection } =
    useFormContext();
  const section = sections[sectionKey] ?? createDefaultSectionState(sectionKey);

  const data = useMemo(
    () => ({
      ...defaults,
      ...(section.data as Partial<T>),
    }),
    [defaults, section.data],
  );

  const setData = useCallback(
    (patch: Partial<T> | ((prev: T) => T)) => {
      updateSection(sectionKey, (prev) => {
        const base = prev as T;
        const next =
          typeof patch === 'function' ? patch({ ...defaults, ...base }) : patch;
        return mergeSectionData(base, next as Record<string, unknown>);
      });
    },
    [defaults, sectionKey, updateSection],
  );

  const setCompleted = useCallback(
    (value: boolean) => {
      setSectionCompletion(sectionKey, value);
    },
    [sectionKey, setSectionCompletion],
  );

  return {
    data,
    setData,
    isCompleted: section.isCompleted,
    dirty: section.dirty,
    setCompleted,
    save: () => saveSection(sectionKey),
  };
};
