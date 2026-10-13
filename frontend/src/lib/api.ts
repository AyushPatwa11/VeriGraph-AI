import type { AnalysisResult } from "@/types/analysis";

const BACKEND_ENDPOINT =
  process.env.NEXT_PUBLIC_BACKEND_URL ||
  (process.env.NODE_ENV === "development"
    ? "http://localhost:8000"
    : "https://verigraph-ai.onrender.com");

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

    const errorData = await response.json().catch(() => null);
    if (errorData?.error || errorData?.detail) {
      throw new Error(errorData.error || errorData.detail);
    }
  } catch (err: any) {
    if (err?.message && !err.message.includes("Failed to fetch") && !err.message.includes("NetworkError")) {
      throw err;
    }
    console.warn("Proxy route notice, connecting directly to backend:", err);
  }

  // Fallback: Direct client-to-backend fetch
  const directUrl = `${BACKEND_ENDPOINT.replace(/\/$/, "")}/api/analyze`;
  try {
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
  } catch (err: any) {
    throw new Error(
      err?.message?.includes("Failed to fetch")
        ? `Unable to connect to backend server at ${BACKEND_ENDPOINT}. Please ensure the backend is running.`
        : (err?.message || "Analysis request failed")
    );
  }
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

    const errorData = await response.json().catch(() => null);
    if (errorData?.error || errorData?.detail) {
      throw new Error(errorData.error || errorData.detail);
    }
  } catch (err: any) {
    if (err?.message && !err.message.includes("Failed to fetch") && !err.message.includes("NetworkError")) {
      throw err;
    }
    console.warn("Proxy route notice, connecting directly to backend:", err);
  }

  // Fallback: Direct client-to-backend fetch
  const directUrl = `${BACKEND_ENDPOINT.replace(/\/$/, "")}/api/propagation/analyze-spread`;
  try {
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
  } catch (err: any) {
    throw new Error(
      err?.message?.includes("Failed to fetch")
        ? `Unable to connect to backend server at ${BACKEND_ENDPOINT}. Please ensure the backend is running.`
        : (err?.message || "Propagation request failed")
    );
  }
}
