"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

const getTone = (score: number): string => {
  if (score >= 70) return "#ff6b5a";
  if (score >= 40) return "#f2bf55";
  return "#4ad79a";
};

interface SpreadMetrics {
  total_reach: {
    total_reach: number;
    total_likes: number;
    total_shares: number;
    total_comments: number;
    post_count: number;
    average_engagement_per_post: number;
  };
  platform_breakdown: {
    platform_distribution: Record<
      string,
      {
        post_count: number;
        total_engagement: number;
        avg_engagement: number;
        reach_percentage: number;
        likes: number;
        shares: number;
        comments: number;
      }
    >;
    platforms_with_posts: string[];
  };
  timeline: {
    timeline_buckets: Record<
      string,
      {
        post_count: number;
        total_engagement: number;
        growth_rate: number;
        date_range: { start: string; end: string };
      }
    >;
    spread_pattern: "exponential" | "linear" | "declining" | "flat" | "none";
    peak_period: string | null;
  };
  top_spreaders: Array<{
    username: string;
    author_id: string;
    platform: string;
    post_count: number;
    total_engagement: number;
    avg_engagement_per_post: number;
    total_likes: number;
    total_shares: number;
    total_comments: number;
  }>;
  virality: {
    viral_coefficient: number;
    doubling_time_hours: number | null;
    growth_rate: number;
    viral_classification:
      | "non-viral"
      | "slow"
      | "moderate"
      | "fast"
      | "explosive";
    virality_score: number;
  };
}

interface PropagationSpreadProps {
  metrics: SpreadMetrics | null;
  isLoading?: boolean;
}

export function PropagationSpread({
  metrics,
  isLoading = false,
}: PropagationSpreadProps) {
  const [animatedReach, setAnimatedReach] = useState(0);
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    if (!metrics) return;

    // Animate total reach
    const reachTarget = metrics.total_reach.total_reach;
    const reachDuration = 1.5;
    const startTime = Date.now();

    const animateReach = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / (reachDuration * 1000), 1);
      setAnimatedReach(Math.floor(reachTarget * progress));

      if (progress < 1) {
        requestAnimationFrame(animateReach);
      }
    };

    animateReach();

    // Animate virality score
    const scoreTarget = metrics.virality.virality_score;
    const scoreDuration = 1.8;
    const scoreStartTime = Date.now();

    const animateScore = () => {
      const elapsed = Date.now() - scoreStartTime;
      const progress = Math.min(elapsed / (scoreDuration * 1000), 1);
      setAnimatedScore(Math.floor(scoreTarget * progress));

      if (progress < 1) {
        requestAnimationFrame(animateScore);
      }
    };

    animateScore();
  }, [metrics]);

  if (isLoading) {
    return (
      <div className="space-y-4 p-6">
        <div className="h-8 bg-white/10 rounded-lg animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[...Array(4)].map((_, i) => (
            <div
              key={i}
              className="h-32 bg-white/10 rounded-lg animate-pulse"
            />
          ))}
        </div>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="text-center p-6 text-gray-400">
        <p>No propagation data available</p>
      </div>
    );
  }

  const viralityColor =
    metrics.virality.virality_score >= 70
      ? "#ff6b5a"
      : metrics.virality.virality_score >= 40
        ? "#f2bf55"
        : "#4ad79a";

  return (
    <section
      className="space-y-6 rounded-3xl border border-white/15 bg-white/10 p-8 backdrop-blur-xl"
      style={{
        boxShadow: `0 0 40px ${viralityColor}20, inset 0 1px 0 ${viralityColor}10`,
      }}
    >
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h2 className="text-lg font-semibold text-white">
          Propagation Spread Analysis
        </h2>
        <p className="text-sm text-gray-400 mt-2">
          How the claim is spreading across {metrics.platform_breakdown.platforms_with_posts.length} sources
        </p>
      </motion.div>

      {/* Main Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Total Reach Card */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm hover:border-white/20 transition-colors"
        >
          <p className="text-xs uppercase tracking-widest text-gray-400 font-medium">
            Total Reach
          </p>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">
              {animatedReach.toLocaleString()}
            </span>
            <span className="text-gray-400">engagements</span>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-2 text-xs">
            <div>
              <p className="text-gray-500">Likes</p>
              <p className="text-white font-semibold">
                {metrics.total_reach.total_likes.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-gray-500">Shares</p>
              <p className="text-white font-semibold">
                {metrics.total_reach.total_shares.toLocaleString()}
              </p>
            </div>
            <div>
              <p className="text-gray-500">Comments</p>
              <p className="text-white font-semibold">
                {metrics.total_reach.total_comments.toLocaleString()}
              </p>
            </div>
          </div>
        </motion.div>

        {/* Virality Score Card */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm hover:border-white/20 transition-colors"
          style={{
            borderColor: `${viralityColor}40`,
            backgroundColor: `${viralityColor}10`,
          }}
        >
          <p className="text-xs uppercase tracking-widest font-medium" style={{ color: viralityColor }}>
            Virality Score
          </p>
          <div className="mt-4 flex items-center justify-between">
            <div>
              <div className="text-4xl font-bold" style={{ color: viralityColor }}>
                {animatedScore}
              </div>
              <p className="text-sm capitalize mt-2">
                <span style={{ color: viralityColor }}>
                  {metrics.virality.viral_classification}
                </span>
              </p>
            </div>
            <div className="relative w-24 h-24">
              <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke="rgba(255,255,255,0.1)"
                  strokeWidth="8"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  fill="none"
                  stroke={viralityColor}
                  strokeWidth="8"
                  strokeDasharray={`${2 * Math.PI * 45}`}
                  strokeDashoffset={`${2 * Math.PI * 45 * (1 - animatedScore / 100)}`}
                  strokeLinecap="round"
                  style={{ transition: "stroke-dashoffset 0.3s ease" }}
                />
              </svg>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Platform Breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm"
      >
        <h3 className="text-sm font-semibold text-white mb-4">
          Platform Distribution
        </h3>
        <div className="space-y-3">
          {metrics.platform_breakdown.platforms_with_posts.map((platform) => {
            const data =
              metrics.platform_breakdown.platform_distribution[platform];
            const platformColor = getPlatformColor(platform);

            return (
              <div key={platform} className="space-y-1">
                <div className="flex justify-between items-center">
                  <span className="text-sm capitalize font-medium text-gray-300">
                    {platform}
                  </span>
                  <span className="text-xs text-gray-500">
                    {data.reach_percentage.toFixed(1)}% • {data.post_count} posts
                  </span>
                </div>
                <div className="w-full bg-white/5 rounded-full h-2 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${data.reach_percentage}%` }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: platformColor }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </motion.div>

      {/* Timeline Spread */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.4 }}
        className="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm"
      >
        <h3 className="text-sm font-semibold text-white mb-4">Spread Timeline</h3>
        <div className="space-y-3">
          {["24h", "7d", "30d"].map((period) => {
            const data = metrics.timeline.timeline_buckets[period];
            if (!data) return null;

            const isHighest =
              period ===
              Object.entries(metrics.timeline.timeline_buckets).reduce(
                (max, [key, val]) =>
                  val.total_engagement > max.engagement
                    ? { key, engagement: val.total_engagement }
                    : max,
                { key: "", engagement: 0 }
              ).key;

            return (
              <div
                key={period}
                className={`p-3 rounded-lg border transition-colors ${
                  isHighest
                    ? "border-white/20 bg-white/10"
                    : "border-white/5 bg-white/5"
                }`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm font-medium text-white">
                      Last {period}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {data.post_count} posts
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-semibold text-white">
                      {data.total_engagement}
                    </p>
                    {data.growth_rate !== 0 && (
                      <p
                        className="text-xs mt-1"
                        style={{
                          color:
                            data.growth_rate > 0 ? "#4ad79a" : "#ff6b5a",
                        }}
                      >
                        {data.growth_rate > 0 ? "+" : ""}
                        {data.growth_rate.toFixed(1)}%
                      </p>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
          <p className="text-xs text-gray-500 mt-4">
            Pattern: <span className="capitalize text-gray-300 font-medium">{metrics.timeline.spread_pattern}</span>
          </p>
        </div>
      </motion.div>

      {/* Top Spreaders */}
      {metrics.top_spreaders.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.5 }}
          className="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm"
        >
          <h3 className="text-sm font-semibold text-white mb-4">
            Top 5 Spreaders
          </h3>
          <div className="space-y-2">
            {metrics.top_spreaders.slice(0, 5).map((spreader, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-3 rounded-lg border border-white/5 bg-white/5 hover:border-white/10 transition-colors"
              >
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                    <span className="text-xs font-semibold">#{idx + 1}</span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">
                      {spreader.username}
                    </p>
                    <p className="text-xs text-gray-500 capitalize">
                      {spreader.platform}
                    </p>
                  </div>
                </div>
                <div className="flex-shrink-0 text-right">
                  <p className="text-sm font-semibold text-white">
                    {spreader.total_engagement}
                  </p>
                  <p className="text-xs text-gray-500">
                    {spreader.post_count} posts
                  </p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Virality Details */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.6 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
      >
        <div className="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur-sm">
          <p className="text-xs uppercase tracking-widest text-gray-400 font-medium">
            Daily Growth Rate
          </p>
          <p className="text-2xl font-bold text-white mt-3">
            {metrics.virality.growth_rate.toFixed(2)}%
          </p>
        </div>
        {metrics.virality.doubling_time_hours && (
          <div className="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur-sm">
            <p className="text-xs uppercase tracking-widest text-gray-400 font-medium">
              Doubling Time
            </p>
            <p className="text-2xl font-bold text-white mt-3">
              {metrics.virality.doubling_time_hours < 24
                ? `${(metrics.virality.doubling_time_hours).toFixed(1)}h`
                : `${(metrics.virality.doubling_time_hours / 24).toFixed(1)}d`}
            </p>
          </div>
        )}
      </motion.div>
    </section>
  );
}

function getPlatformColor(platform: string): string {
  const colors: Record<string, string> = {
    facebook: "#1f97ff",
    news: "#ff6b6b",
    gdelt: "#ffd43b",
    telegram: "#229ed9",
    commoncrawl: "#845ef7",
  };
  return colors[platform] || "#96c9df";
}
