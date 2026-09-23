import { useState, type FormEvent } from 'react';
import { ArrowRight, ShieldCheck } from 'lucide-react';
import { useAuth } from '../auth';
import { errorMessage } from '../api';
import { Brand, ServiceBar } from '../components/Layout';
import { ErrorBanner } from '../components/Common';

export function LoginPage() {
  const { login, error: connectionError } = useAuth();
  const [email, setEmail] = useState(''); const [password, setPassword] = useState('');
  const [busy, setBusy] = useState(false); const [error, setError] = useState('');
  async function submit(event: FormEvent) {
    event.preventDefault(); setBusy(true); setError('');
    try { await login(email, password); } catch (problem) { setError(errorMessage(problem)); }
    finally { setBusy(false); }
  }
  return <div className="login-page"><ServiceBar /><main className="login-main"><section className="login-form-wrap" aria-labelledby="login-title"><Brand /><div className="login-heading"><span className="eyebrow">AUTHORIZED ACCESS</span><h1 id="login-title">Officer sign in</h1><p>Access the packaged-product inspection workspace.</p></div><ErrorBanner message={error || connectionError} /><form onSubmit={submit}><label>Email address<input type="email" autoComplete="username" required value={email} onChange={event => setEmail(event.target.value)} placeholder="name@organisation.in" /></label><label>Password<input type="password" autoComplete="current-password" required value={password} onChange={event => setPassword(event.target.value)} placeholder="Enter your password" /></label><button className="button primary login-submit" disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}<ArrowRight size={18} /></button></form><div className="login-access"><ShieldCheck size={19} /><p>Access is limited to authorized inspection and review accounts.</p></div><div className="scope-note"><strong>Prototype decision-support application</strong><p>Automated checks cover a limited declaration set. Findings require officer verification and are not legal certification.</p></div></section></main><footer className="login-footer"><span>CompliSense research prototype.</span><span>Human verification required.</span></footer></div>;
}
