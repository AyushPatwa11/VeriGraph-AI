"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Navbar } from "@/components/Navbar";
import { ScoreDisplay } from "@/components/ScoreDisplay";
import { LayerBreakdown } from "@/components/LayerBreakdown";
import { NetworkGraph } from "@/components/NetworkGraph";
import { AttributionPanel } from "@/components/AttributionPanel";
import { PostsList } from "@/components/PostsList";
import { PropagationSpread } from "@/components/PropagationSpread";
import { LiveAmplificationFeed } from "@/components/LiveAmplificationFeed";
import { Footer } from "@/components/Footer";
import type { AnalysisResult } from "@/types/analysis";

interface AmplificationPost {
  id: string;
  source: string;
  platform: string;
  title: string;
  text?: string;
  likes: number;
  shares: number;
  timestamp: string;
  url?: string;
  author?: string;
  engagement: number;
}

export default function AnalysisPage() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [propagationMetrics, setPropagationMetrics] = useState<any>(null);
  const [amplificationPosts, setAmplificationPosts] = useState<AmplificationPost[]>([]);
  const [loadingPropagation, setLoadingPropagation] = useState(false);

  const fetchPropagationMetrics = async (query: string) => {
    setLoadingPropagation(true);
    try {
      const response = await fetch("/api/propagation/analyze-spread", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error("API request failed");

      const data = await response.json();

      if (data.analysis) {
        setPropagationMetrics(data.analysis);

        // Transform posts into amplification posts with URLs
        const posts: AmplificationPost[] = (data.posts || []).map((post: any) => {
          // Only use URLs explicitly provided by backend - no fallback construction
          const postUrl = post.url || post.permalink_url || post.link || post.article_url || post.source_url;

          return {
            id: post.id || `${post.author_id || post.username}_${post.created_at || Math.random()}`,
            source: post.platform,
            platform: post.platform,
            title: `${post.username || post.author || "User"} on ${(post.platform || "unknown").toUpperCase()}`,
            text: post.text || post.content || "",
            likes: post.likes || 0,
            shares: post.shares || 0,
            timestamp: post.created_at || new Date().toISOString(),
            author: post.username || post.author || "Anonymous",
            engagement: post.engagement || 0,
            url: postUrl,
          };
        });

        setAmplificationPosts(posts);
      }
    } catch (error) {
      console.error("Error fetching propagation metrics:", error);
    } finally {
      setLoadingPropagation(false);
    }
  };

  useEffect(() => {
    try {
      const raw = window.sessionStorage.getItem("verigraph.analysis");
      if (!raw) {
        setLoaded(true);
        return;
      }
      const parsed = JSON.parse(raw) as AnalysisResult;
      if (parsed?.query && parsed?.layers && parsed?.nodes) {
        setResult(parsed);
        // Fetch propagation metrics for the analyzed claim
        fetchPropagationMetrics(parsed.query);
      }
    } catch {
      setResult(null);
    } finally {
      setLoaded(true);
    }
  }, []);

  if (loaded && !result) {
    return (
      <div className="min-h-screen bg-[#031019] text-white">
        <Navbar />
        <main className="mx-auto flex min-h-[70vh] w-full max-w-4xl flex-col items-center justify-center px-6 text-center">
          <h1 className="text-3xl font-semibold text-white">No Live Analysis Result Found</h1>
          <p className="mt-4 max-w-2xl text-[#b9d8e8]">
            Start from the home page and run a live analysis. Mock results are disabled.
          </p>
          <Link
            href="/"
            className="mt-8 rounded-full border border-[#8adfff]/60 bg-[#73d6ff]/20 px-6 py-3 text-sm font-semibold text-[#def5ff] transition hover:bg-[#73d6ff]/35"
          >
            Go To Home
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className="min-h-screen bg-[#031019] text-white">
      <Navbar />
      <main className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-6 py-10">
        <motion.section
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="rounded-3xl border border-white/15 bg-linear-to-br from-[#0a2838] via-[#0b1b28] to-[#103249] p-7"
        >
          <p className="text-xs uppercase tracking-[0.2em] text-[#8fd2f1]">Analyzed Claim</p>
          <h1 className="mt-3 text-2xl font-semibold leading-9 text-[#e2eff5] sm:text-3xl">
            {result.query}
          </h1>
        </motion.section>

        {/* SIMPLE VERDICT BADGE - TRUE OR FALSE */}
        {(() => {
          let verdict = { label: "", color: "#ffc96f", bgGradient: "from-yellow-950/40 to-yellow-900/20" };

          if (result.riskLevel === "Low") {
            verdict = { label: "✓ TRUE NEWS", color: "#7df5c5", bgGradient: "from-green-950/40 to-green-900/20" };
          } else if (result.riskLevel === "Medium" || result.riskLevel === "Inconclusive") {
            verdict = { label: "⚠ INCONCLUSIVE", color: "#ffc96f", bgGradient: "from-yellow-950/40 to-yellow-900/20" };
          } else {
            verdict = { label: "✕ FALSE NEWS", color: "#ff9e64", bgGradient: "from-red-950/40 to-red-900/20" };
          }

          return (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className={`bg-gradient-to-r ${verdict.bgGradient} border-2 rounded-2xl p-8 text-center backdrop-blur-sm`}
              style={{ borderColor: verdict.color }}
            >
              <p className="text-5xl sm:text-7xl font-black" style={{ color: verdict.color }}>
                {verdict.label}
              </p>
            </motion.div>
          );
        })()}

        <ScoreDisplay
          score={result.finalScore}
          riskLevel={result.riskLevel}
          resultStatus={result.resultStatus}
          confidence={result.confidence}
        />
        <LayerBreakdown layers={result.layers} />

        <div className="grid gap-8 xl:grid-cols-[1.5fr_1fr]">
          <NetworkGraph nodes={result.nodes} links={result.links} />
          <PostsList posts={result.posts} />
        </div>

        <AttributionPanel summary={result.summary} />

        {/* Propagation Metrics */}
        {propagationMetrics && (
          <>
            <motion.section
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-12 pt-8 border-t border-white/10"
            >
              <h2 className="text-2xl font-semibold text-white mb-6">
                How This Claim Spreads
              </h2>
              <PropagationSpread metrics={propagationMetrics} />
            </motion.section>

            {amplificationPosts.length > 0 && (
              <motion.section
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                className="mt-12"
              >
                <h2 className="text-2xl font-semibold text-white mb-6">
                  Top Amplifiers
                </h2>
                <LiveAmplificationFeed posts={amplificationPosts} isLive={false} />
              </motion.section>
            )}
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}

