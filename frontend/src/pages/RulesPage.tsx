import { useEffect, useState } from 'react';
import { BookOpen, ExternalLink } from 'lucide-react';
import { api, errorMessage } from '../api';
import { ErrorBanner, Spinner } from '../components/Common';
import type { RulesData } from '../types';

export function RulesPage() {
  const [data, setData] = useState<RulesData | null>(null); const [error, setError] = useState('');
  function load() { setError(''); api.rules().then(setData).catch(problem => setError(errorMessage(problem))); }
  useEffect(load, []);
  return <div className="page"><div className="page-heading"><div><span className="eyebrow">RULE REFERENCE</span><h1>Rule reference</h1><p>Current checks, applicability limits, and source references used by the inspection desk.</p></div><BookOpen size={38} strokeWidth={1.2} className="heading-icon" /></div><ErrorBanner message={error} retry={load} />{!data && !error ? <Spinner label="Loading rule reference…" /> : data && <><section className="rule-scope"><div><span className="eyebrow">CURRENT SCOPE</span><h2>{data.scope}</h2><span className="version-tag">Rule set {data.version}</span></div><div><h3>Scope and limitations</h3><ul>{data.limitations.map((limit, index) => <li key={index}>{limit}</li>)}</ul></div></section><div className="section-heading"><h2>Declaration checks</h2><span className="muted small">{data.rules.length} rules in this version</span></div><div className="rule-list">{data.rules.map((rule, index) => <article className="rule-row" key={rule.id}><span className="rule-number">{String(index + 1).padStart(2, '0')}</span><div><div className="rule-meta">{rule.id}<span>{rule.provision}</span></div><h3>{rule.title}</h3><p>{rule.description}</p></div><a className="source-link" href={rule.source_url} target="_blank" rel="noreferrer">Official source<ExternalLink size={14} /></a></article>)}</div></>}</div>;
}
