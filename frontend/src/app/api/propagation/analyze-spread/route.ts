import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const candidateHostnames = [
      process.env.BACKEND_URL,
      process.env.NEXT_PUBLIC_BACKEND_URL,
      "http://backend:8000",
      "http://127.0.0.1:8000",
      "http://localhost:8000",
    ].filter(Boolean) as string[];

    let lastError: Error | null = null;
    let response: Response | null = null;

    for (const host of candidateHostnames) {
      try {
        const cleanHost = host.replace(/\/$/, "");
        const targetUrl = `${cleanHost}/api/propagation/analyze-spread`;

        response = await fetch(targetUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });

        if (response.ok || response.status < 500) {
          break;
        }
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
      }
    }

    if (!response) {
      throw lastError || new Error("Failed to connect to Python backend server.");
    }

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Propagation analyze-spread API error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Internal server error" },
      { status: 500 }
    );
  }
}
