import { useEffect, useRef, useState } from 'react';
import { ArrowLeft, Check, ChevronRight, LoaderCircle, Play, Plus, RefreshCw, Upload } from 'lucide-react';
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { api, errorMessage } from '../api';
import { ErrorBanner, formatDate, Spinner, StatusBadge, SuccessBanner } from '../components/Common';
import { EvidenceViewer, type EvidenceSelection } from '../components/EvidenceViewer';
import { DeclarationsEditor } from '../components/DeclarationsEditor';
import { ContextEditor } from '../components/ContextEditor';
import { AssessmentPanel } from '../components/AssessmentPanel';
import { AuditTrail, ReportHistory } from '../components/ReportHistory';
import { UploadPicker, type PendingImage } from '../components/UploadPicker';
import { ReconciliationPanel } from '../components/ReconciliationPanel';
import type { Inspection, InspectionPatch } from '../types';

export function InspectionPage() {
  const { id = '' } = useParams(); const location = useLocation(); const navigate = useNavigate();
  const initialNotice = location.state as { message?: string; error?: string } | null;
  const [inspection, setInspection] = useState<Inspection | null>(null);
  const [error, setError] = useState(initialNotice?.error || ''); const [success, setSuccess] = useState(initialNotice?.message || '');
  const [loading, setLoading] = useState(true); const [busy, setBusy] = useState(false);
  const [tab, setTab] = useState('evidence'); const [selection, setSelection] = useState<EvidenceSelection | null>(null);
  const [files, setFiles] = useState<PendingImage[]>([]); const [uploadOpen, setUploadOpen] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(''); const evidenceRef = useRef<HTMLDivElement>(null);
  const status = inspection?.status;
  useEffect(() => {
    if (location.state) navigate(location.pathname, { replace: true, state: null });
  }, [location.pathname, location.state, navigate]);
  async function load() {
    setError('');
    try { setInspection(await api.inspection(id)); } catch (problem) { setError(errorMessage(problem)); }
    finally { setLoading(false); }
  }
  useEffect(() => {
    let cancelled = false; setLoading(true);
    api.inspection(id).then(data => { if (!cancelled) setInspection(data); }).catch(problem => { if (!cancelled) setError(errorMessage(problem)); }).finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [id]);
  useEffect(() => {
    if (status !== 'processing') return;
    let cancelled = false;
    // Schedule the next poll only after this request finishes, avoiding overlapping requests.
    let timer: ReturnType<typeof setTimeout>;
    async function poll() {
      try { const next = await api.inspection(id); if (cancelled) return; setInspection(next); setError(''); if (next.status !== 'processing') { if (next.status !== 'failed') setSuccess('Analysis complete. Verify declarations and review the assessment.'); return; } }
      catch (problem) { if (!cancelled) setError(errorMessage(problem)); }
      if (!cancelled) timer = setTimeout(() => void poll(), 2500);
    }
    timer = setTimeout(() => void poll(), 1500);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [id, status]);
  async function save(patch: InspectionPatch) {
    setBusy(true); setError(''); setSuccess('');
    try { setInspection(await api.update(id, patch)); setSuccess('Changes saved. The assessment reflects the current evidence and context.'); return true; }
    catch (problem) { setError(errorMessage(problem)); return false; }
    finally { setBusy(false); }
  }
  async function analyze() {
    setBusy(true); setError(''); setSuccess('');
    try { setInspection(await api.analyze(id)); }
    catch (problem) { setError(errorMessage(problem)); }
    finally { setBusy(false); }
  }
  async function upload() {
    setBusy(true); setError(''); setSuccess('');
    const pending = [...files];
    try {
      for (let index = 0; index < pending.length; index++) {
        setUploadProgress(`Uploading ${index + 1} of ${pending.length}…`);
        setInspection(await api.upload(id, pending[index].file, pending[index].panel));
        setFiles(current => current.filter(file => file.key !== pending[index].key));
      }
      setUploadOpen(false); setSuccess('Evidence added. Run analysis to assess the updated image set.');
    } catch (problem) { setError(errorMessage(problem)); }
    finally { setBusy(false); setUploadProgress(''); }
  }
  async function review(decision: string, notes: string) {
    if (!inspection) return false;
    setBusy(true); setError(''); setSuccess('');
    try { setInspection(await api.review(id, inspection.version, decision, notes)); setSuccess('Reviewer decision recorded. The report history has been updated.'); return true; }
    catch (problem) { setError(errorMessage(problem)); return false; }
    finally { setBusy(false); }
  }
  function selectEvidence(next: EvidenceSelection) { setSelection(next); setTab('evidence'); setTimeout(() => evidenceRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 60); }
  if (loading) return <Spinner label="Opening inspection…" />;
  if (!inspection) return <div className="page"><Link className="back-link" to="/inspections"><ArrowLeft size={15} />Inspection register</Link><ErrorBanner message={error || 'This inspection is not available.'} retry={() => void load()} /></div>;
  const processing = inspection.status === 'processing';
  return <div className="page inspection-page"><Link className="back-link" to="/inspections"><ArrowLeft size={15} />Inspection register</Link><div className="page-heading inspection-heading"><div><div className="inspection-id"><span className="eyebrow">INSPECTION / {id.slice(0, 8).toUpperCase()}</span><StatusBadge status={inspection.status} /></div><h1>{inspection.product_name}</h1><p>{inspection.brand || 'Brand not entered'} <b>·</b> {inspection.owner_name} <b>·</b> Created {formatDate(inspection.created_at)}</p></div><button className="button primary" disabled={busy || processing || inspection.images.length === 0} onClick={() => void analyze()}>{processing ? <LoaderCircle className="spin" size={17} /> : inspection.current_assessment_id ? <RefreshCw size={17} /> : <Play size={17} />}{processing ? 'Processing evidence…' : inspection.status === 'failed' ? 'Retry analysis' : inspection.current_assessment_id ? 'Run analysis again' : 'Run analysis'}</button></div>
    <div className="inspection-steps" aria-label="Inspection progress"><span className={inspection.images.length ? 'complete' : 'current'}><i>{inspection.images.length ? <Check size={13} /> : '1'}</i>Capture evidence</span><ChevronRight size={15} /><span className={inspection.current_assessment_id ? 'complete' : inspection.images.length ? 'current' : ''}><i>{inspection.current_assessment_id ? <Check size={13} /> : '2'}</i>Verify declarations</span><ChevronRight size={15} /><span className={inspection.review_decision ? 'complete' : inspection.current_assessment_id ? 'current' : ''}><i>{inspection.review_decision ? <Check size={13} /> : '3'}</i>Review & document</span></div>
    <ErrorBanner message={error} retry={() => void load()} />{success && <SuccessBanner>{success}</SuccessBanner>}{processing && <div className="processing-notice" role="status"><LoaderCircle size={23} className="spin" /><div><strong>Reading the packaging evidence.</strong><p>OCR and declaration checks run on the server. This page updates automatically; you can safely return later.</p></div></div>}{inspection.status === 'failed' && <ErrorBanner message={inspection.processing_error || 'Analysis failed. Check your images and retry the analysis.'} />}
    <ContextEditor inspection={inspection} busy={busy} onSave={save} />
    <div className="inspection-tabs" role="tablist" aria-label="Inspection sections">{[{ key: 'evidence', label: 'Evidence & declarations', count: inspection.images.length }, { key: 'assessment', label: 'Assessment & review', count: inspection.findings.length }, { key: 'reports', label: 'Report history', count: inspection.assessments.length }, { key: 'activity', label: 'Activity' }].map(item => <button id={`tab-${item.key}`} key={item.key} role="tab" aria-selected={tab === item.key} aria-controls={`panel-${item.key}`} onClick={() => setTab(item.key)}>{item.label}{item.count !== undefined && <span>{item.count}</span>}</button>)}</div>
    <div role="tabpanel" id={`panel-${tab}`} aria-labelledby={`tab-${tab}`}>
      {tab === 'evidence' && <><div className="evidence-section-head"><div><h2>The evidence workspace</h2><p>Images and declarations, side by side. Saved edits create a traceable record.</p></div><button className="button secondary small-button" disabled={processing || busy || inspection.images.length >= 8} onClick={() => setUploadOpen(value => !value)}><Plus size={16} />{uploadOpen ? 'Close uploader' : 'Add images'}</button></div><ReconciliationPanel inspection={inspection} />{(uploadOpen || !inspection.images.length) && <div className="detail-uploader"><UploadPicker files={files} onChange={setFiles} existingCount={inspection.images.length} disabled={processing || busy} />{files.length > 0 && <div className="form-actions"><p className="small muted">Adding evidence clears the current assessment until analysis runs again.</p><button className="button primary" disabled={busy || processing} onClick={() => void upload()}><Upload size={16} />{uploadProgress || `Upload ${files.length} image${files.length > 1 ? 's' : ''}`}</button></div>}</div>}<div className="evidence-workspace" ref={evidenceRef}><div className="evidence-column"><EvidenceViewer images={inspection.images} selection={selection} onSelect={setSelection} /><div className="evidence-reminder"><strong>Keep the original in view.</strong><p>OCR is a starting point. Read the highlighted region, correct uncertain values, and record where your evidence came from.</p></div></div><DeclarationsEditor inspection={inspection} busy={busy} onSave={save} onSelect={selectEvidence} /></div></>}
      {tab === 'assessment' && <AssessmentPanel inspection={inspection} busy={busy} onSave={save} onSelect={selectEvidence} onReview={review} />}
      {tab === 'reports' && <ReportHistory inspection={inspection} />}
      {tab === 'activity' && <AuditTrail inspection={inspection} />}
    </div>
  </div>;
}
