import type { GraphLink, GraphNode } from "@/types/analysis";

export const DEFAULT_GRAPH_NODES: GraphNode[] = [
  { id: "node-1", label: "BreakingNews_Net", followers: 45000, cluster: 0 },
  { id: "node-2", label: "TruthSeeker_X", followers: 18200, cluster: 0 },
  { id: "node-3", label: "DailyPulse_RSS", followers: 89000, cluster: 1 },
  { id: "node-4", label: "GlobalAlerts_TG", followers: 34000, cluster: 1 },
  { id: "node-5", label: "FactChecker_Org", followers: 120000, cluster: 2 },
  { id: "node-6", label: "ViralPost_FB", followers: 62000, cluster: 0 },
  { id: "node-7", label: "GDELT_Event_891", followers: 15000, cluster: 3 },
  { id: "node-8", label: "MediaWatch_Blog", followers: 27000, cluster: 2 },
];

export const DEFAULT_GRAPH_LINKS: GraphLink[] = [
  { source: "node-1", target: "node-2", kind: "semantic" },
  { source: "node-1", target: "node-6", kind: "temporal" },
  { source: "node-2", target: "node-4", kind: "url" },
  { source: "node-3", target: "node-1", kind: "semantic" },
  { source: "node-3", target: "node-5", kind: "url" },
  { source: "node-4", target: "node-6", kind: "temporal" },
  { source: "node-5", target: "node-8", kind: "semantic" },
  { source: "node-6", target: "node-7", kind: "temporal" },
  { source: "node-7", target: "node-3", kind: "url" },
];
