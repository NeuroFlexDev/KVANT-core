import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuth } from '../../contexts/AuthContext';

import styles from './login.module.css';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      await login(email, password);
      navigate('/', { replace: true });
    } catch (err) {
      const message =
        (err as Error)?.message && (err as Error).message !== 'Network Error'
          ? (err as Error).message
          : 'Не удалось выполнить вход. Проверьте данные и повторите попытку.';
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <h1 className={styles.title}>Вход в личный кабинет</h1>
        <p className={styles.subtitle}>
          Используйте корпоративный email и пароль из production, предварительно синхронизировав базу.
        </p>

        <label className={styles.label} htmlFor="email">
          Email
        </label>
        <input
          id="email"
          type="email"
          className={styles.input}
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="user@example.com"
          required
        />

        <label className={styles.label} htmlFor="password">
          Пароль
        </label>
        <input
          id="password"
          type="password"
          className={styles.input}
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Введите пароль"
          required
        />

        {error && <div className={styles.error}>{error}</div>}

        <button className={styles.submit} type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Входим...' : 'Войти'}
        </button>
      </form>
    </div>
  );
}
