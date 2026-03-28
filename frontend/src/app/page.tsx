"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { FeatureShowcase } from "@/components/FeatureShowcase";
import { Footer } from "@/components/Footer";
import { analyzeClaim } from "@/lib/api";

export default function Home() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string>("");

  const handleAnalyze = async () => {
    const trimmed = query.trim();
    if (trimmed.length < 4 || isAnalyzing) {
      return;
    }

    setError("");
    setIsAnalyzing(true);
    try {
      const result = await analyzeClaim(trimmed);
      window.sessionStorage.setItem("verigraph.analysis", JSON.stringify(result));
      router.push("/analysis");
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "Unable to analyze claim right now.";
      setError(message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#031019] text-white">
      <Navbar />
      <main>
        <Hero />

        <section className="relative mx-auto w-full max-w-7xl px-6 py-20">
          {/* Background elements */}
          <div className="absolute inset-0 -z-10 opacity-40">
            <div className="absolute top-0 right-0 h-80 w-80 rounded-full bg-[#73d6ff]/20 blur-3xl" />
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6 }}
            className="rounded-3xl border border-white/20 bg-gradient-to-br from-white/12 to-white/5 p-8 backdrop-blur-2xl shadow-2xl"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="w-1 h-8 bg-gradient-to-b from-[#73d6ff] to-[#7df5c5] rounded-full" />
              <p className="text-xs uppercase tracking-[0.3em] font-bold text-[#9be2ff]">Realtime Claim Check</p>
            </div>

            <h2 className="mt-3 text-3xl sm:text-4xl font-bold text-white leading-tight">
              Drop any suspicious claim and launch analysis
            </h2>

            <p className="mt-4 max-w-2xl text-[#d0e4f0]">
              Analyze breaking news, rumors, and claims across millions of websites in real-time.
            </p>

            <div className="mt-8 flex flex-col gap-4 sm:flex-row">
              <motion.input
                whileFocus={{ scale: 1.02 }}
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
                placeholder="Type a breaking claim, rumor, or news snippet..."
                className="flex-1 rounded-2xl border border-white/30 bg-[#0a2332]/80 px-6 py-4 text-sm text-[#dcf1fb] outline-none ring-[#73d6ff] transition focus:ring-2 focus:border-white/50 backdrop-blur-sm placeholder:text-[#7aa2f7]"
              />
              <motion.button
                type="button"
                onClick={handleAnalyze}
                disabled={isAnalyzing || query.trim().length < 4}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="rounded-2xl border-2 border-[#73d6ff]/80 bg-gradient-to-r from-[#73d6ff]/30 to-[#7dd7ff]/20 px-8 py-4 text-sm font-bold text-[#e8f5ff] transition-all duration-300 hover:border-[#73d6ff] hover:from-[#73d6ff]/40 hover:to-[#7dd7ff]/30 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-[#73d6ff]/10"
              >
                {isAnalyzing ? (
                  <span className="flex items-center gap-2">
                    <span className="animate-spin">⚡</span> Analyzing...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <span>🔍</span> Analyze Live
                  </span>
                )}
              </motion.button>
            </div>

            <p className="mt-4 text-sm text-[#96c9df]">
              ✓ Live data integration • ✓ 1M+ page coverage • ✓ 3-layer analysis • ✓ Real-time results
            </p>

            {error ? (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-3 text-sm text-[#ff9e9e] bg-[#3a1f18]/50 border border-[#ff7d47]/30 rounded-lg p-3"
              >
                ⚠ {error}
              </motion.p>
            ) : null}
          </motion.div>
        </section>

        <FeatureShowcase />

        <section id="about" className="relative mx-auto w-full max-w-7xl px-6 pb-20 pt-20">
          {/* Background gradient */}
          <div className="absolute inset-0 -z-10 opacity-40">
            <div className="absolute bottom-0 left-0 h-96 w-96 rounded-full bg-[#7df5c5]/20 blur-3xl" />
            <div className="absolute top-0 right-0 h-80 w-80 rounded-full bg-[#ffc96f]/10 blur-3xl" />
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.7 }}
            className="rounded-3xl border border-white/20 bg-gradient-to-br from-white/12 via-white/6 to-white/4 p-10 backdrop-blur-2xl shadow-2xl"
          >
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-1 h-8 bg-gradient-to-b from-[#7df5c5] to-[#73d6ff] rounded-full" />
                  <p className="text-xs uppercase tracking-[0.3em] font-bold text-[#7df5c5]">About VeriGraph</p>
                </div>

                <h3 className="text-3xl lg:text-4xl font-bold text-white leading-tight">
                  Built for <span className="bg-gradient-to-r from-[#9be2ff] to-[#7df5c5] bg-clip-text text-transparent">trust</span> in realtime information ecosystems
                </h3>

                <p className="mt-6 text-base text-[#d0e4f0] leading-relaxed max-w-2xl">
                  VeriGraph combines <span className="text-[#9be2ff] font-semibold">language analysis</span>, 
                  <span className="text-[#7df5c5] font-semibold"> network coordination mapping</span>, and 
                  <span className="text-[#ffc96f] font-semibold"> fact validation</span> into one intelligence surface.
                </p>

                <p className="mt-4 text-base text-[#b8d4e1] leading-relaxed max-w-2xl">
                  Instead of a single confidence score, it reveals how misinformation propagates across synchronized accounts so investigators, journalists, and public safety teams can act quickly.
                </p>

                <div className="mt-8 flex gap-4">
                  <motion.a
                    href="/analysis"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="inline-flex rounded-full border border-[#7df5c5]/60 bg-[#7df5c5]/15 px-6 py-3 text-sm font-bold text-[#7df5c5] transition-all duration-300 hover:bg-[#7df5c5]/25 hover:border-[#7df5c5]"
                  >
                    Try Dashboard ↗
                  </motion.a>
                </div>
              </div>

              {/* Feature Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { icon: "🧠", title: "NLP Analysis", desc: "Semantic threat signals" },
                  { icon: "🔗", title: "Network Graph", desc: "Coordination detection" },
                  { icon: "✓", title: "Fact Check", desc: "Truth assessment" },
                  { icon: "📊", title: "Live Feed", desc: "Real-time updates" },
                ].map((feature, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.1 }}
                    className="rounded-xl border border-white/15 bg-white/8 p-4 backdrop-blur hover:bg-white/12 transition-all duration-300 group"
                  >
                    <div className="text-2xl mb-2">{feature.icon}</div>
                    <h4 className="font-bold text-white text-sm group-hover:text-[#9be2ff] transition-colors">{feature.title}</h4>
                    <p className="text-xs text-[#96c9df] mt-1">{feature.desc}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </section>
      </main>
      <Footer />
    </div>
  );
}
