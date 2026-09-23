import { useRef, useState } from 'react';
import { ImagePlus, Trash2 } from 'lucide-react';
import { ErrorBanner } from './Common';

export interface PendingImage { file: File; panel: string; key: string }
export function UploadPicker({ files, onChange, existingCount = 0, disabled = false }: { files: PendingImage[]; onChange: (files: PendingImage[]) => void; existingCount?: number; disabled?: boolean }) {
  const input = useRef<HTMLInputElement>(null); const [error, setError] = useState('');
  function addFiles(selected: FileList | null) {
    if (!selected) return;
    const incoming = Array.from(selected);
    if (existingCount + files.length + incoming.length > 8) { setError('An inspection supports up to 8 images. Remove a pending image or choose fewer files.'); return; }
    if (incoming.some(file => !['image/jpeg', 'image/png', 'image/webp'].includes(file.type))) { setError('Choose JPEG, PNG, or WebP images.'); return; }
    if (incoming.some(file => file.size > 10 * 1024 * 1024)) { setError('Each image must be 10 MB or smaller.'); return; }
    setError(''); onChange([...files, ...incoming.map(file => ({ file, panel: 'front', key: crypto.randomUUID() }))]);
  }
  return <div className="upload-picker"><input ref={input} className="sr-only" tabIndex={-1} type="file" accept="image/jpeg,image/png,image/webp" multiple disabled={disabled} onChange={event => { addFiles(event.target.files); event.target.value = ''; }} /><button type="button" className="upload-drop" disabled={disabled || existingCount + files.length >= 8} onClick={() => input.current?.click()}><ImagePlus size={27} strokeWidth={1.4} /><strong>Add packaging photographs</strong><span>JPEG, PNG or WebP · up to 10 MB each · {8 - existingCount - files.length} slots available</span></button><ErrorBanner message={error} />{files.length > 0 && <div className="pending-images">{files.map(item => <div className="pending-image" key={item.key}><div><strong>{item.file.name}</strong><small>{(item.file.size / (1024 * 1024)).toFixed(1)} MB</small></div><label><span className="sr-only">Panel for {item.file.name}</span><select aria-label={`Panel for ${item.file.name}`} disabled={disabled} value={item.panel} onChange={event => onChange(files.map(file => file.key === item.key ? { ...file, panel: event.target.value } : file))}><option value="front">Front panel</option><option value="back">Back panel</option><option value="side">Side panel</option><option value="other">Other panel</option></select></label><button type="button" className="icon-button" disabled={disabled} onClick={() => onChange(files.filter(file => file.key !== item.key))} aria-label={`Remove ${item.file.name}`}><Trash2 size={16} /></button></div>)}</div>}</div>;
}
