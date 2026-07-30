import type { AnalysisResult } from "@/types/analysis";

export async function analyzeClaim(query: string): Promise<AnalysisResult> {
  const response = await fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.error || errorData?.detail || `Analysis request failed (${response.status})`);
  }

  return response.json();
}

export async function getPropagationMetrics(query: string) {
  const response = await fetch("/api/propagation/analyze-spread", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.error || errorData?.detail || `Propagation request failed (${response.status})`);
  }

  return response.json();
}
