import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const backendUrl = "http://localhost:8000/api/analyze";

    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      let errorDetail = `Backend error: ${response.status} ${response.statusText}`;
      try {
        const jsonErr = JSON.parse(errorText);
        if (jsonErr.detail) errorDetail = jsonErr.detail;
      } catch {}
      return NextResponse.json({ error: errorDetail }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Analyze API proxy error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Internal server error" },
      { status: 500 }
    );
  }
}
