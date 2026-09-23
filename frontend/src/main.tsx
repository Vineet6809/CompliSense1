import React from 'react';
import ReactDOM from 'react-dom/client';
import '@fontsource/noto-sans/400.css';
import '@fontsource/noto-sans/600.css';
import '@fontsource/noto-sans/700.css';
import '@fontsource/noto-sans-devanagari/400.css';
import '@fontsource/noto-sans-devanagari/600.css';
import '@fontsource/noto-sans-devanagari/700.css';
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth';
import { Layout } from './components/Layout';
import { EmptyState, Spinner } from './components/Common';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { InspectionsPage } from './pages/InspectionsPage';
import { CreateInspectionPage } from './pages/CreateInspectionPage';
import { InspectionPage } from './pages/InspectionPage';
import { RulesPage } from './pages/RulesPage';
import './styles.css';

function App() {
  const { user, loading } = useAuth();
  if (loading) return <div className="boot-screen"><Spinner label="Opening CompliSense…" /></div>;
  if (!user) return <LoginPage />;
  return <><a className="skip-link" href="#main-content">Skip to content</a><Routes><Route element={<Layout />}><Route index element={<DashboardPage />} /><Route path="inspections" element={<InspectionsPage />} /><Route path="inspections/new" element={<CreateInspectionPage />} /><Route path="inspections/:id" element={<InspectionPage />} /><Route path="rules" element={<RulesPage />} /><Route path="*" element={<EmptyState title="This page could not be found." action={<Link className="button primary" to="/">Back to overview</Link>}>Use the navigation to return to your workspace.</EmptyState>} /></Route></Routes></>;
}
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><BrowserRouter><AuthProvider><App /></AuthProvider></BrowserRouter></React.StrictMode>);
