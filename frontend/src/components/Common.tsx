import { AlertCircle, ArrowUpRight, Check, FileSearch, LoaderCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { ReactNode } from 'react';
import type { InspectionSummary } from '../types';

export function Spinner({ label = 'Loading workspace…' }: { label?: string }) {
  return <div className="loading" role="status"><LoaderCircle className="spin" size={20} /><span>{label}</span></div>;
}
export function ErrorBanner({ message, retry }: { message: string; retry?: () => void }) {
  if (!message) return null;
  return <div className="notice error" role="alert"><AlertCircle size={18} /><div>{message}{retry && <button type="button" className="text-button" onClick={retry}>Reload latest record</button>}</div></div>;
}
export function SuccessBanner({ children }: { children: ReactNode }) {
  return <div className="notice success" role="status"><Check size={18} /><div>{children}</div></div>;
}
export function EmptyState({ title, children, action }: { title: string; children: ReactNode; action?: ReactNode }) {
  return <div className="empty-state"><div className="empty-icon"><FileSearch size={32} strokeWidth={1.25} /></div><h3>{title}</h3><p>{children}</p>{action}</div>;
}
const statusLabels: Record<string, string> = { draft: 'Draft', processing: 'Processing', ready: 'Ready for review', reviewed: 'Reviewed', failed: 'Processing failed', pass: 'Check passed', potential_violation: 'Potential violation', needs_review: 'Needs review', not_applicable: 'Not applicable', accepted: 'Accepted', follow_up: 'Follow-up needed' };
export function StatusBadge({ status }: { status: string }) {
  return <span className={`status-badge status-${status}`}>{status === 'processing' ? <LoaderCircle size={12} className="spin" /> : <i />}{statusLabels[status] || status.replaceAll('_', ' ')}</span>;
}
export function formatDate(value: string, includeTime = false) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat('en-IN', { day: '2-digit', month: 'short', year: 'numeric', ...(includeTime ? { hour: '2-digit', minute: '2-digit' } : {}) }).format(date);
}
export function InspectionTable({ inspections }: { inspections: InspectionSummary[] }) {
  return <div className="table-scroll"><table className="inspection-table"><thead><tr><th>Product / inspection</th><th>Status</th><th>Evidence</th><th>Owner</th><th>Updated</th><th><span className="sr-only">Open</span></th></tr></thead><tbody>{inspections.map(item => <tr key={item.id}>
    <td data-label="Product / inspection"><Link className="product-link" to={`/inspections/${item.id}`}>{item.product_name}<span>{item.brand || 'Brand not entered'} <b>·</b> {item.id.slice(0, 8).toUpperCase()}</span></Link></td>
    <td data-label="Status"><StatusBadge status={item.status} />{item.review_decision === 'follow_up' && <span className="table-detail">Follow-up needed</span>}</td>
    <td data-label="Evidence">{item.image_count} {item.image_count === 1 ? 'image' : 'images'}<span className="table-detail">{item.potential_violations ? `${item.potential_violations} potential concern${item.potential_violations === 1 ? '' : 's'}` : item.needs_review ? `${item.needs_review} to verify` : '—'}</span></td>
    <td data-label="Owner">{item.owner_name}</td><td data-label="Updated" className="nowrap muted">{formatDate(item.updated_at)}</td><td data-label="Open"><Link className="icon-button" to={`/inspections/${item.id}`} aria-label={`Open ${item.product_name}`}><ArrowUpRight size={18} /></Link></td>
  </tr>)}</tbody></table></div>;
}
