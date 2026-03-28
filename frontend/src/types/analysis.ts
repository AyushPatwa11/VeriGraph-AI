export type RiskLevel = "Low" | "Medium" | "High" | "Inconclusive";
export type ResultStatus = "final" | "inconclusive";
export type LayerStatus = "available" | "insufficient_evidence" | "unavailable";

export interface LayerResult {
  name: "NLP" | "GNN" | "Gemini";
  score: number;
  explanation: string;
  status?: LayerStatus;
  confidence?: number | null;
  evidence?: Record<string, unknown>;
  errorCode?: string | null;
}

export interface GraphNode {
  id: string;
  label: string;
  followers: number;
  cluster: number;
}

export interface GraphLink {
  source: string;
  target: string;
  kind: "semantic" | "temporal" | "url";
}

export interface PostItem {
  id: string;
  username: string;
  timestamp: string;
  text: string;
  likes: number;
  shares: number;
}

export interface AnalysisResult {
  query: string;
  finalScore: number;
  riskLevel: RiskLevel;
  resultStatus?: ResultStatus;
  confidence?: number;
  summary: string;
  layers: LayerResult[];
  nodes: GraphNode[];
  links: GraphLink[];
  posts: PostItem[];
}
