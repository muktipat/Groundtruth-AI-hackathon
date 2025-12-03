"use client"

import { Button } from "@/components/ui/button"
import { ArrowRight, Zap, Shield, MapPin, CheckCircle, Sparkles } from "lucide-react"
import { useState } from "react"

interface LandingPageProps {
  mode: "tooling" | "rag"
  setMode: (mode: "tooling" | "rag") => void
  onStartChat: () => void
}

export default function LandingPage({ mode, setMode, onStartChat }: LandingPageProps) {
  const [showLocationPrompt, setShowLocationPrompt] = useState(false)

  const handleStartChat = () => {
    setShowLocationPrompt(true)
    // Request location access
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        () => {
          onStartChat()
        },
        () => {
          // User denied or error, still proceed with chat
          onStartChat()
        },
      )
    } else {
      onStartChat()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-white text-slate-900">
      {/* Top Banner */}
      <div className="bg-teal-500 text-white text-center py-3 px-4">
        <p className="text-sm font-medium">AuraCX Recognized for Best Context-Aware Customer Support in 2025</p>
      </div>

      {/* Navigation */}
      <nav className="flex items-center justify-between px-8 py-5 border-b border-slate-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center text-white font-bold text-lg">
            A
          </div>
          <span className="text-2xl font-bold bg-gradient-to-r from-teal-600 to-teal-700 bg-clip-text text-transparent">
            AuraCX
          </span>
        </div>
        <div className="flex items-center gap-8">
          <a href="#" className="text-sm font-medium text-slate-600 hover:text-teal-600 transition">
            How It Works
          </a>
          <a href="#" className="text-sm font-medium text-slate-600 hover:text-teal-600 transition">
            Examples
          </a>
          <a href="#" className="text-sm font-medium text-slate-600 hover:text-teal-600 transition">
            Docs
          </a>
          <Button variant="outline" size="sm" className="rounded-full text-slate-700 border-slate-300 bg-transparent">
            Sign In
          </Button>
          <Button size="sm" className="rounded-full bg-teal-500 hover:bg-teal-600 text-white">
            Get Started
          </Button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-8 py-24 max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-6">
              <h1 className="text-6xl md:text-7xl font-bold text-balance leading-tight text-slate-900">
                Instant, <span className="text-teal-600">context-aware</span> retail support
              </h1>
              <p className="text-xl text-slate-600 max-w-lg leading-relaxed">
                Switch between fast Tooling Mode and context-rich RAG Mode. Voice or text. Real customer intelligence at
                scale.
              </p>
            </div>

            {/* Mode Toggle */}
            <div className="flex flex-col gap-6">
              <div className="inline-flex items-center gap-2 bg-white border-2 border-teal-200 p-1 rounded-full w-fit shadow-md">
                <button
                  onClick={() => setMode("tooling")}
                  className={`px-6 py-3 rounded-full text-sm font-semibold transition-all ${
                    mode === "tooling" ? "bg-teal-500 text-white shadow-lg" : "text-slate-700 hover:bg-slate-50"
                  }`}
                >
                  <span className="flex items-center gap-2">
                    <Zap className="w-4 h-4" />
                    Tooling Mode
                  </span>
                </button>
                <button
                  onClick={() => setMode("rag")}
                  className={`px-6 py-3 rounded-full text-sm font-semibold transition-all ${
                    mode === "rag" ? "bg-teal-600 text-white shadow-lg" : "text-slate-700 hover:bg-slate-50"
                  }`}
                >
                  <span className="flex items-center gap-2">
                    <Shield className="w-4 h-4" />
                    RAG Mode
                  </span>
                </button>
              </div>

              {/* Mode Description */}
              <div className="text-sm text-slate-700 bg-slate-50 p-4 rounded-lg border border-slate-200">
                <p className="font-semibold text-teal-700 mb-2">
                  {mode === "tooling" ? "⚡ Tooling Mode" : "🔍 RAG Mode"}
                </p>
                <p>
                  {mode === "tooling"
                    ? "Fast, deterministic responses using APIs and databases. Zero hallucinations, instant answers about store hours, inventory, and orders."
                    : "Context-rich generation using your documents. Evidence-based answers with source verification and personalized insights."}
                </p>
              </div>
            </div>

            {/* CTAs */}
            <div className="flex gap-4 pt-4">
              <Button
                size="lg"
                className="rounded-full gap-2 bg-teal-500 hover:bg-teal-600 text-white font-semibold"
                onClick={handleStartChat}
              >
                Try Demo Chat <ArrowRight className="w-5 h-5" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="rounded-full bg-white border-2 border-slate-300 text-slate-700 hover:bg-slate-50 font-semibold"
              >
                Learn How It Works
              </Button>
            </div>
          </div>

          {/* Right Visual - Feature Diagram */}
          <div className="relative">
            <div className="bg-gradient-to-br from-teal-100 to-cyan-50 rounded-2xl border-2 border-teal-200 p-8 shadow-xl">
              <div className="space-y-8">
                {/* Tooling Mode Features */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2 mb-4">
                    <Zap className="w-5 h-5 text-teal-600" />
                    <h3 className="font-bold text-slate-900 text-sm">Tooling Mode</h3>
                  </div>
                  <div className="space-y-2">
                    {["Store Hours & Availability", "Real-time Inventory", "Order Tracking", "Personalized Offers"].map(
                      (feature, i) => (
                        <div key={i} className="flex items-center gap-3 text-sm text-slate-700">
                          <CheckCircle className="w-4 h-4 text-teal-600 flex-shrink-0" />
                          <span>{feature}</span>
                        </div>
                      ),
                    )}
                  </div>
                </div>

                <div className="border-t border-teal-200" />

                {/* RAG Mode Features */}
                <div className="space-y-3">
                  <div className="flex items-center gap-2 mb-4">
                    <Shield className="w-5 h-5 text-teal-700" />
                    <h3 className="font-bold text-slate-900 text-sm">RAG Mode</h3>
                  </div>
                  <div className="space-y-2">
                    {["Document Retrieval", "Context Compression", "Evidence-Based Answers", "Source Verification"].map(
                      (feature, i) => (
                        <div key={i} className="flex items-center gap-3 text-sm text-slate-700">
                          <CheckCircle className="w-4 h-4 text-teal-700 flex-shrink-0" />
                          <span>{feature}</span>
                        </div>
                      ),
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-8 py-20 bg-slate-50 border-t border-slate-200">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-slate-900 mb-4">Built for Retail Excellence</h2>
          <p className="text-lg text-slate-600 mb-16">
            Power your customer support with AI that understands context, location, and history.
          </p>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Sparkles,
                title: "Agentic Architecture",
                description:
                  "Specialized agents for store hours, inventory, orders, and emotions with real-time orchestration",
              },
              {
                icon: Shield,
                title: "Zero-PII Gateway",
                description:
                  "Evidence-checked answers with automatic data masking. No raw customer data sent to external LLMs.",
              },
              {
                icon: MapPin,
                title: "Location Intelligence",
                description:
                  "Real-time GPS context, nearby stores, competitor proximity, and location-triggered offers.",
              },
            ].map((feature, i) => (
              <div
                key={i}
                className="bg-white p-8 rounded-xl border border-slate-200 hover:border-teal-300 hover:shadow-lg transition group"
              >
                <feature.icon className="w-8 h-8 text-teal-600 mb-4 group-hover:scale-110 transition" />
                <h3 className="font-bold text-lg text-slate-900 mb-3">{feature.title}</h3>
                <p className="text-slate-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Footer */}
      <section className="px-8 py-16 bg-gradient-to-r from-teal-600 to-teal-700 text-white">
        <div className="max-w-7xl mx-auto text-center space-y-6">
          <h2 className="text-3xl font-bold">Ready to transform customer support?</h2>
          <p className="text-lg text-teal-50 max-w-2xl mx-auto">
            Try AuraCX demo now and see how context-aware AI can answer customer questions instantly.
          </p>
          <Button
            size="lg"
            className="rounded-full bg-white text-teal-700 hover:bg-slate-100 font-semibold gap-2"
            onClick={handleStartChat}
          >
            Launch Demo Chat <ArrowRight className="w-5 h-5" />
          </Button>
        </div>
      </section>
    </div>
  )
}
