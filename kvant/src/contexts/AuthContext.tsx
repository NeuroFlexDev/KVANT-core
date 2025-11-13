import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import type { ReactNode } from 'react';
import { AxiosError } from 'axios';

import apiClient from '../api/client';
import { authApi } from '../api/auth';

interface AuthContextValue {
  isAuthenticated: boolean;
  accessToken: string | null;
  userEmail: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const ACCESS_TOKEN_KEY = 'authToken';
const REFRESH_TOKEN_KEY = 'refreshToken';

const decodeEmail = (token: string | null): string | null => {
  if (!token) {
    return null;
  }
  try {
    const payload = JSON.parse(atob(token.split('.')[1] ?? ''));
    return typeof payload.email === 'string' ? payload.email : null;
  } catch (error) {
    return null;
  }
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [accessToken, setAccessToken] = useState<string | null>(
    () => localStorage.getItem(ACCESS_TOKEN_KEY),
  );
  const [refreshToken, setRefreshToken] = useState<string | null>(
    () => localStorage.getItem(REFRESH_TOKEN_KEY),
  );
  const [userEmail, setUserEmail] = useState<string | null>(() =>
    decodeEmail(localStorage.getItem(ACCESS_TOKEN_KEY)),
  );

  const isRefreshing = useRef(false);

  const persistTokens = useCallback((access: string | null, refresh: string | null) => {
    if (access) {
      localStorage.setItem(ACCESS_TOKEN_KEY, access);
    } else {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
    }

    if (refresh) {
      localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
    } else {
      localStorage.removeItem(REFRESH_TOKEN_KEY);
    }

    setAccessToken(access);
    setRefreshToken(refresh);
    setUserEmail(decodeEmail(access));
  }, []);

  const logout = useCallback(() => {
    persistTokens(null, null);
  }, [persistTokens]);

  const login = useCallback(
    async (email: string, password: string) => {
      const response = await authApi.login({ email, password });
      persistTokens(response.access, response.refresh);
    },
    [persistTokens],
  );

  useEffect(() => {
    const requestInterceptor = apiClient.interceptors.request.use((config) => {
      if (accessToken) {
        config.headers = config.headers ?? {};
        (config.headers as Record<string, string>)['X-Auth-Token'] = accessToken;
      }
      return config;
    });

    const responseInterceptor = apiClient.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config;

        if (
          error.response?.status === 401 &&
          refreshToken &&
          originalRequest &&
          !isRefreshing.current
        ) {
          try {
            isRefreshing.current = true;
            const { access } = await authApi.refresh(refreshToken);
            persistTokens(access, refreshToken);
            originalRequest.headers = originalRequest.headers ?? {};
            (originalRequest.headers as Record<string, string>)['X-Auth-Token'] = access;
            return apiClient(originalRequest);
          } catch (refreshError) {
            logout();
            return Promise.reject(refreshError);
          } finally {
            isRefreshing.current = false;
          }
        }

        return Promise.reject(error);
      },
    );

    return () => {
      apiClient.interceptors.request.eject(requestInterceptor);
      apiClient.interceptors.response.eject(responseInterceptor);
    };
  }, [accessToken, refreshToken, logout, persistTokens]);

  const value = useMemo<AuthContextValue>(
    () => ({
      isAuthenticated: Boolean(accessToken),
      accessToken,
      userEmail,
      login,
      logout,
    }),
    [accessToken, login, logout, userEmail],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
