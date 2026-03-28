"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export function Navbar() {
  return (
    <motion.header
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="sticky top-0 z-50 border-b border-white/20 bg-[#04121b]/60 backdrop-blur-xl"
    >
      <nav className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-xl font-semibold tracking-tight text-[#f2f7f9]">
          VeriGraph AI
        </Link>
        <div className="flex items-center gap-6 text-sm text-[#d8e7ef]">
          <a href="#features" className="transition hover:text-white">
            Features
          </a>
          <a href="#about" className="transition hover:text-white">
            About
          </a>
          <Link
            href="/analysis"
            className="rounded-full border border-[#8ad7ff]/50 px-4 py-2 font-medium transition hover:border-[#8ad7ff] hover:bg-[#8ad7ff]/20"
          >
            Dashboard
          </Link>
        </div>
      </nav>
    </motion.header>
  );
}
