export function Footer() {
  return (
    <footer className="relative border-t border-white/15 bg-gradient-to-b from-[#031019] to-[#0a1a26] px-6 py-16">
      {/* Background gradient */}
      <div className="absolute inset-0 -z-10 opacity-30">
        <div className="absolute bottom-0 right-0 h-64 w-64 rounded-full bg-[#73d6ff]/10 blur-3xl" />
      </div>

      <div className="mx-auto max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          {/* Brand */}
          <div>
            <h3 className="text-xl font-bold text-[#e8f5ff] mb-4">VeriGraph AI</h3>
            <p className="text-sm text-[#96c9df] leading-relaxed">
              Real-time coordinated misinformation detection powered by hybrid intelligence.
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-[#b8d4e1]">
              <li><a href="#features" className="hover:text-[#9be2ff] transition-colors">Features</a></li>
              <li><a href="/analysis" className="hover:text-[#9be2ff] transition-colors">Dashboard</a></li>
              <li><a href="#" className="hover:text-[#9be2ff] transition-colors">Documentation</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">Contact</h4>
            <p className="text-sm text-[#b8d4e1] mb-3">
              <a href="mailto:info@verigraph.ai" className="hover:text-[#9be2ff] transition-colors">info@verigraph.ai</a>
            </p>
            <div className="flex gap-3">
              <a href="#" className="w-8 h-8 rounded-lg bg-white/10 hover:bg-[#73d6ff]/30 flex items-center justify-center text-[#73d6ff] transition-all duration-300">
                𝕏
              </a>
              <a href="#" className="w-8 h-8 rounded-lg bg-white/10 hover:bg-[#73d6ff]/30 flex items-center justify-center text-[#73d6ff] transition-all duration-300">
                📱
              </a>
            </div>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-white/10 pt-8">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-sm text-[#8fb9cd]">
              © 2026 VeriGraph AI. All rights reserved.
            </p>
            <div className="flex gap-6 text-sm text-[#8fb9cd]">
              <a href="#" className="hover:text-[#9be2ff] transition-colors">Privacy</a>
              <a href="#" className="hover:text-[#9be2ff] transition-colors">Terms</a>
              <a href="#" className="hover:text-[#9be2ff] transition-colors">Security</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
