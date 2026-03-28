"use client";

import { useEffect, useState } from "react";
import { animate, motion } from "framer-motion";

interface ScoreDisplayProps {
  score: number;
  riskLevel: string;
  resultStatus?: "final" | "inconclusive";
  confidence?: number;
}

function getTone(score: number, resultStatus?: "final" | "inconclusive") {
  if (resultStatus === "inconclusive") return "#74c1ff";
  if (score >= 70) return "#ff6b5a";
  if (score >= 40) return "#f2bf55";
  return "#4ad79a";
}

export function ScoreDisplay({ score, riskLevel, resultStatus = "final", confidence }: ScoreDisplayProps) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const controls = animate(0, score, {
      duration: 1.8,
      ease: "easeOut",
      onUpdate: (latest) => setAnimatedScore(Math.round(latest)),
    });

    return () => controls.stop();
  }, [score]);

  const radius = 78;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.max(0, Math.min(100, animatedScore));
  const strokeDashoffset = circumference * (1 - progress / 100);
  const tone = getTone(score, resultStatus);
  const confidencePct = confidence === undefined ? null : Math.round(confidence * 100);

  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45 }}
      className="relative rounded-3xl border border-white/15 bg-white/10 p-8 backdrop-blur-xl overflow-hidden"
      style={{
        boxShadow: `0 0 40px ${tone}20, inset 0 1px 0 ${tone}10`,
      }}
      aria-label={`Threat assessment: ${animatedScore} out of 100, Risk level: ${riskLevel}`}
      role="region"
    >
      <p className="text-xs uppercase tracking-[0.2em] font-semibold text-[#96c9df]">Threat Assessment</p>
      <div className="mt-7 flex flex-wrap items-center gap-12">
        <motion.div 
          className="relative h-52 w-52" 
          whileHover={{ scale: 1.05 }} 
          transition={{ duration: 0.3 }}
        >
          <div className="absolute inset-0 rounded-full blur-xl opacity-30" style={{ backgroundColor: tone }} />
          <svg viewBox="0 0 200 200" className="h-full w-full -rotate-90 relative z-10">
            <circle cx="100" cy="100" r={radius} fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="16" />
            <circle
              cx="100"
              cy="100"
              r={radius}
              fill="none"
              stroke={tone}
              strokeWidth="16"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              style={{ transition: "stroke-dashoffset 160ms linear" }}
            />
          </svg>
          <div className="absolute inset-0 grid place-items-center">
            <div className="text-center">
              <p className="text-4xl font-bold text-white">{animatedScore}</p>
              <p className="text-xs uppercase tracking-[0.2em] text-[#9bc7dd]">/ 100</p>
            </div>
          </div>
        </motion.div>

        <motion.div 
          className="flex flex-col gap-6 flex-1" 
          initial={{ opacity: 0, x: 20 }} 
          animate={{ opacity: 1, x: 0 }} 
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center gap-3">
            <div className="flex items-baseline gap-2">
              <motion.span 
                className="text-7xl font-bold tracking-tight" 
                style={{ color: tone }}
                key={animatedScore}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
              >
                {animatedScore}
              </motion.span>
              <span className="text-lg text-[#89b7cb] font-medium">/100</span>
            </div>
          </div>
          
          <div className="space-y-3 border-t border-white/10 pt-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-[#96c9df]">Risk Level</span>
              <span className="px-3 py-1.5 rounded-full text-sm font-semibold" style={{
                backgroundColor: `${tone}15`,
                color: tone,
                border: `1px solid ${tone}40`,
              }}>
                {riskLevel}
              </span>
            </div>
            
            {resultStatus === "inconclusive" ? (
              <div className="flex items-center justify-between text-sm">
                <span className="text-[#96c9df]">Status</span>
                <span className="text-[#f2bf55] font-medium">⚠ Inconclusive</span>
              </div>
            ) : null}
            
            {confidencePct !== null ? (
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-[#96c9df]">Confidence</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 h-2 bg-white/10 rounded-full overflow-hidden">
                    <motion.div 
                      className="h-full rounded-full" 
                      style={{ backgroundColor: tone }}
                      initial={{ width: 0 }}
                      animate={{ width: `${confidencePct}%` }}
                      transition={{ delay: 1, duration: 0.8 }}
                    />
                  </div>
                  <span className="text-sm font-semibold" style={{ color: tone }}>{confidencePct}%</span>
                </div>
              </div>
            ) : null}
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}
