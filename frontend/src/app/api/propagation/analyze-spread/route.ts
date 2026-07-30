import { NextRequest, NextResponse } from "next/server";

export const maxDuration = 60; // 60 seconds duration on Vercel
export const dynamic = "force-dynamic";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const primaryUrl =
      process.env.BACKEND_URL ||
      process.env.NEXT_PUBLIC_BACKEND_URL ||
      "https://verigraph-ai.onrender.com";

    const cleanHost = primaryUrl.replace(/\/$/, "");
    const targetUrl = `${cleanHost}/api/propagation/analyze-spread`;

    let lastErrorDetail = "";

    for (let attempt = 1; attempt <= 2; attempt++) {
      try {
        const response = await fetch(targetUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
          cache: "no-store",
        });

        if (response.ok) {
          const data = await response.json();
          return NextResponse.json(data);
        }

        const errorText = await response.text().catch(() => "");
        lastErrorDetail = `Backend HTTP ${response.status}: ${errorText || response.statusText}`;

        if (response.status < 500) {
          return NextResponse.json({ error: lastErrorDetail }, { status: response.status });
        }
      } catch (err) {
        lastErrorDetail = err instanceof Error ? err.message : String(err);
        if (attempt < 2) {
          await new Promise((resolve) => setTimeout(resolve, 2000));
        }
      }
    }

    return NextResponse.json(
      {
        error:
          "The backend server is spinning up from sleep. Please wait 5 seconds and click Analyze again.",
      },
      { status: 503 }
    );
  } catch (error) {
    console.error("Propagation analyze-spread API error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Internal server error" },
      { status: 500 }
    );
  }
}
