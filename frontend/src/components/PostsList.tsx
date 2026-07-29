"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { PostItem } from "@/types/analysis";

interface PostsListProps {
  posts: PostItem[];
}

export function PostsList({ posts }: PostsListProps) {
  const [isLoading, setIsLoading] = useState(posts.length === 0);

  useEffect(() => {
    if (posts.length > 0) {
      setIsLoading(false);
    }
  }, [posts]);

  const getTargetUrl = (post: PostItem): string => {
    if (post.url && post.url.trim().length > 0) {
      return post.url;
    }
    if (post.urls && post.urls.length > 0 && post.urls[0].trim().length > 0) {
      return post.urls[0];
    }
    // Fallback: search engine link for source attribution verification
    const query = `${post.username} ${post.text.slice(0, 100)}`;
    return `https://www.google.com/search?q=${encodeURIComponent(query)}`;
  };

  return (
    <section 
      className="rounded-3xl border border-white/15 bg-white/10 p-6 backdrop-blur-xl"
      aria-label="Live amplification feed showing posts from sources"
      role="region"
    >
      <div className="flex items-center justify-between">
        <p className="text-xs uppercase tracking-[0.2em] text-[#99d2eb]">Live Source Feed</p>
        <span className="text-xs text-[#73d6ff]">🔗 Click any item to visit original source</span>
      </div>
      
      {isLoading ? (
        <motion.div 
          className="mt-5 space-y-3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {[1, 2, 3].map((i) => (
            <motion.div
              key={i}
              className="rounded-2xl border border-white/10 bg-[#0b2230]/70 p-4"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              <div className="h-4 bg-white/10 rounded w-1/3 mb-3" />
              <div className="h-3 bg-white/10 rounded w-full mb-2" />
              <div className="h-3 bg-white/10 rounded w-4/5 mb-3" />
              <div className="flex gap-4">
                <div className="h-3 bg-white/10 rounded w-20" />
                <div className="h-3 bg-white/10 rounded w-20" />
              </div>
            </motion.div>
          ))}
        </motion.div>
      ) : (
        <motion.div 
          className="mt-5 space-y-3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ staggerChildren: 0.08, delayChildren: 0.1 }}
        >
          {posts.map((post) => {
            const targetUrl = getTargetUrl(post);
            const isDirectLink = Boolean((post.url && post.url.trim()) || (post.urls && post.urls.length > 0));

            return (
              <motion.article
                key={post.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4 }}
                whileHover={{ scale: 1.01, y: -2 }}
                className="rounded-2xl border border-white/10 bg-[#0b2230]/70 p-4 transition-all hover:border-[#73d6ff]/60 group relative cursor-pointer"
                style={{
                  boxShadow: "0 0 0 0 rgba(115, 214, 255, 0)",
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLElement).style.boxShadow = "0 0 20px rgba(115, 214, 255, 0.25)";
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLElement).style.boxShadow = "0 0 0 0 rgba(115, 214, 255, 0)";
                }}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <a
                    href={targetUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm font-semibold text-[#73d6ff] hover:underline flex items-center gap-1.5"
                  >
                    <span>{post.username}</span>
                    <span className="text-xs opacity-75">↗</span>
                  </a>
                  <span className="text-xs text-[#89b7cb]">{post.timestamp}</span>
                </div>

                <a
                  href={targetUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-2 block text-sm leading-6 text-[#deecf4] hover:text-white transition-colors"
                >
                  {post.text}
                </a>

                <div className="mt-3 flex items-center justify-between text-xs text-[#9bc8db] pt-2 border-t border-white/5">
                  <div className="flex gap-4">
                    <span>❤️ Likes: {post.likes}</span>
                    <span>🔄 Shares: {post.shares}</span>
                  </div>
                  <a
                    href={targetUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-[#73d6ff] hover:text-[#a0e4ff] font-medium hover:underline"
                  >
                    <span>{isDirectLink ? "Visit Source Webpage" : "Verify on Search"}</span>
                    <span>↗</span>
                  </a>
                </div>
              </motion.article>
            );
          })}
        </motion.div>
      )}
    </section>
  );
}
