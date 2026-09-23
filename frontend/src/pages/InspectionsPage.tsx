import { useEffect, useState } from 'react';
import { Plus, Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import { api, errorMessage } from '../api';
import { EmptyState, ErrorBanner, InspectionTable, Spinner } from '../components/Common';
import type { InspectionSummary } from '../types';

export function InspectionsPage() {
  const [items, setItems] = useState<InspectionSummary[]>([]);
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [retry, setRetry] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    const timer = setTimeout(() => {
      api.inspections(query, status)
        .then(data => { if (!cancelled) setItems(data); })
        .catch(problem => { if (!cancelled) setError(errorMessage(problem)); })
        .finally(() => { if (!cancelled) setLoading(false); });
    }, 250);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [query, status, retry]);

  return (
    <div className="page">
      <div className="page-heading">
        <div>
          <span className="eyebrow">RECORDS AND CASES</span>
          <h1>Inspection register</h1>
          <p>Search product records, check their status, and resume an inspection.</p>
        </div>
        <Link to="/inspections/new" className="button primary"><Plus size={18} />New inspection</Link>
      </div>

      <div className="filter-bar">
        <label className="search-input">
          <Search size={18} />
          <input aria-label="Search inspections" placeholder="Search product, brand, or barcode…" value={query} onChange={event => setQuery(event.target.value)} />
        </label>
        <label className="filter-select">
          <span>Status</span>
          <select value={status} onChange={event => setStatus(event.target.value)}>
            <option value="">All statuses</option>
            <option value="draft">Draft</option>
            <option value="processing">Processing</option>
            <option value="ready">Ready for review</option>
            <option value="reviewed">Reviewed</option>
            <option value="failed">Processing failed</option>
          </select>
        </label>
        {(query || status) && <button className="text-button clear-filters" type="button" onClick={() => { setQuery(''); setStatus(''); }}>Clear filters</button>}
      </div>

      <ErrorBanner message={error} retry={() => setRetry(value => value + 1)} />
      {loading ? <Spinner label="Loading inspections…" /> : !error && (
        items.length ? (
          <>
            <div className="result-count">Showing {items.length} {items.length === 1 ? 'inspection' : 'inspections'}</div>
            <InspectionTable inspections={items} />
          </>
        ) : (
          <EmptyState title={query || status ? 'No matching inspections.' : 'Your register is ready.'}>
            {query || status ? 'Try another search or choose a different status.' : 'Create an inspection to begin collecting product evidence.'}
          </EmptyState>
        )
      )}
    </div>
  );
}
