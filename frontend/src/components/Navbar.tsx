"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";

interface NavItem {
  name: string;
  href: string;
  isAnchor?: boolean;
  anchorId?: string;
  badge?: string;
}

const navItems: NavItem[] = [
  { name: "Home", href: "/", isAnchor: true, anchorId: "hero" },
  { name: "Scanner", href: "/#scanner", isAnchor: true, anchorId: "scanner" },
  { name: "Features", href: "/#features", isAnchor: true, anchorId: "features" },
  { name: "Spread Radar", href: "/propagation-demo" },
  { name: "History", href: "/history" },
  { name: "About", href: "/#about", isAnchor: true, anchorId: "about" },
];

export function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Handle smooth scroll when clicking anchor links on the homepage
  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, item: NavItem) => {
    if (item.isAnchor && pathname === "/") {
      e.preventDefault();
      setMobileMenuOpen(false);

      if (item.anchorId === "hero") {
        window.scrollTo({ top: 0, behavior: "smooth" });
        window.history.pushState(null, "", "/");
        return;
      }

      const target = document.getElementById(item.anchorId || "");
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
        window.history.pushState(null, "", `#${item.anchorId}`);
      }
    } else {
      setMobileMenuOpen(false);
    }
  };

  const isItemActive = (item: NavItem) => {
    if (item.href === "/propagation-demo" && pathname === "/propagation-demo") {
      return true;
    }
    if (item.href === "/history" && pathname === "/history") {
      return true;
    }
    if (item.href === "/" && pathname === "/" && item.anchorId === "hero") {
      return true;
    }
    return false;
  };

  const isDashboardActive = pathname === "/analysis";

  return (
    <motion.header
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className={`sticky top-0 z-50 transition-all duration-300 ${
        scrolled
          ? "border-b border-[#73d6ff]/20 bg-[#031019]/90 shadow-lg shadow-black/40 backdrop-blur-2xl"
          : "border-b border-white/10 bg-[#04121b]/70 backdrop-blur-xl"
      }`}
    >
      <nav className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-3.5 sm:px-6">
        {/* Brand Logo */}
        <Link
          href="/"
          className="group flex items-center gap-3 transition-opacity hover:opacity-90"
          onClick={() => {
            if (pathname === "/") {
              window.scrollTo({ top: 0, behavior: "smooth" });
            }
          }}
        >
          {/* Glowing Animated Radar Icon */}
          <div className="relative flex h-9 w-9 items-center justify-center rounded-xl border border-[#73d6ff]/50 bg-gradient-to-br from-[#73d6ff]/20 via-[#0a2738] to-[#7df5c5]/20 shadow-md shadow-[#73d6ff]/20 group-hover:border-[#73d6ff]">
            <svg
              className="h-5 w-5 text-[#73d6ff] transition-transform duration-300 group-hover:scale-110"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="2" />
              <path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14" />
            </svg>
            <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#7df5c5] opacity-75" />
              <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-[#7df5c5]" />
            </span>
          </div>

          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-tight text-white group-hover:text-[#e8f5ff]">
              VeriGraph <span className="bg-gradient-to-r from-[#73d6ff] to-[#7df5c5] bg-clip-text text-transparent">AI</span>
            </span>
            <span className="hidden text-[10px] uppercase tracking-widest text-[#8fd2f1] sm:block">
              Misinformation Radar
            </span>
          </div>
        </Link>

        {/* Live Engine Status Badge (Desktop) */}
        <div className="hidden items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-950/30 px-3 py-1 text-xs text-emerald-400 lg:flex">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="font-medium tracking-wide">Radar Online</span>
        </div>

        {/* Desktop Navigation Links */}
        <div className="hidden items-center gap-1 md:flex lg:gap-2">
          {navItems.map((item) => {
            const active = isItemActive(item);
            return (
              <Link
                key={item.name}
                href={item.href}
                onClick={(e) => handleNavClick(e, item)}
                className={`relative rounded-lg px-3.5 py-2 text-sm font-medium transition-all duration-200 ${
                  active
                    ? "text-[#73d6ff] bg-[#73d6ff]/10"
                    : "text-[#cce2ed] hover:bg-white/5 hover:text-white"
                }`}
              >
                {item.name}
                {item.badge && (
                  <span className="ml-1.5 rounded-full bg-[#73d6ff]/20 px-1.5 py-0.5 text-[10px] font-semibold text-[#73d6ff]">
                    {item.badge}
                  </span>
                )}
                {active && (
                  <motion.div
                    layoutId="activeNavIndicator"
                    className="absolute inset-x-2 -bottom-1 h-0.5 rounded-full bg-gradient-to-r from-[#73d6ff] to-[#7df5c5]"
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
              </Link>
            );
          })}
        </div>

        {/* Action Button: Dashboard CTA */}
        <div className="hidden items-center gap-3 sm:flex">
          <Link
            href="/analysis"
            className={`group relative flex items-center gap-2 overflow-hidden rounded-full px-5 py-2 text-sm font-semibold transition-all duration-300 ${
              isDashboardActive
                ? "border-2 border-[#73d6ff] bg-gradient-to-r from-[#73d6ff]/30 to-[#7df5c5]/20 text-white shadow-lg shadow-[#73d6ff]/25"
                : "border border-[#8ad7ff]/50 bg-gradient-to-r from-[#73d6ff]/15 to-[#7df5c5]/10 text-[#dcf1fb] hover:border-[#73d6ff] hover:bg-[#73d6ff]/25 hover:text-white hover:shadow-lg hover:shadow-[#73d6ff]/20"
            }`}
          >
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#73d6ff] opacity-75" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-[#73d6ff]" />
            </span>
            <span>Dashboard</span>
            <svg
              className="h-3.5 w-3.5 transition-transform duration-300 group-hover:translate-x-0.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>

        {/* Mobile Hamburger Button */}
        <button
          type="button"
          aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
          aria-expanded={mobileMenuOpen}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/15 bg-white/5 text-[#dcf1fb] transition hover:bg-white/10 md:hidden"
        >
          {mobileMenuOpen ? (
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </nav>

      {/* Mobile Drawer Navigation */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden border-b border-white/15 bg-[#031019]/95 px-6 pb-6 pt-2 backdrop-blur-2xl md:hidden"
          >
            <div className="flex flex-col gap-2">
              {navItems.map((item) => {
                const active = isItemActive(item);
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={(e) => handleNavClick(e, item)}
                    className={`flex items-center justify-between rounded-xl px-4 py-3 text-base font-medium transition ${
                      active
                        ? "bg-[#73d6ff]/15 text-[#73d6ff] border border-[#73d6ff]/30"
                        : "text-[#d0e4f0] hover:bg-white/5 hover:text-white"
                    }`}
                  >
                    <span>{item.name}</span>
                    <svg className="h-4 w-4 opacity-60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                );
              })}

              {/* Mobile Dashboard Button */}
              <div className="mt-3 pt-3 border-t border-white/10">
                <Link
                  href="/analysis"
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex w-full items-center justify-center gap-2 rounded-xl py-3.5 text-center text-sm font-bold transition ${
                    isDashboardActive
                      ? "border-2 border-[#73d6ff] bg-[#73d6ff]/25 text-white"
                      : "border border-[#73d6ff]/60 bg-gradient-to-r from-[#73d6ff]/20 to-[#7df5c5]/20 text-white hover:bg-[#73d6ff]/30"
                  }`}
                >
                  <span className="h-2 w-2 rounded-full bg-[#7df5c5] animate-ping" />
                  <span>Open Intelligence Dashboard</span>
                </Link>
              </div>

              {/* Status Indicator (Mobile) */}
              <div className="mt-2 flex items-center justify-center gap-2 py-2 text-xs text-emerald-400">
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                <span>Real-time Multi-Stream Radar Active</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  );
}
