"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ParticleBackdrop } from "@/components/ParticleBackdrop";
import { NetworkGraph } from "@/components/NetworkGraph";

const words = ["Realtime", "Trust", "Detection"];

export function Hero() {
  return (
    <section className="relative overflow-hidden px-6 pb-20 pt-8 min-h-screen flex flex-col justify-center">
      <div className="hero-gradient pointer-events-none absolute inset-0" aria-hidden="true" />
      <ParticleBackdrop />

      {/* Video Background - Transparent Looping */}
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.2 }}
        className="absolute top-0 left-0 right-0 h-[600px] z-0 overflow-hidden"
      >
        <video
          autoPlay
          muted
          loop
          playsInline
          className="w-full h-full object-cover opacity-40 mix-blend-screen absolute inset-0"
          style={{ background: "transparent" }}
        >
          <source src="/VeriGraph_AI_Trust_Your_Data.mp4" type="video/mp4" />
        </video>
        {/* Gradient overlay to blend video smoothly */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#031019]/30 to-[#031019] pointer-events-none" />
      </motion.div>

      <div className="relative mx-auto w-full max-w-7xl z-10">
        <motion.p
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="inline-flex rounded-full border border-[#84d8ff]/40 bg-[#06202d]/70 px-4 py-2 text-xs uppercase tracking-[0.2em] text-[#a4daf5] backdrop-blur-sm"
        >
          🎬 Coordinated Misinformation Radar
        </motion.p>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.6 }}
          className="mt-12 max-w-5xl text-5xl sm:text-6xl xl:text-7xl font-bold leading-[1.1] text-white"
        >
          <span className="bg-gradient-to-r from-[#e8f5ff] via-[#9be2ff] to-[#73d6ff] bg-clip-text text-transparent">
            VeriGraph AI:
          </span>
          <span className="block mt-2">
            Detect coordinated deception with{" "}
            <span className="inline-flex flex-wrap gap-3 mt-3">
              {words.map((word, index) => (
                <motion.span
                  key={word}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + index * 0.12, duration: 0.5 }}
                  className="rounded-2xl bg-gradient-to-r from-[#9be2ff]/40 to-[#7df5c5]/20 px-4 py-2 text-[#9be2ff] font-bold border border-[#9be2ff]/50 backdrop-blur-md shadow-lg shadow-[#73d6ff]/20"
                >
                  {word}
                </motion.span>
              ))}
            </span>
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="mt-8 max-w-3xl text-base sm:text-lg leading-8 text-[#d0e4f0]"
        >
          Hybrid intelligence across <span className="text-[#9be2ff] font-semibold">language semantics</span>, 
          <span className="text-[#7df5c5] font-semibold"> account networks</span>, and 
          <span className="text-[#ffc96f] font-semibold"> fact verification</span>. Built to show judges real impact in one glance.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
          className="mt-10 flex flex-wrap gap-4"
        >
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <Link
              href="/analysis"
              className="inline-flex rounded-full border-2 border-[#73d6ff]/80 bg-gradient-to-r from-[#73d6ff]/25 to-[#7dd7ff]/15 px-8 py-4 text-sm font-bold text-[#e8f5ff] transition-all duration-300 hover:border-[#73d6ff] hover:from-[#73d6ff]/35 hover:to-[#7dd7ff]/25 hover:shadow-2xl hover:shadow-[#73d6ff]/25 backdrop-blur-md items-center gap-2"
            >
              <span>⚡</span> Launch Live Dashboard
            </Link>
          </motion.div>
          <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
            <a
              href="#features"
              className="inline-flex rounded-full border-2 border-white/30 bg-white/8 px-8 py-4 text-sm font-bold text-white transition-all duration-300 hover:border-white/50 hover:bg-white/12 hover:shadow-xl backdrop-blur-md items-center gap-2"
            >
              <span>↓</span> Explore Features
            </a>
          </motion.div>
        </motion.div>

        {/* Stats Bar */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
          className="mt-16 grid grid-cols-3 gap-4 sm:gap-8"
        >
          {[
            { label: "Analysis Layers", value: "3" },
            { label: "Data Sources", value: "1000+" },
            { label: "Real-time Processing", value: "99.9%" },
          ].map((stat, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 + idx * 0.1 }}
              className="relative"
            >
              <div className="rounded-xl border border-white/15 bg-white/5 p-4 sm:p-6 backdrop-blur-sm hover:bg-white/8 transition-all duration-300 group">
                <p className="text-2xl sm:text-3xl font-bold text-[#9be2ff] group-hover:text-[#e8f5ff] transition-colors">{stat.value}</p>
                <p className="text-xs sm:text-sm text-[#96c9df] mt-1">{stat.label}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
