export type Role = 'inspector' | 'reviewer';
export interface User { id: number; name: string; email: string; role: Role }
export interface AuthResponse { user: User; csrf_token: string }
export type InspectionStatus = 'draft' | 'processing' | 'ready' | 'reviewed' | 'failed';
export type FindingStatus = 'pass' | 'potential_violation' | 'needs_review' | 'not_applicable';
export interface InspectionSummary {
  id: string; product_name: string; brand: string; barcode: string; category: string;
  origin: string; scope_confirmed: boolean; notes: string; status: InspectionStatus;
  created_at: string; updated_at: string; owner_name: string; version: number;
  image_count: number; potential_violations: number; needs_review: number;
  review_decision: string | null;
}
export interface OcrLine { text: string; confidence: number; box: number[][] }
export interface Applicability {
  status: 'unknown' | 'applicable' | 'not_applicable';
  exemption: 'none' | 'claimed' | 'confirmed';
  reason: string;
}
export interface DeclarationCandidate {
  value: string; confidence: number; image_id: string; panel?: string; box: number[][] | null;
}
export interface EvidenceImage {
  id: string; filename: string; panel: string; width: number; height: number; url: string;
  quality: { warnings: string[]; blur_score?: number; reflection_score?: number; ocr_confidence?: number; review_required?: boolean }; ocr_text: string; lines: OcrLine[];
}
export interface Declaration {
  value: string; confidence: number; image_id: string | null; box: number[][] | null;
  source: 'ocr' | 'manual'; note: string; candidates?: DeclarationCandidate[];
}
export interface Reconciliation {
  net_quantity?: { status: 'insufficient' | 'consistent' | 'conflict'; candidates: DeclarationCandidate[]; normalized?: (string | null)[] };
}
export interface Finding {
  rule_id: string; title: string; status: FindingStatus; explanation: string;
  field: string | null; evidence_image_id: string | null; evidence_box: number[][] | null;
  evidence?: { image_id: string; filename: string; panel: string; sha256?: string } | null;
  source_url: string; provision: string;
}
export interface AssessmentSummary {
  id: string; created_at: string; rule_version: string;
  summary: Record<FindingStatus, number>; review_decision: string | null; assessment_version?: string; evidence_count?: number;
}
export interface AuditEvent { id: number; created_at: string; actor: string; action: string; detail: string }
export interface Inspection extends InspectionSummary {
  coverage_confirmed: boolean; images: EvidenceImage[]; fields: Record<string, Declaration>;
  findings: Finding[]; assessments: AssessmentSummary[]; audit: AuditEvent[];
  applicability: Applicability; reconciliation: Reconciliation;
  manual_checks: Record<string, string>; processing_error: string | null;
  processing_seconds: number | null; rule_version: string | null;
  current_assessment_id: string | null; review_notes: string | null;
}
export interface InspectionInput {
  product_name: string; brand?: string; barcode?: string; category: 'household' | 'other';
  origin: 'domestic' | 'imported' | 'unknown'; scope_confirmed: boolean; applicability?: Applicability; notes?: string;
}
export interface InspectionPatch {
  version: number; product_name?: string; brand?: string; barcode?: string;
  origin?: string; scope_confirmed?: boolean; applicability?: Applicability; notes?: string; coverage_confirmed?: boolean;
  fields?: Record<string, string>; field_notes?: Record<string, string>;
  manual_checks?: Record<string, string>;
}
export interface DashboardData {
  total: number; needs_review: number; reviewed: number; potential_violations: number;
  recent: InspectionSummary[];
}
export interface Rule { id: string; title: string; field: string; provision: string; source_url: string; description: string }
export interface RulesData { version: string; scope: string; limitations: string[]; rules: Rule[] }
export interface Sample { name: string; description: string; url: string }
export const FIELD_LABELS: Record<string, string> = {
  product_name: 'Product name', manufacturer: 'Manufacturer / packer / importer',
  address: 'Responsible business address', net_quantity: 'Net quantity', mrp: 'Maximum retail price',
  date: 'Manufacture / packing / import date', consumer_care: 'Consumer care', country_of_origin: 'Country of origin',
};
