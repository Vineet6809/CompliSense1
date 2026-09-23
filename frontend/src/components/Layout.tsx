import { useEffect, useState } from 'react';
import { BookOpen, ChevronRight, ClipboardList, LayoutDashboard, LogOut, Menu, Plus, X } from 'lucide-react';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { api, errorMessage } from '../api';
import { useAuth } from '../auth';

export function ServiceBar() {
  return <div className="service-bar">
    <div className="service-identity">
      <span className="service-kicker">COMPLISENSE</span>
      <span className="service-divider" aria-hidden="true">|</span>
      <span className="service-name">Evidence-led label review</span>
      <span className="service-separator" aria-hidden="true">•</span>
      <span className="service-note">Unofficial student prototype</span>
    </div>
    <span className="rule-pack">Rule set demo-2026.09</span>
  </div>;
}

function ApertureMark() {
  return <svg className="brand-mark" viewBox="0 0 24 24" aria-hidden="true">
    <path d="M5.5 4.5H19" className="mark-saffron" />
    <path d="M5.5 19.5H19" className="mark-green" />
    <path d="M5.5 4.5v15" className="mark-spine" />
    <rect x="10.5" y="10.5" width="4" height="4" className="mark-pip" />
  </svg>;
}

export function Brand({ light = false, compact = false }: { light?: boolean; compact?: boolean }) {
  return <div className={`brand ${light ? 'brand-light' : ''} ${compact ? 'brand-compact' : ''}`}>
    <ApertureMark />
    <span className="brand-copy"><span className="brand-name"><b>Compli</b><span>Sense</span></span>{!compact && <small>LEGAL METROLOGY WORKSTATION</small>}</span>
  </div>;
}

function currentSection(pathname: string) {
  if (pathname === '/') return 'Overview';
  if (pathname.startsWith('/rules')) return 'Rule reference';
  if (pathname === '/inspections/new') return 'New inspection';
  if (pathname.startsWith('/inspections/')) return 'Inspection case file';
  return 'Inspection register';
}

export function Layout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const [health, setHealth] = useState<string>('Checking OCR service');
  const [logoutError, setLogoutError] = useState('');
  useEffect(() => { setMenuOpen(false); }, [location.pathname]);
  useEffect(() => { api.health().then(data => setHealth(data.ocr_available ? 'OCR available' : 'OCR unavailable')).catch(() => setHealth('Service unavailable')); }, []);
  async function signOut() { try { await logout(); } catch (error) { setLogoutError(errorMessage(error)); } }
  const section = currentSection(location.pathname);
  return <div className="application-root">
    <ServiceBar />
    <div className="app-shell">
      {menuOpen && <button className="sidebar-scrim" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}
      <aside className={`sidebar ${menuOpen ? 'is-open' : ''}`}>
        <div className="sidebar-brand"><Brand light /><button className="mobile-only icon-button" onClick={() => setMenuOpen(false)} aria-label="Close navigation"><X size={20} /></button></div>
        <div className="workspace-label">INSPECTION WORKSPACE</div>
        <nav aria-label="Main navigation">
          <NavLink to="/" end><LayoutDashboard size={18} /><span>Overview</span></NavLink>
          <NavLink to="/inspections" end><ClipboardList size={18} /><span>Inspections</span></NavLink>
          <NavLink to="/inspections/new" className="sidebar-create"><Plus size={18} /><span>New inspection</span><ChevronRight size={15} /></NavLink>
          <NavLink to="/rules"><BookOpen size={18} /><span>Rule reference</span></NavLink>
        </nav>
        <div className="sidebar-spacer" />
        <div className="account"><span className="avatar">{user?.name.slice(0, 2).toUpperCase()}</span><div><strong>{user?.name}</strong><small>{user?.role === 'reviewer' ? 'Review officer' : 'Inspection officer'}</small></div><button className="icon-button" onClick={() => void signOut()} aria-label="Sign out" title="Sign out"><LogOut size={17} /></button></div>
        {logoutError && <p className="sidebar-error" role="alert">{logoutError}</p>}
      </aside>
      <div className="main-shell">
        <header className="topbar"><div className="breadcrumb"><button className="mobile-only icon-button" onClick={() => setMenuOpen(true)} aria-label="Open navigation"><Menu size={21} /></button><span className="topbar-context">Workspace</span><ChevronRight size={14} /><span>{section}</span></div><span className="service-state"><i className={health === 'OCR available' ? 'available' : ''} />{health}</span></header>
        <main id="main-content"><Outlet /></main>
        <footer className="app-footer"><span>CompliSense · Packaged-product label review</span><span>Decision support. Human verification required.</span></footer>
      </div>
    </div>
  </div>;
}
