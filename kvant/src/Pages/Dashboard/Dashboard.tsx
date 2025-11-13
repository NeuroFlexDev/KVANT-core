import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { questionnaireApi } from '../../api/questionnaire';
import type { QuestionnaireFormSummary } from '../../api/questionnaire';
import { useAuth } from '../../contexts/AuthContext';

import styles from './dashboard.module.css';

const formatProgress = (progress: QuestionnaireFormSummary['progress']) => {
  if (!progress) {
    return '0%';
  }
  if (progress.total === 0) {
    return '0%';
  }
  const percent = Math.round((progress.completed / progress.total) * 100);
  return `${percent}%`;
};

export default function Dashboard() {
  const [forms, setForms] = useState<QuestionnaireFormSummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const navigate = useNavigate();
  const { userEmail, logout } = useAuth();

  const loadForms = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await questionnaireApi.listForms();
      setForms(data);
    } catch (error) {
      console.error('Не удалось загрузить формы', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadForms();
  }, [loadForms]);

  const handleCreateForm = useCallback(async () => {
    setIsCreating(true);
    try {
      const now = new Date();
      const title = `Новый опросник ${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;
      const form = await questionnaireApi.createForm({ title });
      navigate(`/forms/${form.id}`);
    } catch (error) {
      console.error('Не удалось создать форму', error);
      await loadForms();
    } finally {
      setIsCreating(false);
    }
  }, [loadForms, navigate]);

  const handleOpenForm = useCallback(
    (formId: number) => {
      navigate(`/forms/${formId}`);
    },
    [navigate],
  );

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.headerInfo}>
          <h1 className={styles.title}>Опросники</h1>
          <p className={styles.subtitle}>
            Управляйте опросными листами и продолжайте заполнение ранее
            сохраненных форм.
          </p>
        </div>
        <div className={styles.headerActions}>
          <div className={styles.userBadge}>
            <span className={styles.userName}>{userEmail ?? 'Неизвестный пользователь'}</span>
          </div>
          <button
            className={styles.secondaryButton}
            type="button"
            onClick={logout}
          >
            Выйти
          </button>
          <button
            className={styles.primaryButton}
            type="button"
            onClick={handleCreateForm}
            disabled={isCreating}
          >
            {isCreating ? 'Создание...' : 'Создать опросник'}
          </button>
        </div>
      </header>

      {isLoading ? (
        <div className={styles.emptyState}>Загрузка...</div>
      ) : forms.length === 0 ? (
        <div className={styles.emptyState}>
          <p>Пока нет сохраненных опросников.</p>
          <button
            className={styles.secondaryButton}
            type="button"
            onClick={handleCreateForm}
            disabled={isCreating}
          >
            Создать первый опросник
          </button>
        </div>
      ) : (
        <div className={styles.list}>
          {forms.map((form) => (
            <article key={form.id} className={styles.card}>
              <div className={styles.cardHeader}>
                <h2 className={styles.cardTitle}>{form.title}</h2>
                <span className={styles.status}>{form.status}</span>
              </div>
              <div className={styles.cardBody}>
                <div className={styles.detail}>
                  Прогресс:{' '}
                  <strong>{formatProgress(form.progress)}</strong>
                </div>
                <div className={styles.detail}>
                  Последнее обновление:{' '}
                  <time dateTime={form.updated_at}>
                    {new Date(form.updated_at).toLocaleString()}
                  </time>
                </div>
              </div>
              <div className={styles.cardFooter}>
                <button
                  className={styles.secondaryButton}
                  type="button"
                  onClick={() => handleOpenForm(form.id)}
                >
                  Продолжить заполнение
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
