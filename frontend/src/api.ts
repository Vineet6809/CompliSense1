import type { AuthResponse, DashboardData, Inspection, InspectionInput, InspectionPatch, InspectionSummary, RulesData, Sample } from './types';

let csrfToken = '';
const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');
export function setCsrfToken(token: string) { csrfToken = token; }
export class ApiError extends Error {
  constructor(message: string, public status: number) { super(message); }
}

// Cookies authenticate requests; the separate token protects every signed-in mutation.
async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json');
  if (options.method && options.method !== 'GET' && csrfToken) headers.set('X-CSRF-Token', csrfToken);
  let response: Response;
  try { response = await fetch(`${API_BASE}/api${path}`, { ...options, headers, credentials: 'include' }); }
  catch { throw new ApiError('The server could not be reached. Check that the backend is running, then try again.', 0); }
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = data?.detail;
    const message = typeof detail === 'string' ? detail : Array.isArray(detail)
      ? detail.map((item: { loc?: string[]; msg: string }) => `${item.loc?.slice(1).join('.') || 'Input'}: ${item.msg}`).join('; ')
      : `Request failed (${response.status}). Please try again.`;
    throw new ApiError(message, response.status);
  }
  return data as T;
}

export const api = {
  me: () => request<AuthResponse>('/auth/me'),
  login: (email: string, password: string) => request<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  logout: () => request<{ message: string }>('/auth/logout', { method: 'POST' }),
  dashboard: () => request<DashboardData>('/dashboard'),
  inspections: (q = '', status = '') => request<InspectionSummary[]>(`/inspections?${new URLSearchParams({ q, status })}`),
  inspection: (id: string) => request<Inspection>(`/inspections/${id}`),
  create: (input: InspectionInput) => request<Inspection>('/inspections', { method: 'POST', body: JSON.stringify(input) }),
  update: (id: string, input: InspectionPatch) => request<Inspection>(`/inspections/${id}`, { method: 'PATCH', body: JSON.stringify(input) }),
  upload: (id: string, file: File, panel: string) => {
    const body = new FormData(); body.append('file', file); body.append('panel', panel);
    return request<Inspection>(`/inspections/${id}/images`, { method: 'POST', body });
  },
  analyze: (id: string) => request<Inspection>(`/inspections/${id}/analyze`, { method: 'POST' }),
  review: (id: string, version: number, decision: string, notes: string) => request<Inspection>(`/inspections/${id}/review`, { method: 'POST', body: JSON.stringify({ version, decision, notes }) }),
  rules: () => request<RulesData>('/rules'),
  samples: () => request<Sample[]>('/samples'),
  health: () => request<{ status: string; ocr_available: boolean; ocr_engine: string }>('/health'),
};

export function errorMessage(error: unknown) {
  if (error instanceof ApiError && error.status === 409) return 'This record changed since you opened it. Reload the latest record, then apply your changes again.';
  return error instanceof Error ? error.message : 'Something went wrong. Please try again.';
}
