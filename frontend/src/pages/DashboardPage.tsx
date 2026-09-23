import { useEffect, useState } from 'react';
import { ArrowRight, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api, errorMessage } from '../api';
import { useAuth } from '../auth';
import { EmptyState, ErrorBanner, InspectionTable, Spinner } from '../components/Common';
import type { DashboardData } from '../types';

export function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null); const [error, setError] = useState('');
  function load() { setError(''); api.dashboard().then(setData).catch(problem => setError(errorMessage(problem))); }
  useEffect(load, []);
  return <div className="page dashboard-page"><div className="page-heading"><div><span className="eyebrow">OPERATIONAL OVERVIEW</span><h1>Inspection desk</h1><p>Welcome, {user?.name.split(' ')[0]}. Review current cases and continue work requiring attention.</p></div><Link to="/inspections/new" className="button primary"><Plus size={18} />New inspection</Link></div>
    <ErrorBanner message={error} retry={load} />
    {!data && !error ? <Spinner /> : data && <><section className="metrics" aria-label="Inspection statistics"><div><span>Total inspections</span><strong>{data.total.toString().padStart(2, '0')}</strong><small>{user?.role === 'reviewer' ? 'Across the workspace' : 'Assigned workspace records'}</small></div><div><span>Needs verification</span><strong>{data.needs_review.toString().padStart(2, '0')}<i className="metric-dot amber" /></strong><small>Evidence requiring officer review</small></div><div><span>Potential violations</span><strong>{data.potential_violations.toString().padStart(2, '0')}<i className="metric-dot rust" /></strong><small>Pending human assessment</small></div><div><span>Reviewed</span><strong>{data.reviewed.toString().padStart(2, '0')}<i className="metric-dot teal" /></strong><small>Reviewer decision recorded</small></div></section>
    <section className="workspace-section"><div className="section-heading"><div><span className="eyebrow">RECENT RECORDS</span><h2>Recent inspections</h2></div><Link className="text-link" to="/inspections">Open register <ArrowRight size={16} /></Link></div>{data.recent.length ? <InspectionTable inspections={data.recent} /> : <EmptyState title="No inspections recorded." action={<Link className="button primary" to="/inspections/new"><Plus size={17} />Create inspection</Link>}>Create an inspection to begin collecting product evidence.</EmptyState>}</section></>}
  </div>;
}
