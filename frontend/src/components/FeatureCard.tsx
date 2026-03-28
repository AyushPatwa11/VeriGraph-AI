"use client";

import { motion } from "framer-motion";

interface FeatureCardProps {
  title: string;
  description: string;
  accent: string;
}

export function FeatureCard({ title, description, accent }: FeatureCardProps) {
  return (
    <motion.article
      whileHover={{ y: -10, scale: 1.02 }}
      transition={{ type: "spring", stiffness: 200, damping: 18 }}
      className="group relative overflow-hidden rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl"
    >
      <div
        className="pointer-events-none absolute -top-20 -right-20 h-40 w-40 rounded-full opacity-40 blur-2xl"
        style={{ background: accent }}
      />
      <h3 className="text-lg font-semibold text-white">{title}</h3>
      <svg viewBox="0 0 200 80" className="w-full h-16 mt-4" aria-hidden="true">
        <polyline points="0,40 10,30 20,35 30,25 40,30 50,20 60,30 70,25 80,35 90,30 100,40 110,35 120,45 130,40 140,50 150,45 160,55 170,50 180,60 190,55 200,60" fill="none" stroke={accent} strokeWidth="2" opacity="0.7" />
      </svg>
      <p className="mt-4 text-sm leading-6 text-[#cae5f3]">{description}</p>
      <div className="mt-6 text-xs font-medium uppercase tracking-widest text-[#93d5f7]">
        Interactive Module
      </div>
    </motion.article>
  );
}
