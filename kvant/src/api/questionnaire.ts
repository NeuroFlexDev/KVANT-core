import apiClient from './client';

export interface SectionProgress {
  total: number;
  completed: number;
}

export interface QuestionnaireSection {
  id: number;
  form_id: number;
  section_key: string;
  title?: string | null;
  order_index: number;
  data: Record<string, unknown>;
  is_completed: boolean;
  completed_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface QuestionnaireFormSummary {
  id: number;
  guid: string;
  title: string;
  description?: string | null;
  status: string;
  current_step: number;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  progress: SectionProgress;
}

export interface QuestionnaireFormDetail
  extends Omit<QuestionnaireFormSummary, 'progress'> {
  sections: QuestionnaireSection[];
}

export interface SectionPayloadInput {
  section_key: string;
  title?: string;
  order_index?: number;
  data?: Record<string, unknown>;
  is_completed?: boolean;
  completed_at?: string;
}

export interface CreateFormPayload {
  title: string;
  description?: string;
  status?: string;
  current_step?: number;
  metadata?: Record<string, unknown>;
  sections?: SectionPayloadInput[];
}

export interface UpdateFormPayload {
  title?: string;
  description?: string;
  status?: string;
  current_step?: number;
  metadata?: Record<string, unknown>;
}

export interface UpsertSectionPayload {
  title?: string;
  order_index?: number;
  data?: Record<string, unknown>;
  is_completed?: boolean;
  completed_at?: string;
}

export const questionnaireApi = {
  async listForms(): Promise<QuestionnaireFormSummary[]> {
    const { data } = await apiClient.get<QuestionnaireFormSummary[]>('/questionnaire/forms');
    return data;
  },

  async createForm(payload: CreateFormPayload): Promise<QuestionnaireFormDetail> {
    const { data } = await apiClient.post<QuestionnaireFormDetail>('/questionnaire/forms', payload);
    return data;
  },

  async getForm(formId: number): Promise<QuestionnaireFormDetail> {
    const { data } = await apiClient.get<QuestionnaireFormDetail>(`/questionnaire/forms/${formId}`);
    return data;
  },

  async updateForm(formId: number, payload: UpdateFormPayload): Promise<QuestionnaireFormDetail> {
    const { data } = await apiClient.patch<QuestionnaireFormDetail>(`/questionnaire/forms/${formId}`, payload);
    return data;
  },

  async deleteForm(formId: number): Promise<QuestionnaireFormSummary> {
    const { data } = await apiClient.delete<QuestionnaireFormSummary>(`/questionnaire/forms/${formId}`);
    return data;
  },

  async upsertSection(
    formId: number,
    sectionKey: string,
    payload: UpsertSectionPayload,
  ): Promise<QuestionnaireSection> {
    const { data } = await apiClient.put<QuestionnaireSection>(
      `/questionnaire/forms/${formId}/sections/${sectionKey}`,
      payload,
    );
    return data;
  },
};
