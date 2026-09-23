import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { api, ApiError, errorMessage, setCsrfToken } from './api';
import type { User } from './types';

interface AuthState { user: User | null; loading: boolean; error: string; login: (email: string, password: string) => Promise<void>; logout: () => Promise<void>; refresh: () => Promise<void> }
const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  async function refresh() {
    setLoading(true); setError('');
    try { const data = await api.me(); setUser(data.user); setCsrfToken(data.csrf_token); }
    catch (problem) { if (!(problem instanceof ApiError && problem.status === 401)) setError(errorMessage(problem)); }
    finally { setLoading(false); }
  }
  useEffect(() => { void refresh(); }, []);
  async function login(email: string, password: string) {
    const data = await api.login(email, password); setCsrfToken(data.csrf_token); setUser(data.user); setError('');
  }
  async function logout() { await api.logout(); setUser(null); setCsrfToken(''); }
  return <AuthContext.Provider value={{ user, loading, error, login, logout, refresh }}>{children}</AuthContext.Provider>;
}
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('AuthProvider is required.');
  return context;
}
