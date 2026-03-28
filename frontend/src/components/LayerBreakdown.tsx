"use client";

import { motion } from "framer-motion";
import type { LayerResult } from "@/types/analysis";

interface LayerBreakdownProps {
  layers: LayerResult[];
}

export function LayerBreakdown({ layers }: LayerBreakdownProps) {
  const statusTone = (status?: string) => {
    if (status === "unavailable") return "text-[#ff9b9b] bg-[#3a1b24]";
    if (status === "insufficient_evidence") return "text-[#ffd58b] bg-[#3a2f1a]";
    return "text-[#9fdfff] bg-[#0d2a39]";
  };

  const statusLabel = (status?: string) => {
    if (status === "unavailable") return "Unavailable";
    if (status === "insufficient_evidence") return "Limited Evidence";
    return "Available";
  };

  const evidenceEntries = (evidence?: Record<string, unknown>) => {
    if (!evidence) {
      return [] as Array<[string, unknown]>;
    }
    return Object.entries(evidence).filter(([, value]) => {
        if (value === null || value === undefined) {
          return false;
        }
        if (typeof value === "string") {
          return value.trim().length > 0;
        }
        if (Array.isArray(value)) {
          return value.length > 0;
        }
        if (typeof value === "object") {
          return Object.keys(value as Record<string, unknown>).length > 0;
        }
        return true;
      })
      .slice(0, 4);
  };

  const formatEvidenceValue = (value: unknown) => {
    if (typeof value === "number") {
      return Number.isInteger(value) ? String(value) : value.toFixed(3);
    }
    if (typeof value === "string") {
      return value;
    }
    if (Array.isArray(value)) {
      return value.join(", ");
    }
    if (typeof value === "object" && value !== null) {
      return Object.entries(value as Record<string, unknown>)
        .map(([key, nested]) => `${key}:${String(nested)}`)
        .join(", ");
    }
    return String(value);
  };

  const badgeCandidates = (layer: LayerResult): Array<[string, unknown]> => {
    const evidence = layer.evidence ?? {};
    const keysByLayer: Record<LayerResult["name"], string[]> = {
      NLP: ["urgencyHits", "urgencyTerms", "exclamationHits", "tokenCount"],
      GNN: ["coordinationDensity", "nodeCount", "linkCount", "clusterCount"],
      Gemini: ["verdict", "httpStatus", "model", "confidence"],
    };

    const keys = keysByLayer[layer.name] || [];
    return keys
      .map((key) => [key, evidence[key]] as [string, unknown])
      .filter(([, value]) => {
        if (value === null || value === undefined) {
          return false;
        }
        if (typeof value === "string") {
          return value.trim().length > 0;
        }
        if (Array.isArray(value)) {
          return value.length > 0;
        }
        return true;
      })
      .slice(0, 3);
  };

  const badgeTone = (layer: LayerResult) => {
    if (layer.status === "unavailable") {
      return "border-[#ff8f8f]/40 bg-[#3a1d25] text-[#ffb4b4]";
    }
    if (layer.status === "insufficient_evidence") {
      return "border-[#e8bb6c]/40 bg-[#3c2d18] text-[#ffd58b]";
    }
    return "border-[#70d6ff]/40 bg-[#103445] text-[#b9e7fb]";
  };

  return (
    <motion.section
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
      className="grid gap-4 lg:grid-cols-3"
      aria-label="Analysis layers: NLP, Graph neural network, and Gemini fact-check"
      role="region"
    >
      {layers.map((layer) => (
        <motion.article
          key={layer.name}
          variants={{
            hidden: { opacity: 0, y: 20 },
            show: { opacity: 1, y: 0 },
          }}
          className="rounded-2xl border border-white/15 bg-white/10 p-5 backdrop-blur-xl transition-all hover:border-[#73d6ff]/50 hover:bg-white/[0.12] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#73d6ff] focus-visible:ring-offset-2 focus-visible:ring-offset-[#031019] cursor-pointer"
        >
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-white">{layer.name}</h3>
            <motion.span 
              className={`rounded-full px-3 py-1 text-sm font-semibold ${statusTone(layer.status)}`}
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              {layer.score}
            </motion.span>
          </div>
          <p className="mt-2 text-xs uppercase tracking-[0.12em] text-[#9ec5d8]">
            {statusLabel(layer.status)}
            {typeof layer.confidence === "number" ? ` • ${Math.round(layer.confidence * 100)}% confidence` : ""}
          </p>
          <div className="mt-4 h-2 rounded-full bg-white/10">
            <motion.div
              initial={{ width: 0 }}
              whileInView={{ width: `${layer.score}%` }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              className="h-2 rounded-full bg-linear-to-r from-[#46d5ff] to-[#9af2d8]"
            />
          </div>
          <p className="mt-4 text-sm leading-6 text-[#cee6f3]">{layer.explanation}</p>
          {badgeCandidates(layer).length > 0 ? (
            <div className="mt-4 flex flex-wrap gap-2">
              {badgeCandidates(layer).map(([key, value]) => (
                <span
                  key={`${layer.name}-badge-${key}`}
                  className={`rounded-full border px-2.5 py-1 text-[11px] font-medium ${badgeTone(layer)}`}
                >
                  {key}: {formatEvidenceValue(value)}
                </span>
              ))}
            </div>
          ) : null}
          {evidenceEntries(layer.evidence).length > 0 ? (
            <div className="mt-4 rounded-xl border border-white/10 bg-[#091f2b] p-4">
              <p className="text-[11px] uppercase tracking-[0.12em] text-[#8ebdd3] mb-4">Evidence Signals</p>
              <div className="space-y-4">
                {evidenceEntries(layer.evidence).map(([key, value]) => (
                  <div key={`${layer.name}-${key}`} className="space-y-1.5">
                    <div className="flex justify-between items-center">
                      <span className="text-[11px] font-medium text-[#98cde6] capitalize">{key}</span>
                      <span className="text-[12px] font-semibold text-[#73d6ff]">{formatEvidenceValue(value)}</span>
                    </div>
                    
                    {/* Visual representation based on data type */}
                    {(() => {
                      // For ratio values (0-1 range)
                      if (typeof value === "number" && value >= 0 && value <= 1) {
                        return (
                          <motion.div 
                            className="h-1.5 rounded-full bg-white/10"
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            viewport={{ once: true }}
                          >
                            <motion.div
                              initial={{ width: 0 }}
                              whileInView={{ width: `${value * 100}%` }}
                              viewport={{ once: true }}
                              transition={{ duration: 0.6, ease: "easeOut" }}
                              className={`h-1.5 rounded-full ${
                                value > 0.7 ? "bg-red-500" : 
                                value > 0.4 ? "bg-yellow-500" : 
                                "bg-green-500"
                              }`}
                            />
                          </motion.div>
                        );
                      }
                      
                      // For count values (0+)
                      if (typeof value === "number" && Number.isInteger(value) && value >= 0) {
                        const maxVal = key === "tokenCount" ? 100 : key === "nodeCount" ? 50 : 20;
                        const percentage = Math.min((value / maxVal) * 100, 100);
                        return (
                          <motion.div 
                            className="h-2 rounded-full bg-white/10 overflow-hidden"
                            initial={{ opacity: 0 }}
                            whileInView={{ opacity: 1 }}
                            viewport={{ once: true }}
                          >
                            <motion.div
                              initial={{ width: 0 }}
                              whileInView={{ width: `${percentage}%` }}
                              viewport={{ once: true }}
                              transition={{ duration: 0.6, ease: "easeOut" }}
                              className="h-2 rounded-full bg-gradient-to-r from-[#73d6ff] to-[#7df5c5]"
                            />
                          </motion.div>
                        );
                      }
                      
                      return null;
                    })()}
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </motion.article>
      ))}
    </motion.section>
  );
}
