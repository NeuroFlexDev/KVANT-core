import type { ComponentType } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router-dom';
import GeneralProvisions from '../../Components/StepsProvisions/GeneralProvisions/GeneralProvisions';
import MainArchitecture from '../../Components/StepsProvisions/MainArchitecture/MainArchitecture';
import Footer from '../../Components/ElementUi/Footer/Footer';
import SummaryInfo from '../../Components/StepsProvisions/SummaryInfo/SummaryInfo';
import EngineeringSolution from '../../Components/StepsProvisions/EngineeringSolution/EngineeringSolution';
import CompositionSolution from '../../Components/StepsProvisions/CompositionSection/CompositionSection';
import styles from './mainPage.module.css';
import { FormProvider, useFormContext } from '../../contexts/FormContext';
import type { SectionKey } from '../../contexts/FormContext';

const STEP_COMPONENTS: { key: SectionKey; Component: ComponentType }[] = [
  { key: 'general', Component: GeneralProvisions },
  { key: 'architecture', Component: MainArchitecture },
  { key: 'summary', Component: SummaryInfo },
  { key: 'engineering', Component: EngineeringSolution },
  { key: 'composition', Component: CompositionSolution },
];

function FormContent() {
  const {
    form,
    currentStep,
    goToStep,
    saveSection,
    saveAllSections,
    sections,
    isLoading,
    isSaving,
  } = useFormContext();
  const navigate = useNavigate();

  const stepsCount = STEP_COMPONENTS.length;
  const StepEntry = STEP_COMPONENTS[currentStep] ?? STEP_COMPONENTS[0];
  const StepComponent = StepEntry.Component;
  const activeKey = StepEntry.key;
  const isDirty = sections[activeKey]?.dirty ?? false;

  if (isLoading) {
    return (
      <div className={styles.loading}>
        Загрузка опросника...
      </div>
    );
  }

  const handleStepChange = (nextStep: number) => {
    if (
      nextStep < 0 ||
      nextStep >= stepsCount ||
      nextStep === currentStep ||
      isSaving
    ) {
      return;
    }

    const currentKey =
      STEP_COMPONENTS[currentStep]?.key ?? STEP_COMPONENTS[0].key;

    void (async () => {
      if (sections[currentKey]?.dirty) {
        await saveSection(currentKey);
      }
      await goToStep(nextStep);
    })();
  };

  const handleExit = () => {
    if (isSaving) {
      return;
    }
    const currentKey = STEP_COMPONENTS[currentStep]?.key ?? STEP_COMPONENTS[0].key;
    void (async () => {
      if (sections[currentKey]?.dirty) {
        await saveSection(currentKey);
      }
      navigate('/', { replace: true });
    })();
  };

  const handleSave = () => {
    if (isSaving) {
      return;
    }
    void (async () => {
      await saveSection(activeKey);
    })();
  };

  const handleCalculate = () => {
    if (isSaving) {
      return;
    }
    void (async () => {
      await saveAllSections();
    })();
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.headerInfo}>
          <h1 className={styles.title}>{form?.title ?? 'Опросник'}</h1>
          <p className={styles.caption}>
            Шаг {currentStep + 1} из {stepsCount}
          </p>
        </div>
        <div className={styles.headerActions}>
          <button
            className={styles.exitButton}
            type="button"
            onClick={handleExit}
            disabled={isSaving}
          >
            К списку опросников
          </button>
        </div>
      </header>

      <div className={styles.content}>
        <StepComponent />
      </div>

      <Footer
        currentStep={currentStep}
        totalSteps={stepsCount}
        onStepChange={handleStepChange}
        onSave={handleSave}
        onCalculate={handleCalculate}
        saveDisabled={isSaving || !isDirty}
        calculateDisabled={isSaving}
      />
    </div>
  );
}

export default function MainPage() {
  const params = useParams<{ formId: string }>();
  const formIdParam = params.formId;

  if (!formIdParam) {
    return <Navigate to="/" replace />;
  }

  const formId = Number(formIdParam);
  if (Number.isNaN(formId)) {
    return <Navigate to="/" replace />;
  }

  return (
    <FormProvider formId={formId}>
      <FormContent />
    </FormProvider>
  );
}
