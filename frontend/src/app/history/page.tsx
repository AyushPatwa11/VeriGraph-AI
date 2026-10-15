"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";

interface HistoryRecord {
  id: number;
  saved_at: string;
  query: string;
  finalScore: number;
  riskLevel: "Low" | "Medium" | "High" | "Inconclusive";
  confidence: number;
  summary: string;
  layers: Array<{ name: string; score: number; status: string }>;
  nodes: unknown[];
  links: unknown[];
  posts: unknown[];
}

interface HistoryResponse {
  total: number;
  records: HistoryRecord[];
}

const riskConfig = {
  Low: {
    label: "✓ TRUE",
    color: "#7df5c5",
    bg: "from-emerald-950/50 to-emerald-900/20",
    border: "border-emerald-500/40",
    badge: "bg-emerald-950/60 text-emerald-400 border-emerald-500/40",
  },
  Medium: {
    label: "⚠ MIXED",
    color: "#ffc96f",
    bg: "from-yellow-950/50 to-yellow-900/20",
    border: "border-yellow-500/40",
    badge: "bg-yellow-950/60 text-yellow-400 border-yellow-500/40",
  },
  High: {
    label: "✕ FALSE",
    color: "#ff7d6b",
    bg: "from-red-950/50 to-red-900/20",
    border: "border-red-500/40",
    badge: "bg-red-950/60 text-red-400 border-red-500/40",
  },
  Inconclusive: {
    label: "? UNCLEAR",
    color: "#a0b4c8",
    bg: "from-slate-900/50 to-slate-800/20",
    border: "border-slate-600/40",
    badge: "bg-slate-900/60 text-slate-400 border-slate-600/40",
  },
};

function ScoreRing({ score, color }: { score: number; color: string }) {
  const r = 24;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;
  return (
    <svg width={64} height={64} viewBox="0 0 64 64" className="rotate-[-90deg]">
      <circle cx={32} cy={32} r={r} fill="none" stroke="#1a3045" strokeWidth={6} />
      <circle
        cx={32}
        cy={32}
        r={r}
        fill="none"
        stroke={color}
        strokeWidth={6}
        strokeLinecap="round"
        strokeDasharray={`${dash} ${circ - dash}`}
        style={{ transition: "stroke-dasharray 0.8s ease" }}
      />
      <text
        x={32}
        y={37}
        textAnchor="middle"
        fill={color}
        fontSize={13}
        fontWeight={700}
        style={{ transform: "rotate(90deg)", transformOrigin: "32px 32px" }}
      >
        {score}
      </text>
    </svg>
  );
}

function formatDate(iso: string): string {
  try {
    const d = new Date(iso);
    return d.toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  } catch {
    return iso;
  }
}

export default function HistoryPage() {
  const router = useRouter();
  const [data, setData] = useState<HistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deleting, setDeleting] = useState<number | null>(null);
  const [clearing, setClearing] = useState(false);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<string>("all");
  const [dbStats, setDbStats] = useState<{ total: number; file_size_kb: number; file_path: string } | null>(null);
  const [downloadUrl] = useState("http://localhost:8000/api/history/export/download");

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [histRes, statsRes] = await Promise.all([
        fetch("/api/history?limit=200"),
        fetch("http://localhost:8000/api/db-stats").catch(() => null),
      ]);
      if (!histRes.ok) throw new Error("Failed to load history");
      const json: HistoryResponse = await histRes.json();
      setData(json);
      if (statsRes?.ok) {
        const stats = await statsRes.json();
        setDbStats(stats);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load history");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleDelete = async (id: number) => {
    setDeleting(id);
    try {
      await fetch(`http://localhost:8000/api/history/${id}`, { method: "DELETE" });
      setData((prev) =>
        prev ? { ...prev, total: prev.total - 1, records: prev.records.filter((r) => r.id !== id) } : prev
      );
    } finally {
      setDeleting(null);
    }
  };

  const handleClearAll = async () => {
    if (!confirm("Are you sure you want to delete ALL saved analyses? This cannot be undone.")) return;
    setClearing(true);
    try {
      await fetch("/api/history", { method: "DELETE" });
      setData({ total: 0, records: [] });
    } finally {
      setClearing(false);
    }
  };

  const handleReAnalyze = (record: HistoryRecord) => {
    window.sessionStorage.setItem("verigraph.analysis", JSON.stringify(record));
    router.push(`/analysis?q=${encodeURIComponent(record.query)}`);
  };

  // Filter + search
  const visibleRecords = (data?.records ?? []).filter((r) => {
    const matchSearch = search === "" || r.query.toLowerCase().includes(search.toLowerCase());
    const matchFilter = filter === "all" || r.riskLevel === filter;
    return matchSearch && matchFilter;
  });

  const filters = ["all", "Low", "Medium", "High", "Inconclusive"];

  return (
    <div className="min-h-screen bg-[#031019] text-white">
      <Navbar />

      {/* Page Header */}
      <div className="border-b border-white/10 bg-gradient-to-b from-[#061a28] to-[#031019]">
        <div className="mx-auto max-w-7xl px-6 py-10">
          <motion.div initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
            <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="h-2 w-2 rounded-full bg-[#73d6ff] animate-pulse" />
                  <span className="text-xs font-bold uppercase tracking-[0.25em] text-[#8fd2f1]">
                    Persistent Intelligence Archive
                  </span>
                </div>
                <h1 className="text-3xl font-bold text-white sm:text-4xl">
                  Analysis{" "}
                  <span className="bg-gradient-to-r from-[#73d6ff] to-[#7df5c5] bg-clip-text text-transparent">
                    History
                  </span>
                </h1>
                <p className="mt-2 text-sm text-[#96c9df]">
                  Every claim analyzed is automatically saved to{" "}
                  <code className="rounded bg-white/10 px-1.5 py-0.5 text-[#73d6ff] text-xs font-mono">
                    backend/data/analyses.json
                  </code>
                </p>
              </div>

              {/* Stats Bar */}
              {dbStats && (
                <div className="flex flex-wrap gap-3">
                  {[
                    { label: "Total Saved", value: dbStats.total },
                    { label: "File Size", value: `${dbStats.file_size_kb} KB` },
                  ].map((stat) => (
                    <div
                      key={stat.label}
                      className="rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-center backdrop-blur-sm"
                    >
                      <p className="text-lg font-bold text-[#9be2ff]">{stat.value}</p>
                      <p className="text-xs text-[#7aaac2]">{stat.label}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      <main className="mx-auto max-w-7xl px-6 py-8">
        {/* Toolbar */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
        >
          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#5a8099]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search saved claims..."
              className="w-full rounded-xl border border-white/20 bg-[#0a2030]/70 pl-10 pr-4 py-2.5 text-sm text-[#dcf1fb] outline-none focus:border-[#73d6ff]/60 focus:ring-1 focus:ring-[#73d6ff]/30 placeholder:text-[#4a7a95]"
            />
          </div>

          {/* Filters + Actions */}
          <div className="flex flex-wrap items-center gap-2">
            {/* Risk filter pills */}
            <div className="flex gap-1 rounded-xl border border-white/10 bg-white/5 p-1">
              {filters.map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`rounded-lg px-3 py-1 text-xs font-semibold transition ${
                    filter === f
                      ? "bg-[#73d6ff]/20 text-[#73d6ff] border border-[#73d6ff]/40"
                      : "text-[#96c9df] hover:text-white"
                  }`}
                >
                  {f === "all" ? "All" : f}
                </button>
              ))}
            </div>

            {/* Download */}
            <a
              href={downloadUrl}
              download="verigraph_analyses.json"
              className="flex items-center gap-1.5 rounded-xl border border-[#73d6ff]/40 bg-[#73d6ff]/10 px-3 py-2 text-xs font-semibold text-[#73d6ff] transition hover:bg-[#73d6ff]/20"
            >
              <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download JSON
            </a>

            {/* Clear All */}
            {(data?.total ?? 0) > 0 && (
              <button
                onClick={handleClearAll}
                disabled={clearing}
                className="flex items-center gap-1.5 rounded-xl border border-red-500/30 bg-red-950/20 px-3 py-2 text-xs font-semibold text-red-400 transition hover:bg-red-950/40 disabled:opacity-50"
              >
                {clearing ? "Clearing..." : "Clear All"}
              </button>
            )}

            {/* Refresh */}
            <button
              onClick={fetchHistory}
              className="flex items-center gap-1.5 rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-xs font-semibold text-[#96c9df] transition hover:bg-white/10"
            >
              <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Refresh
            </button>
          </div>
        </motion.div>

        {/* Content */}
        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="flex flex-col items-center gap-4">
              <div className="h-10 w-10 animate-spin rounded-full border-4 border-[#73d6ff]/20 border-t-[#73d6ff]" />
              <p className="text-sm text-[#8fd2f1]">Loading saved analyses...</p>
            </div>
          </div>
        )}

        {error && !loading && (
          <div className="rounded-2xl border border-red-500/30 bg-red-950/20 p-8 text-center">
            <p className="text-red-400">{error}</p>
            <p className="mt-2 text-sm text-[#96c9df]">
              Make sure the backend is running at{" "}
              <code className="text-[#73d6ff]">http://localhost:8000</code>
            </p>
          </div>
        )}

        {!loading && !error && visibleRecords.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="rounded-3xl border border-white/10 bg-white/[0.04] p-16 text-center backdrop-blur-xl"
          >
            <div className="text-5xl mb-4">🗄️</div>
            <h2 className="text-xl font-semibold text-white mb-2">
              {search || filter !== "all" ? "No matching records" : "No analyses saved yet"}
            </h2>
            <p className="text-[#96c9df] mb-6">
              {search || filter !== "all"
                ? "Try adjusting your search or filter."
                : "Analyze a claim on the home page — it will automatically appear here."}
            </p>
            <Link
              href="/"
              className="inline-flex items-center gap-2 rounded-full border border-[#73d6ff]/50 bg-[#73d6ff]/15 px-6 py-3 text-sm font-bold text-[#73d6ff] transition hover:bg-[#73d6ff]/25"
            >
              <span>🔍</span> Go Analyze Something
            </Link>
          </motion.div>
        )}

        {!loading && !error && visibleRecords.length > 0 && (
          <div className="space-y-4">
            <p className="text-xs text-[#5a8099]">
              Showing {visibleRecords.length} of {data?.total ?? 0} records
            </p>
            <AnimatePresence mode="popLayout">
              {visibleRecords.map((record, idx) => {
                const risk = riskConfig[record.riskLevel] ?? riskConfig.Inconclusive;
                return (
                  <motion.div
                    key={record.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.96, y: -10 }}
                    transition={{ duration: 0.3, delay: idx < 10 ? idx * 0.04 : 0 }}
                    className={`group relative overflow-hidden rounded-2xl border bg-gradient-to-br ${risk.bg} ${risk.border} backdrop-blur-sm transition-all duration-300 hover:border-opacity-60 hover:shadow-lg`}
                  >
                    {/* Glow accent line */}
                    <div
                      className="absolute left-0 top-0 bottom-0 w-1 rounded-l-2xl"
                      style={{ background: risk.color }}
                    />

                    <div className="flex flex-col gap-4 p-5 pl-6 sm:flex-row sm:items-start sm:justify-between">
                      {/* Left: Score ring + info */}
                      <div className="flex items-start gap-4">
                        <ScoreRing score={record.finalScore} color={risk.color} />
                        <div className="flex-1 min-w-0">
                          <div className="flex flex-wrap items-center gap-2 mb-1">
                            <span
                              className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-[11px] font-bold ${risk.badge}`}
                            >
                              {risk.label}
                            </span>
                            <span className="text-xs text-[#5a8099]">
                              #{record.id} • {formatDate(record.saved_at)}
                            </span>
                          </div>
                          <p
                            className="text-base font-semibold text-white leading-snug line-clamp-2 group-hover:text-[#e8f5ff] transition-colors"
                            title={record.query}
                          >
                            {record.query}
                          </p>
                          {record.summary && (
                            <p className="mt-1.5 text-xs text-[#7aaac2] line-clamp-2">{record.summary}</p>
                          )}

                          {/* Meta badges */}
                          <div className="mt-3 flex flex-wrap gap-2">
                            <span className="rounded-md border border-white/10 bg-white/5 px-2 py-0.5 text-[11px] text-[#96c9df]">
                              {record.posts?.length ?? 0} posts
                            </span>
                            <span className="rounded-md border border-white/10 bg-white/5 px-2 py-0.5 text-[11px] text-[#96c9df]">
                              {record.nodes?.length ?? 0} nodes
                            </span>
                            <span className="rounded-md border border-white/10 bg-white/5 px-2 py-0.5 text-[11px] text-[#96c9df]">
                              {Math.round((record.confidence ?? 0) * 100)}% confidence
                            </span>
                            {(record.layers ?? []).map((layer) => (
                              <span
                                key={layer.name}
                                className="rounded-md border border-white/10 bg-white/5 px-2 py-0.5 text-[11px] text-[#96c9df]"
                              >
                                {layer.name}: {layer.score}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Right: Actions */}
                      <div className="flex shrink-0 items-center gap-2 sm:flex-col sm:items-end">
                        <button
                          onClick={() => handleReAnalyze(record)}
                          className="flex items-center gap-1.5 rounded-xl border border-[#73d6ff]/40 bg-[#73d6ff]/10 px-3 py-2 text-xs font-semibold text-[#73d6ff] transition hover:bg-[#73d6ff]/25"
                        >
                          <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                          </svg>
                          View
                        </button>
                        <button
                          onClick={() => handleDelete(record.id)}
                          disabled={deleting === record.id}
                          className="flex items-center gap-1.5 rounded-xl border border-red-500/20 bg-red-950/10 px-3 py-2 text-xs font-semibold text-red-400/80 transition hover:bg-red-950/30 hover:text-red-300 disabled:opacity-40"
                        >
                          {deleting === record.id ? (
                            <span className="animate-spin">⌛</span>
                          ) : (
                            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          )}
                          Delete
                        </button>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
