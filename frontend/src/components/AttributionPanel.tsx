"use client";

import { motion } from "framer-motion";

interface AttributionPanelProps {
  summary: string;
}

export function AttributionPanel({ summary }: AttributionPanelProps) {
  // Extract key metrics from summary
  const isInconclusive = summary.toLowerCase().includes("inconclusive");
  const confidenceMatch = summary.match(/(\d+)%/);
  const confidence = confidenceMatch ? confidenceMatch[1] : "N/A";
  const nlpMatch = summary.match(/NLP=(\d+)/)?.[1];
  const gnnMatch = summary.match(/GNN=(\d+)/)?.[1];
  const geminiMatch = summary.match(/Gemini=(\d+)/)?.[1];
  const accountsMatch = summary.match(/observed (\d+) accounts/);
  const accounts = accountsMatch ? accountsMatch[1] : "0";

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.45 }}
      className="rounded-3xl border border-white/15 bg-[#08212d]/85 p-6 backdrop-blur-xl"
      aria-label="Attribution summary and analysis conclusion"
      role="region"
    >
      <p className="text-xs uppercase tracking-[0.2em] text-[#96d7f5]">Attribution Summary</p>
      
      <div className="mt-4 space-y-3">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm font-semibold text-white">
              {isInconclusive ? "⚠ Inconclusive" : "✓ Complete"}
            </p>
            <p className="text-xs text-[#96c9df] mt-1">
              {accounts} account{accounts !== "1" ? "s" : ""} detected • Confidence {confidence}%
            </p>
          </div>
          <div className="flex gap-2 flex-wrap justify-end">
            {nlpMatch && <span className="text-xs px-2 py-1 rounded bg-[#73d6ff]/20 text-[#73d6ff] font-semibold">NLP {nlpMatch}</span>}
            {gnnMatch && <span className="text-xs px-2 py-1 rounded bg-[#7df5c5]/20 text-[#7df5c5] font-semibold">GNN {gnnMatch}</span>}
            {geminiMatch && <span className="text-xs px-2 py-1 rounded bg-[#ffc96f]/20 text-[#ffc96f] font-semibold">Gemini {geminiMatch}</span>}
          </div>
        </div>
        {isInconclusive && (
          <p className="text-xs text-[#d0e4f0]">Inconsistent evidence across layers. More data recommended before final verdict.</p>
        )}
      </div>
    </motion.section>
  );
}
