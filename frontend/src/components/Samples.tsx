import { useEffect, useState } from 'react';
import { ArrowDownToLine, FlaskConical } from 'lucide-react';
import { api, errorMessage } from '../api';
import type { Sample } from '../types';

export function Samples() {
  const [samples, setSamples] = useState<Sample[]>([]); const [error, setError] = useState('');
  useEffect(() => { api.samples().then(setSamples).catch(problem => setError(errorMessage(problem))); }, []);
  return <section className="samples-block"><div><FlaskConical size={22} /><span className="eyebrow">TRY THE WORKFLOW</span><h3>Start with a synthetic label.</h3><p>Download a sample, create an inspection, and upload it to run real OCR. These are fictional labels for testing.</p></div><div className="sample-links">{error && <p className="small muted">Sample downloads unavailable. {error}</p>}{!error && !samples.length && <p className="small muted">Loading sample labels…</p>}{samples.map(sample => <a key={sample.url} href={sample.url} download><span><strong>{sample.name}</strong><small>{sample.description}</small></span><ArrowDownToLine size={18} /></a>)}</div></section>;
}
