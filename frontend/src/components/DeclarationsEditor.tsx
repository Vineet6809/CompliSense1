import { useEffect, useState, type FormEvent } from 'react';
import { Crosshair, Save } from 'lucide-react';
import { FIELD_LABELS, type Inspection, type InspectionPatch } from '../types';
import type { EvidenceSelection } from './EvidenceViewer';

export function DeclarationsEditor({ inspection, busy, onSave, onSelect }: { inspection: Inspection; busy: boolean; onSave: (patch: InspectionPatch) => Promise<boolean>; onSelect: (selection: EvidenceSelection) => void }) {
  const [values, setValues] = useState<Record<string, string>>({}); const [notes, setNotes] = useState<Record<string, string>>({});
  useEffect(() => {
    setValues(Object.fromEntries(Object.keys(FIELD_LABELS).map(key => [key, inspection.fields[key]?.value || ''])));
    setNotes(Object.fromEntries(Object.keys(FIELD_LABELS).map(key => [key, inspection.fields[key]?.note || ''])));
  }, [inspection.version, inspection.fields]);
  const changedFields = Object.fromEntries(Object.entries(values).filter(([key, value]) => value !== (inspection.fields[key]?.value || '')));
  const changedNotes = Object.fromEntries(Object.entries(notes).filter(([key, value]) => value !== (inspection.fields[key]?.note || '')));
  const dirty = Object.keys(changedFields).length > 0 || Object.keys(changedNotes).length > 0;
  async function submit(event: FormEvent) { event.preventDefault(); await onSave({ version: inspection.version, fields: changedFields, field_notes: changedNotes }); }
  return <form className="declarations-panel" onSubmit={submit}><div className="declarations-heading"><span className="eyebrow">READ / VERIFY / CORRECT</span><h2>Declarations</h2><p>Check each value against the label. Select a source to highlight its image region.</p></div>{Object.entries(FIELD_LABELS).map(([key, label], index) => {
    const field = inspection.fields[key];
    return <div className="declaration-row" key={key}><div className="declaration-label"><label htmlFor={`field-${key}`}><span>{String(index + 1).padStart(2, '0')}</span>{label}</label>{field?.source === 'manual' ? <span className="confidence manual">Manual</span> : field?.value ? <span className={`confidence ${field.confidence < 0.8 ? 'low' : ''}`}>{Math.round(field.confidence * 100)}% OCR</span> : <span className="confidence missing">Unverified</span>}</div><div className="declaration-input"><input id={`field-${key}`} value={values[key] || ''} disabled={busy || inspection.status === 'processing'} maxLength={2000} onChange={event => setValues(current => ({ ...current, [key]: event.target.value }))} placeholder="Not identified — verify the label" />{field?.image_id && <button className="icon-button" type="button" title={`Locate ${label} in evidence`} aria-label={`Locate ${label} in evidence`} onClick={() => onSelect({ imageId: field.image_id!, box: field.box, label })}><Crosshair size={17} /></button>}</div><details className="field-note"><summary>Evidence / correction note{notes[key] ? ' · added' : ''}</summary><label><span className="sr-only">Evidence or correction note for {label}</span><textarea rows={2} value={notes[key] || ''} disabled={busy || inspection.status === 'processing'} maxLength={2000} onChange={event => setNotes(current => ({ ...current, [key]: event.target.value }))} placeholder="Where was this verified? Explain any correction." /></label></details></div>;
  })}<div className="declarations-save"><p>{dirty ? 'You have unsaved corrections.' : 'Saved corrections are recorded with their provenance.'}</p><button className="button primary" disabled={busy || !dirty || inspection.status === 'processing'}><Save size={16} />{busy ? 'Saving…' : 'Save corrections'}</button></div></form>;
}
