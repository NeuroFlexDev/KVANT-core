import apiClient from './client';

export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  exp: string;
}

export interface RefreshResponse {
  access: string;
  exp: string;
}

export const authApi = {
  async login(payload: LoginPayload): Promise<LoginResponse> {
    const { data } = await apiClient.post<LoginResponse>('/auth/login', payload);
    return data;
  },

  async refresh(refreshToken: string): Promise<RefreshResponse> {
    const { data } = await apiClient.post<RefreshResponse>(
      '/auth/refresh_token',
      null,
      { params: { refresh_token: refreshToken } },
    );
    return data;
  },
};
