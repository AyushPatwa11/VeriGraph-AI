import type { AnalysisResult } from "@/types/analysis";

const BACKEND_ENDPOINT =
  process.env.NEXT_PUBLIC_BACKEND_URL || "https://verigraph-ai.onrender.com";

export async function analyzeClaim(query: string): Promise<AnalysisResult> {
  // First attempt via Next.js serverless proxy route
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (response.ok) {
      return await response.json();
    }
  } catch (err) {
    console.warn("Proxy route notice, connecting directly to Render backend:", err);
  }

  // Fallback: Direct client-to-backend fetch (Bypasses Vercel 10s Serverless timeout cap)
  const directUrl = `${BACKEND_ENDPOINT.replace(/\/$/, "")}/api/analyze`;
  const directResponse = await fetch(directUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!directResponse.ok) {
    const errorData = await directResponse.json().catch(() => null);
    throw new Error(
      errorData?.error || errorData?.detail || `Analysis request failed (${directResponse.status})`
    );
  }

  return directResponse.json();
}

export async function getPropagationMetrics(query: string) {
  // First attempt via Next.js serverless proxy route
  try {
    const response = await fetch("/api/propagation/analyze-spread", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (response.ok) {
      return await response.json();
    }
  } catch (err) {
    console.warn("Proxy route notice, connecting directly to Render backend:", err);
  }

  // Fallback: Direct client-to-backend fetch (Bypasses Vercel 10s Serverless timeout cap)
  const directUrl = `${BACKEND_ENDPOINT.replace(/\/$/, "")}/api/propagation/analyze-spread`;
  const directResponse = await fetch(directUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!directResponse.ok) {
    const errorData = await directResponse.json().catch(() => null);
    throw new Error(
      errorData?.error || errorData?.detail || `Propagation request failed (${directResponse.status})`
    );
  }

  return directResponse.json();
}
