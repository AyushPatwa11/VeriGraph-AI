import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const primaryUrl =
      process.env.BACKEND_URL ||
      process.env.NEXT_PUBLIC_BACKEND_URL ||
      "https://verigraph-ai.onrender.com";

    const candidateHosts = [
      primaryUrl,
      "http://backend:8000",
      "http://127.0.0.1:8000",
      "http://localhost:8000",
    ];

    const uniqueHosts = Array.from(new Set(candidateHosts.map((h) => h.replace(/\/$/, ""))));

    let response: Response | null = null;
    let lastErrorDetail = "";

    for (const host of uniqueHosts) {
      try {
        const targetUrl = `${host}/api/propagation/analyze-spread`;

        response = await fetch(targetUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(25000), // 25s timeout for cloud propagation analysis
        });

        if (response.ok) {
          const data = await response.json();
          return NextResponse.json(data);
        }

        const errorText = await response.text().catch(() => "");
        lastErrorDetail = `Backend error (${response.status}): ${errorText || response.statusText}`;

        if (response.status < 500) {
          return NextResponse.json({ error: lastErrorDetail }, { status: response.status });
        }
      } catch (err) {
        lastErrorDetail = err instanceof Error ? err.message : String(err);
      }
    }

    return NextResponse.json(
      { error: `Propagation request failed: ${lastErrorDetail || "Backend unreachable"}` },
      { status: 500 }
    );
  } catch (error) {
    console.error("Propagation analyze-spread API error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Internal server error" },
      { status: 500 }
    );
  }
}
