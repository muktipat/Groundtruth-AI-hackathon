"use client"

import { Card } from "@/components/ui/card"
import { CheckCircle, Clock, AlertCircle, Zap, Shield, MapPin, Lock } from "lucide-react"
import type { Agent, AgentStatus } from "@/types"

interface AgentActivityPanelProps {
  agents: Agent[]
  currentThinkingStep: string
  isProcessing: boolean
  mode: "tooling" | "rag"
  userLocation?: { lat: number; lng: number } | null
}

const getStatusIcon = (status: AgentStatus) => {
  switch (status) {
    case "done":
      return <CheckCircle className="w-4 h-4 text-green-600" />
    case "running":
      return <div className="w-4 h-4 rounded-full bg-teal-600 animate-pulse" />
    case "queued":
      return <Clock className="w-4 h-4 text-slate-400" />
    case "failed":
      return <AlertCircle className="w-4 h-4 text-red-600" />
  }
}

export default function AgentActivityPanel({
  agents,
  currentThinkingStep,
  isProcessing,
  mode,
  userLocation,
}: AgentActivityPanelProps) {
  return (
    <div className="w-96 flex flex-col gap-4">
      {/* Thinking Trace */}
      {isProcessing && (
        <Card className="p-4 bg-gradient-to-br from-teal-50 to-cyan-50 border-2 border-teal-200">
          <h3 className="text-xs font-bold text-slate-900 mb-4 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-teal-600 animate-pulse" />
            Agent Thinking Process
          </h3>
          <div className="space-y-3">
            <div className="text-sm text-slate-700 font-medium">{currentThinkingStep || "Initializing agents..."}</div>
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <div className="flex gap-1">
                <div className="w-1.5 h-1.5 rounded-full bg-teal-600 animate-bounce" />
                <div className="w-1.5 h-1.5 rounded-full bg-teal-600 animate-bounce delay-100" />
                <div className="w-1.5 h-1.5 rounded-full bg-teal-600 animate-bounce delay-200" />
              </div>
              Processing...
            </div>
          </div>
        </Card>
      )}

      {/* Agent List */}
      <Card className="p-4 bg-white border-2 border-slate-200 flex-1 overflow-y-auto">
        <h3 className="text-xs font-bold text-slate-900 mb-3 flex items-center gap-2">
          <span className="flex items-center justify-center w-5 h-5 rounded bg-teal-100 text-teal-700 text-xs font-bold">
            {agents.length}
          </span>
          Active Agents
        </h3>

        {agents.length === 0 ? (
          <div className="text-xs text-slate-500 text-center py-6">Agents will appear here when processing a query</div>
        ) : (
          <div className="space-y-2">
            {agents.map((agent, i) => (
              <div
                key={`${agent.name}-${i}`}
                className="text-xs p-3 rounded-lg border border-slate-200 bg-slate-50 hover:bg-white hover:border-teal-300 transition"
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-start gap-2 flex-1">
                    <div className="mt-0.5">{getStatusIcon(agent.status)}</div>
                    <div className="flex-1 min-w-0">
                      <p className="font-bold text-slate-900">{agent.name}</p>
                      <p className="text-slate-500 text-xs">{agent.role}</p>
                    </div>
                  </div>
                  {agent.confidence > 0 && (
                    <div className="text-right flex-shrink-0">
                      <div className="text-xs font-bold text-teal-700">{(agent.confidence * 100).toFixed(0)}%</div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Mode Info */}
      <Card
        className={`p-4 border-2 ${
          mode === "tooling"
            ? "bg-teal-50 border-teal-200"
            : "bg-gradient-to-br from-teal-900 to-teal-800 text-white border-teal-700"
        }`}
      >
        <div className="flex items-center gap-2 mb-2">
          {mode === "tooling" ? <Zap className="w-4 h-4 text-teal-600" /> : <Shield className="w-4 h-4 text-white" />}
          <span className={`text-xs font-bold ${mode === "tooling" ? "text-teal-900" : "text-white"}`}>
            {mode === "tooling" ? "⚡ Tooling Mode" : "🔍 RAG Mode"}
          </span>
        </div>
        <p className={`text-xs leading-relaxed ${mode === "tooling" ? "text-slate-700" : "text-teal-50"}`}>
          {mode === "tooling"
            ? "Fast, deterministic responses using APIs and databases. Zero hallucinations."
            : "Evidence-based generation using document retrieval and source verification."}
        </p>
      </Card>

      {/* Location Info */}
      {userLocation && (
        <Card className="p-4 bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200">
          <div className="flex items-center gap-2 mb-2">
            <MapPin className="w-4 h-4 text-blue-600" />
            <span className="text-xs font-bold text-blue-900">Location Enabled</span>
          </div>
          <p className="text-xs text-blue-700 font-mono">
            {userLocation.lat.toFixed(4)}, {userLocation.lng.toFixed(4)}
          </p>
        </Card>
      )}

      {/* Privacy Notice */}
      <div className="text-xs text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-200 flex gap-2">
        <Lock className="w-4 h-4 flex-shrink-0 text-slate-500 mt-0.5" />
        <div>
          <p className="font-semibold text-slate-900 mb-1">Data Protection</p>
          <p>PII masked. Location used only for proximity. No external LLM access to raw data.</p>
        </div>
      </div>
    </div>
  )
}
