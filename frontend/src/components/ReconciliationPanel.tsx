import { AlertTriangle, CheckCircle2, GitCompare } from 'lucide-react';
import type { Inspection } from '../types';

export function ReconciliationPanel({ inspection }: { inspection: Inspection }) {
  const quantity = inspection.reconciliation?.net_quantity;
  if (!quantity?.candidates?.length) return null;
  const conflict = quantity.status === 'conflict';
  return <section className={`reconciliation-panel ${conflict ? 'conflict' : 'consistent'}`} aria-labelledby="reconciliation-heading">
    <div className="reconciliation-icon">{conflict ? <AlertTriangle size={18} /> : <CheckCircle2 size={18} />}</div>
    <div className="reconciliation-body">
      <div className="reconciliation-heading"><div><span className="eyebrow">MULTI-VIEW RECONCILIATION</span><h3 id="reconciliation-heading">Net quantity across supplied views</h3></div><GitCompare size={19} /></div>
      <p>{conflict ? 'Different quantity declarations were found. Resolve the package views before deciding whether the declaration is compliant.' : 'The supplied views agree on the normalized net quantity. Keep the original images available for the final review.'}</p>
      <div className="reconciliation-values">{quantity.candidates.map((candidate, index) => <div className="reconciliation-value" key={`${candidate.image_id}-${index}`}><span>{candidate.panel || 'other'} view</span><strong>{candidate.value}</strong><small>{Math.round(candidate.confidence * 100)}% OCR</small></div>)}</div>
      {conflict && <div className="reconciliation-action">Review the highlighted evidence and record the verified value in the declarations panel.</div>}
    </div>
  </section>;
}
