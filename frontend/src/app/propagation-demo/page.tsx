"use client";

import { useEffect, useState } from "react";
import { PropagationSpread } from "@/components/PropagationSpread";
import { LiveAmplificationFeed } from "@/components/LiveAmplificationFeed";
import { ScoreDisplay } from "@/components/ScoreDisplay";
import { motion } from "framer-motion";

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

interface AnalysisState {
  threatScore: number;
  riskLevel: string;
  propagationMetrics: any;
  amplificationPosts: AmplificationPost[];
  isLoading: boolean;
}

export default function PropagationDemoPage() {
  const [state, setState] = useState<AnalysisState>({
    threatScore: 0,
    riskLevel: "Unknown",
    propagationMetrics: null,
    amplificationPosts: [],
    isLoading: false,
  });

  const [query, setQuery] = useState<string>("");

  const analyzeClaim = async (searchQuery: string) => {
    if (!searchQuery.trim() || searchQuery.length < 4) {
      alert("Please enter a claim with at least 4 characters");
      return;
    }

    setState((prev) => ({ ...prev, isLoading: true }));

    try {
      // Get propagation metrics
      const response = await fetch("/api/propagation/analyze-spread", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      if (!data.analysis) {
        throw new Error("No analysis data received");
      }

      // Transform posts into amplification posts with URLs
      const amplificationPosts: AmplificationPost[] = (
        data.posts || []
      ).map((post: any) => ({
        id: post.id || `${post.author_id || post.username}_${post.created_at || Math.random()}`,
        source: post.platform,
        platform: post.platform,
        title: `${post.username || post.author || 'User'} on ${(post.platform || 'unknown').toUpperCase()}`,
        text: post.text || post.content || '',
        likes: post.likes || 0,
        shares: post.shares || 0,
        timestamp: post.created_at || new Date().toISOString(),
        author: post.username || post.author || 'Anonymous',
        engagement: post.engagement || 0,
        url: post.url || post.permalink_url || undefined,
      }));

      // Calculate threat score based on virality
      const threatScore = data.analysis.virality?.virality_score || 0;

      setState({
        threatScore,
        riskLevel: getThreatLevel(threatScore),
        propagationMetrics: data.analysis,
        amplificationPosts,
        isLoading: false,
      });
    } catch (error) {
      console.error("Error analyzing claim:", error);
      alert("Failed to analyze claim. Make sure the backend is running on localhost:8000");
      setState((prev) => ({ ...prev, isLoading: false }));
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      analyzeClaim(query);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="border-b border-white/10 bg-white/5 backdrop-blur-xl sticky top-0 z-40"
      >
        <div className="max-w-7xl mx-auto px-6 py-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Propaganda Propagation Analysis
          </h1>
          <p className="text-gray-400">
            Track how claims spread across 5 sources with threat assessment and
            live amplification feed
          </p>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Search Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-12"
        >
          <div className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter a claim to analyze (min 4 characters)..."
              disabled={state.isLoading}
              className="flex-1 px-6 py-4 rounded-xl border border-white/20 bg-white/5 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 transition-all"
            />
            <button
              onClick={() => analyzeClaim(query)}
              disabled={state.isLoading}
              className="px-8 py-4 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold hover:shadow-lg hover:shadow-blue-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
            >
              {state.isLoading ? "Analyzing..." : "Analyze"}
            </button>
          </div>
        </motion.div>

        {/* Results */}
        {state.propagationMetrics ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-8"
          >
            {/* Threat Assessment */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.3 }}
            >
              <ScoreDisplay
                score={state.threatScore}
                riskLevel={state.riskLevel}
                confidence={state.threatScore / 100}
              />
            </motion.div>

            {/* Propagation Metrics */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.4 }}
            >
              <PropagationSpread metrics={state.propagationMetrics} />
            </motion.div>

            {/* Live Amplification Feed */}
            {state.amplificationPosts.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.5 }}
              >
                <h2 className="text-xl font-semibold text-white mb-4">
                  Top Amplifiers
                </h2>
                <LiveAmplificationFeed
                  posts={state.amplificationPosts}
                  isLive={false}
                />
              </motion.div>
            )}
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="rounded-3xl border border-white/15 bg-white/10 p-12 backdrop-blur-xl text-center"
          >
            <div className="max-w-md mx-auto">
              <div className="text-6xl mb-6">📊</div>
              <h2 className="text-2xl font-semibold text-white mb-4">
                Analyze Propaganda Spread
              </h2>
              <p className="text-gray-300 mb-6 text-lg">
                Enter a claim to see how it propagates across multiple news
                sources and social platforms
              </p>

              <div className="bg-white/10 rounded-lg p-6 mb-6 text-left">
                <h3 className="font-semibold text-white mb-3">
                  📰 Data Sources:
                </h3>
                <ul className="space-y-2 text-gray-300 text-sm">
                  <li className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-red-500"></span>
                    News RSS feeds (AP, BBC, Reuters, CNN)
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
                    GDELT global event database
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                    Telegram public channels
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-purple-500"></span>
                    CommonCrawl web archive (200B+ pages)
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
                    Facebook public posts
                  </li>
                </ul>
              </div>

              <div className="grid grid-cols-1 gap-2">
                <button
                  onClick={() => {
                    setQuery("vaccine safety concerns");
                    setTimeout(() => analyzeClaim("vaccine safety concerns"), 100);
                  }}
                  className="px-4 py-3 rounded-lg border border-white/20 text-white hover:border-white/40 hover:bg-white/10 transition-all text-sm font-medium"
                >
                  Example: "vaccine safety concerns"
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

function getThreatLevel(
  score: number
): "Critical" | "High" | "Medium" | "Low" | "None" {
  if (score >= 80) return "Critical";
  if (score >= 60) return "High";
  if (score >= 40) return "Medium";
  if (score >= 20) return "Low";
  return "None";
}
