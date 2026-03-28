"use client";

import { motion } from "framer-motion";
import { FeatureCard } from "@/components/FeatureCard";

const features = [
  {
    title: "Semantic Threat Signal",
    description:
      "Transformer-powered language analysis catches manipulative patterns, urgency framing, and sentiment pressure in real time.",
    accent: "#33c4ff",
  },
  {
    title: "Coordination Graph Lens",
    description:
      "Force-directed relationship graph surfaces synchronized bursts, repeated links, and account cluster behavior instantly.",
    accent: "#63f9d2",
  },
  {
    title: "Fact Validation Layer",
    description:
      "Gemini fact verification adds truth assessment with confidence scoring and compact evidence explanation.",
    accent: "#f8d46b",
  },
  {
    title: "Realtime Intelligence Feed",
    description:
      "Live post cards animate into view while counters and cluster metrics update smoothly for a broadcast-style experience.",
    accent: "#ff7d6b",
  },
];

export function FeatureShowcase() {
  return (
    <motion.section
      id="features"
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, amount: 0.2 }}
      variants={{
        hidden: {},
        show: {
          transition: {
            staggerChildren: 0.12,
          },
        },
      }}
      className="mx-auto w-full max-w-7xl px-6 py-16"
    >
      <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
        Why VeriGraph feels different
      </h2>
      <p className="mt-4 max-w-3xl text-[#c8e1ee]">
        This is not a static report. It is a living misinformation radar with layered evidence and
        tactile interactions.
      </p>
      
      {/* Process Timeline */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.6 }}
        className="mt-12 rounded-2xl border border-white/15 bg-white/[0.06] p-8 mb-10"
      >
        <p className="text-xs uppercase tracking-[0.2em] text-[#96c9df] font-semibold mb-6">Analysis Pipeline</p>
        <div className="flex flex-wrap items-center justify-between gap-0">
          {[
            { label: "Input Claim", icon: "📝" },
            { label: "NLP Analysis", icon: "🧠" },
            { label: "Network Map", icon: "🔗" },
            { label: "Fact Check", icon: "✓" },
            { label: "Results", icon: "📊" },
          ].map((item, idx) => (
            <motion.div
              key={idx}
              className="flex flex-col items-center flex-1"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: idx * 0.12 }}
            >
              <motion.div
                className="relative z-10 w-12 h-12 rounded-full border-2 border-[#73d6ff] bg-[#0a2535] flex items-center justify-center mb-2 text-lg"
                whileHover={{ boxShadow: "0 0 15px rgba(115, 214, 255, 0.4)", scale: 1.08 }}
              >
                {item.icon}
              </motion.div>
              <span className="text-xs font-semibold text-[#dcf1fb] text-center">{item.label}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>

      <div className="mt-10 grid gap-5 md:grid-cols-2">
        {features.map((feature) => (
          <motion.div
            key={feature.title}
            variants={{
              hidden: { opacity: 0, y: 30 },
              show: { opacity: 1, y: 0, transition: { duration: 0.55 } },
            }}
          >
            <FeatureCard {...feature} />
          </motion.div>
        ))}
      </div>
    </motion.section>
  );
}
