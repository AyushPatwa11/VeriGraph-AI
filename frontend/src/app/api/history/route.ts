import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

const BACKEND =
  process.env.BACKEND_URL ||
  process.env.NEXT_PUBLIC_BACKEND_URL ||
  (process.env.NODE_ENV === "development"
    ? "http://localhost:8000"
    : "https://verigraph-ai.onrender.com");

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = searchParams.get("limit") ?? "50";
    const offset = searchParams.get("offset") ?? "0";

    const url = `${BACKEND.replace(/\/$/, "")}/api/history?limit=${limit}&offset=${offset}`;
    const res = await fetch(url, { cache: "no-store" });

    if (!res.ok) {
      return NextResponse.json({ error: "Backend error" }, { status: res.status });
    }
    const data = await res.json();
    return NextResponse.json(data);
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Failed to fetch history" },
      { status: 500 }
    );
  }
}

export async function DELETE() {
  try {
    const url = `${BACKEND.replace(/\/$/, "")}/api/history`;
    const res = await fetch(url, { method: "DELETE", cache: "no-store" });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Failed to clear history" },
      { status: 500 }
    );
  }
}
