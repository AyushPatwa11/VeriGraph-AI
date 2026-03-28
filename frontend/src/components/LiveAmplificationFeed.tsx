"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";

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

interface LiveAmplificationFeedProps {
  posts?: AmplificationPost[];
  isLive?: boolean;
  onLinkClick?: (url: string) => void;
}

const getSourceColor = (source: string): string => {
  const colors: Record<string, string> = {
    "ap news": "#ff6b6b",
    "bbc": "#4c72b0",
    "cnn": "#e74c3c",
    "reuters": "#f39c12",
    "The New York Times": "#1f77b4",
    "The Guardian": "#2ca02c",
    "Washington Post": "#d62728",
    "MSNBC": "#ff7f0e",
    "facebook": "#1f97ff",
    "news": "#ff6b6b",
    "gdelt": "#ffd43b",
    "telegram": "#229ed9",
    "commoncrawl": "#845ef7",
  };

  const lowerSource = source.toLowerCase();
  for (const [key, color] of Object.entries(colors)) {
    if (lowerSource.includes(key.toLowerCase())) {
      return color;
    }
  }
  return "#96c9df";
};

const getTimeAgo = (timestamp: string): string => {
  try {
    const date = new Date(timestamp);
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  } catch {
    return timestamp;
  }
};

export function LiveAmplificationFeed({
  posts = [],
  isLive = true,
  onLinkClick,
}: LiveAmplificationFeedProps) {
  const [displayPosts, setDisplayPosts] = useState<AmplificationPost[]>(posts);
  const [newPostCount, setNewPostCount] = useState(0);

  useEffect(() => {
    if (posts.length > 0) {
      setDisplayPosts(posts);
    }
  }, [posts]);

  const handleLinkClick = (url: string | undefined) => {
    if (url) {
      if (onLinkClick) {
        onLinkClick(url);
      }
      window.open(url, "_blank", "noopener,noreferrer");
    }
  };

  if (displayPosts.length === 0) {
    return (
      <section className="rounded-3xl border border-white/15 bg-white/10 p-8 backdrop-blur-xl">
        <div className="flex items-center gap-3 mb-6">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isLive ? "animate-pulse bg-red-500" : "bg-gray-500"}`} />
            <h2 className="text-lg font-semibold text-white">
              Live Amplification Feed
            </h2>
          </div>
        </div>
        <p className="text-center text-gray-400 py-8">
          No posts found. Run an analysis to see live amplification data.
        </p>
      </section>
    );
  }

  return (
    <section
      className="rounded-3xl border border-white/15 bg-white/10 p-8 backdrop-blur-xl"
      style={{
        boxShadow: `0 0 40px #ff6b5a20, inset 0 1px 0 #ff6b5a10`,
      }}
    >
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between mb-6"
      >
        <div className="flex items-center gap-3">
          <div className={`w-2 h-2 rounded-full ${isLive ? "animate-pulse bg-red-500" : "bg-gray-500"}`} />
          <h2 className="text-lg font-semibold text-white">
            Live Amplification Feed
          </h2>
          {newPostCount > 0 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="ml-4 px-3 py-1 rounded-full bg-red-500/20 border border-red-500/50"
            >
              <span className="text-xs font-semibold text-red-400">
                {newPostCount} new
              </span>
            </motion.div>
          )}
        </div>
        <p className="text-xs text-gray-400">
          {displayPosts.length} posts spreading
        </p>
      </motion.div>

      {/* Posts List */}
      <div className="space-y-3">
        <AnimatePresence>
          {displayPosts.map((post, idx) => {
            const sourceColor = getSourceColor(post.source);
            const totalEngagement = post.likes + post.shares;
            const isHighEngagement = totalEngagement > 300;

            return (
              <motion.div
                key={post.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: idx * 0.05 }}
                onClick={() => handleLinkClick(post.url)}
                className={`group relative p-4 rounded-xl border transition-all cursor-pointer ${
                  post.url
                    ? "border-white/10 hover:border-white/30 hover:bg-white/8"
                    : "border-white/10 bg-white/5"
                }`}
                style={{
                  borderColor: isHighEngagement ? `${sourceColor}40` : undefined,
                  backgroundColor: isHighEngagement ? `${sourceColor}08` : undefined,
                }}
              >
                {/* High Engagement Badge */}
                {isHighEngagement && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="absolute -top-2 -right-2"
                  >
                    <div
                      className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white"
                      style={{ backgroundColor: sourceColor }}
                    >
                      🔥
                    </div>
                  </motion.div>
                )}

                {/* Content Grid */}
                <div className="flex items-start justify-between gap-4">
                  {/* Left: Source + Title */}
                  <div className="flex-1 min-w-0">
                    {/* Source + Time */}
                    <div className="flex items-center gap-2 mb-2">
                      <div
                        className="w-2 h-2 rounded-full flex-shrink-0"
                        style={{ backgroundColor: sourceColor }}
                      />
                      <span
                        className="text-xs font-semibold"
                        style={{ color: sourceColor }}
                      >
                        {post.source.toUpperCase()}
                      </span>
                      <span className="text-xs text-gray-500">
                        {getTimeAgo(post.timestamp)}
                      </span>
                    </div>

                    {/* Title */}
                    {post.url ? (
                      <a
                        href={post.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="text-sm font-medium text-white leading-tight mb-2 line-clamp-2 hover:text-blue-300 hover:underline transition-colors block"
                      >
                        {post.title}
                      </a>
                    ) : (
                      <h3 className="text-sm font-medium text-white leading-tight mb-2 line-clamp-2">
                        {post.title}
                      </h3>
                    )}

                    {/* Text Preview */}
                    {post.text && (
                      <p className="text-xs text-gray-400 line-clamp-2 mb-2">
                        {post.text}
                      </p>
                    )}

                    {/* Author */}
                    {post.author && (
                      <p className="text-xs text-gray-500">
                        by{" "}
                        {post.url ? (
                          <a
                            href={post.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={(e) => e.stopPropagation()}
                            className="text-blue-400 hover:text-blue-300 hover:underline font-medium transition-colors"
                          >
                            {post.author}
                          </a>
                        ) : (
                          <span className="text-gray-400">{post.author}</span>
                        )}
                      </p>
                    )}
                  </div>

                  {/* Right: Engagement Metrics */}
                  <div className="flex-shrink-0 flex flex-col items-end gap-3">
                    {/* Engagement Numbers */}
                    <div className="flex items-center gap-4 text-sm">
                      <div className="text-center">
                        <div className="text-xl font-bold text-red-400">
                          {post.likes}
                        </div>
                        <p className="text-xs text-gray-500">Likes</p>
                      </div>
                      <div className="text-center">
                        <div className="text-xl font-bold text-blue-400">
                          {post.shares}
                        </div>
                        <p className="text-xs text-gray-500">Shares</p>
                      </div>
                    </div>

                    {/* Total Engagement Bar */}
                    <div className="w-32 bg-white/5 rounded-full h-1.5 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: "100%" }}
                        transition={{ duration: 1 }}
                        className="h-full rounded-full"
                        style={{
                          background: `linear-gradient(90deg, ${sourceColor}80, ${sourceColor})`,
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Link Indicator */}
                {post.url && (
                  <div className="mt-3 flex items-center gap-1 text-xs text-gray-400 group-hover:text-gray-300 transition-colors">
                    <span>🔗</span>
                    <a
                      href={post.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="hover:text-blue-400 hover:underline truncate"
                    >
                      {post.url}
                    </a>
                  </div>
                )}
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="mt-6 pt-4 border-t border-white/10 flex items-center justify-between"
      >
        <p className="text-xs text-gray-400">
          {isLive && "🔴 Live — Updates every 30s"}
        </p>
        <p className="text-xs text-gray-500">
          Last updated: {new Date().toLocaleTimeString()}
        </p>
      </motion.div>
    </section>
  );
}
