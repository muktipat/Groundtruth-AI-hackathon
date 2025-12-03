"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Mic, Send, ArrowLeft, Zap, Shield, Volume2, MapPin } from "lucide-react"
import AgentActivityPanel from "./agent-activity-panel"
import ResponseCard from "./response-card"
import { sendChatMessage, healthCheck } from "@/lib/api-client"
import type { Message, Agent } from "@/types"
import type { ChatResponse } from "@/lib/api-client"

interface ChatInterfaceProps {
  initialMode: "tooling" | "rag"
  onModeChange: (mode: "tooling" | "rag") => void
  onBack: () => void
}

const DEMO_SCENARIOS = [
  {
    title: "I'm cold",
    description: "Vague emotional need → context-aware solution",
    mode: "rag" as const,
    query: "I'm cold",
    expectedMode: "RAG",
  },
  {
    title: "Do you have size 10?",
    description: "Direct stock availability check",
    mode: "tooling" as const,
    query: "Do you have size 10 sneakers in stock?",
    expectedMode: "Tooling",
  },
  {
    title: "Is this store open?",
    description: "Store hours and current status",
    mode: "tooling" as const,
    query: "Is the Target store open right now?",
    expectedMode: "Tooling",
  },
  {
    title: "Where is my order?",
    description: "Order tracking with ETA",
    mode: "tooling" as const,
    query: "Where is my order #4471?",
    expectedMode: "Tooling",
  },
  {
    title: "Where's the closest store?",
    description: "Location-based store lookup",
    mode: "tooling" as const,
    query: "Where's the closest Starbucks?",
    expectedMode: "Tooling",
  },
  {
    title: "Recommend something warm",
    description: "Weather-aware RAG with personalization",
    mode: "rag" as const,
    query: "I want something warm but not too heavy",
    expectedMode: "RAG",
  },
]

const DEMO_RESPONSES: Record<
  string,
  { text: string; confidence: number; provenance: string[]; actions: Array<{ label: string; type: string }> }
> = {
  "I'm cold": {
    text: "The Starbucks 62m away is open and has hot beverages. Because it's 2°C outside, your 10% Hot Cocoa coupon is active. Want directions?",
    confidence: 0.92,
    provenance: ["menu_starbucks.pdf", "promo_sheet_q4.pdf", "weather_api"],
    actions: [
      { label: "Open Map", type: "map" },
      { label: "Apply Coupon", type: "coupon" },
      { label: "More Info", type: "more" },
    ],
  },
  "Do you have size 10 sneakers in stock?": {
    text: "Yes, size 10 is available at the Midtown store with 3 units left. VIP members get priority reservation. Want to reserve one?",
    confidence: 0.98,
    provenance: ["inventory_api", "midtown_store_db"],
    actions: [
      { label: "Reserve Item", type: "reserve" },
      { label: "Map to Store", type: "map" },
    ],
  },
  "Is the Target store open right now?": {
    text: "Target at Midtown is open until 10 PM (closes in 2 hours). It's 420 meters from you. Footfall is currently moderate.",
    confidence: 0.99,
    provenance: ["store_hours_db", "location_service"],
    actions: [
      { label: "Get Directions", type: "map" },
      { label: "Call Store", type: "escalate" },
    ],
  },
  "Where is my order #4471?": {
    text: "Order #4471 is out for delivery. Estimated arrival in 14 minutes. Your driver is 2.3km away. You'll get a notification when they're nearby.",
    confidence: 0.97,
    provenance: ["order_status_api", "tracking_service"],
    actions: [
      { label: "Track Live", type: "map" },
      { label: "Contact Driver", type: "escalate" },
    ],
  },
  "Where's the closest Starbucks?": {
    text: "Starbucks is 62 meters away and currently open. They're offering a 20% promotion on cold drinks today. Want a map link?",
    confidence: 0.95,
    provenance: ["location_service", "store_hours_db", "offers_api"],
    actions: [
      { label: "Open Map", type: "map" },
      { label: "See Menu", type: "more" },
    ],
  },
  "I want something warm but not too heavy": {
    text: "The weather is cold, you're near Starbucks, and based on your taste history, a light Matcha Tea with 10% discount fits perfectly. Available now.",
    confidence: 0.88,
    provenance: ["beverage_menu.json", "user_preferences.pdf", "weather_api"],
    actions: [
      { label: "View Items", type: "more" },
      { label: "Reserve", type: "reserve" },
      { label: "Add to Cart", type: "coupon" },
    ],
  },
}

export default function ChatInterface({ initialMode, onModeChange, onBack }: ChatInterfaceProps) {
  const [mode, setMode] = useState<"tooling" | "rag">(initialMode)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [activeAgents, setActiveAgents] = useState<Agent[]>([])
  const [currentThinkingStep, setCurrentThinkingStep] = useState<string>("")
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null)
  const [backendError, setBackendError] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Check backend health on mount
    healthCheck()
      .then(() => setBackendError(null))
      .catch((err) => {
        console.error("Backend health check failed:", err)
        setBackendError("Backend unavailable - running in demo mode")
      })

    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition((position) => {
        setUserLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        })
      })
    }
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleModeToggle = () => {
    const newMode = mode === "tooling" ? "rag" : "tooling"
    setMode(newMode)
    onModeChange(newMode)
  }

  const convertBackendAgentsToUIAgents = (backendExecution?: any[]): Agent[] => {
    if (!backendExecution) {
      // Fallback to default agents
      return mode === "tooling"
        ? [
            { name: "PII Masker", role: "Data Protection", status: "completed", confidence: 0.98 },
            { name: "Intent Detector", role: "Understanding Query", status: "completed", confidence: 0.95 },
            { name: "Location Context", role: "GPS & Proximity", status: "completed", confidence: 0.9 },
            { name: "Stock Lookup", role: "Inventory Check", status: "completed", confidence: 0.88 },
            { name: "Synthesizer", role: "Response Generation", status: "completed", confidence: 0.92 },
          ]
        : [
            { name: "PII Masker", role: "Data Protection", status: "completed", confidence: 0.98 },
            { name: "Intent Detector", role: "Understanding Query", status: "completed", confidence: 0.95 },
            { name: "Query Rewriter", role: "Query Expansion", status: "completed", confidence: 0.9 },
            { name: "Retriever", role: "Document Search", status: "completed", confidence: 0.92 },
            { name: "Reranker", role: "Relevance Scoring", status: "completed", confidence: 0.88 },
            { name: "Context Compressor", role: "Summarization", status: "completed", confidence: 0.87 },
            { name: "RAG Generator", role: "Evidence-Based Gen", status: "completed", confidence: 0.91 },
            { name: "Synthesizer", role: "Final Response", status: "completed", confidence: 0.93 },
          ]
    }

    return backendExecution.map((agent) => ({
      name: agent.agent_name || "Unknown",
      role: agent.role || "Processing",
      status: agent.status === "completed" ? "completed" : agent.status === "running" ? "running" : "queued",
      confidence: agent.confidence || 0,
    }))
  }

  const sendMessageToBackend = async (query: string): Promise<ChatResponse | null> => {
    try {
      const response = await sendChatMessage({
        message: query,
        customer_id: `user_${Date.now()}`,
        location: userLocation || undefined,
      })
      return response
    } catch (error) {
      console.error("Backend error:", error)
      setBackendError(`Error: ${error instanceof Error ? error.message : "Unknown error"}`)
      return null
    }
  }

  const simulateAgentExecution = async (query: string) => {
    setIsProcessing(true)
    setBackendError(null)

    // Try to use real backend
    const backendResponse = await sendMessageToBackend(query)

    if (backendResponse) {
      // Use real backend response
      const agents = convertBackendAgentsToUIAgents(backendResponse.agent_execution)
      setActiveAgents(agents)

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          type: "user",
          content: query,
          timestamp: new Date(),
        },
        {
          id: (Date.now() + 1).toString(),
          type: "assistant",
          content: backendResponse.response,
          confidence: backendResponse.confidence,
          provenance: backendResponse.sources || [],
          actions: (backendResponse.recommended_actions || []).map((action) => ({
            label: action,
            type: "action",
          })),
          mode: backendResponse.mode,
          timestamp: new Date(),
        },
      ])
    } else {
      // Fallback to demo mode
      const toolingAgents: Agent[] = [
        { name: "PII Masker", role: "Data Protection", status: "running", confidence: 0.98 },
        { name: "Intent Detector", role: "Understanding Query", status: "queued", confidence: 0 },
        { name: "Location Context", role: "GPS & Proximity", status: "queued", confidence: 0 },
        { name: "Stock Lookup", role: "Inventory Check", status: "queued", confidence: 0 },
        { name: "Synthesizer", role: "Response Generation", status: "queued", confidence: 0 },
      ]

      const ragAgents: Agent[] = [
        { name: "PII Masker", role: "Data Protection", status: "running", confidence: 0.98 },
        { name: "Intent Detector", role: "Understanding Query", status: "queued", confidence: 0 },
        { name: "Query Rewriter", role: "Query Expansion", status: "queued", confidence: 0 },
        { name: "Retriever", role: "Document Search", status: "queued", confidence: 0 },
        { name: "Reranker", role: "Relevance Scoring", status: "queued", confidence: 0 },
        { name: "Context Compressor", role: "Summarization", status: "queued", confidence: 0 },
        { name: "RAG Generator", role: "Evidence-Based Gen", status: "queued", confidence: 0 },
        { name: "Synthesizer", role: "Final Response", status: "queued", confidence: 0 },
      ]

      const agents = mode === "tooling" ? toolingAgents : ragAgents

      // Simulate agent progression
      for (let i = 0; i < agents.length; i++) {
        await new Promise((resolve) => setTimeout(resolve, 500))
        setActiveAgents(agents.slice(0, i + 1))
        if (i < agents.length - 1) {
          setCurrentThinkingStep(`Running ${agents[i].name}...`)
        }
      }

      await new Promise((resolve) => setTimeout(resolve, 600))
      setCurrentThinkingStep("Synthesizing response...")

      // Get demo response
      const demoResponse = DEMO_RESPONSES[query] || {
        text: "Based on your query and current context, here's what I found. Would you like more information?",
        confidence: 0.75,
        provenance: mode === "tooling" ? ["api_service"] : ["knowledge_base.pdf"],
        actions: [
          { label: "Learn More", type: "more" },
          { label: "Help", type: "escalate" },
        ],
      }

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          type: "user",
          content: query,
          timestamp: new Date(),
        },
        {
          id: (Date.now() + 1).toString(),
          type: "assistant",
          content: demoResponse.text,
          confidence: demoResponse.confidence,
          provenance: demoResponse.provenance,
          actions: demoResponse.actions,
          mode: mode,
          timestamp: new Date(),
        },
      ])
    }

    setIsProcessing(false)
    setActiveAgents([])
    setCurrentThinkingStep("")
  }

  const handleSendMessage = async () => {
    if (!input.trim()) return
    const query = input
    setInput("")
    await simulateAgentExecution(query)
  }

  const handleDemoScenario = async (scenario: (typeof DEMO_SCENARIOS)[0]) => {
    setMode(scenario.mode)
    onModeChange(scenario.mode)
    await simulateAgentExecution(scenario.query)
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-slate-50 to-slate-100 text-slate-900">
      {/* Header */}
      <div className="border-b border-slate-200 px-8 py-4 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={onBack}
              className="rounded-full text-slate-700 hover:bg-slate-100"
            >
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="font-bold text-xl text-slate-900">AuraCX Demo Chat</h1>
              <p className="text-xs text-slate-500 flex items-center gap-1">
                <span className={`w-2 h-2 rounded-full ${backendError ? "bg-red-500" : "bg-teal-500"}`} />
                {backendError ? "⚠️ Demo Mode" : "🚀 Backend Connected"} •{" "}
                {mode === "tooling" ? "⚡ Tooling" : "🔍 RAG"} {userLocation && <span>• Location Enabled</span>}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Mode Toggle */}
            <div className="flex items-center gap-1 bg-slate-100 border border-slate-200 p-1 rounded-full">
              <button
                onClick={() => {
                  setMode("tooling")
                  onModeChange("tooling")
                }}
                className={`px-4 py-2 rounded-full text-xs font-semibold transition-all flex items-center gap-1 ${
                  mode === "tooling" ? "bg-teal-500 text-white shadow" : "text-slate-600 hover:bg-slate-50"
                }`}
              >
                <Zap className="w-3 h-3" />
                Tooling
              </button>
              <button
                onClick={() => {
                  setMode("rag")
                  onModeChange("rag")
                }}
                className={`px-4 py-2 rounded-full text-xs font-semibold transition-all flex items-center gap-1 ${
                  mode === "rag" ? "bg-teal-600 text-white shadow" : "text-slate-600 hover:bg-slate-50"
                }`}
              >
                <Shield className="w-3 h-3" />
                RAG
              </button>
            </div>

            {userLocation && (
              <Button variant="ghost" size="icon" className="rounded-full text-teal-600 hover:bg-teal-50">
                <MapPin className="w-5 h-5" />
              </Button>
            )}

            <Button variant="ghost" size="icon" className="rounded-full text-slate-600 hover:bg-slate-100">
              <Volume2 className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden flex gap-8 p-8 max-w-7xl mx-auto w-full">
        {/* Chat Area */}
        <div className="flex-1 flex flex-col">
          {/* Messages or Scenarios */}
          {messages.length === 0 ? (
            <div className="flex-1 flex flex-col justify-center">
              <div className="space-y-8">
                <div>
                  <h2 className="text-3xl font-bold text-slate-900 mb-3">Try a Demo Scenario</h2>
                  <p className="text-slate-600">
                    See how AuraCX handles real-world customer queries with location-aware, context-rich responses.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {DEMO_SCENARIOS.map((scenario, i) => (
                    <button
                      key={i}
                      onClick={() => handleDemoScenario(scenario)}
                      className="text-left p-5 rounded-xl border-2 border-slate-200 hover:border-teal-400 bg-white hover:bg-slate-50 hover:shadow-lg transition group"
                    >
                      <h3 className="font-bold text-base text-slate-900 group-hover:text-teal-600 transition">
                        {scenario.title}
                      </h3>
                      <p className="text-sm text-slate-500 mt-2">{scenario.description}</p>
                      <div className="mt-4 flex items-center gap-2">
                        {scenario.mode === "tooling" ? (
                          <span className="inline-flex items-center gap-1 text-xs bg-teal-100 text-teal-700 px-3 py-1 rounded-full font-semibold">
                            <Zap className="w-3 h-3" />
                            Tooling
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-xs bg-teal-900 text-white px-3 py-1 rounded-full font-semibold">
                            <Shield className="w-3 h-3" />
                            RAG
                          </span>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="flex-1 overflow-y-auto space-y-5 mb-6">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                  {message.type === "user" ? (
                    <div className="bg-teal-600 text-white rounded-2xl px-5 py-3 max-w-md shadow-md">
                      <p className="text-sm leading-relaxed">{message.content}</p>
                    </div>
                  ) : (
                    <div className="max-w-2xl">
                      <ResponseCard
                        content={message.content}
                        confidence={message.confidence || 0}
                        provenance={message.provenance || []}
                        actions={message.actions || []}
                        mode={message.mode || mode}
                      />
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}

          {/* Privacy Notice */}
          {messages.length === 0 && (
            <div className="text-xs text-slate-600 bg-slate-100 p-4 rounded-lg border border-slate-200 mb-6">
              🔒 <span className="font-semibold">Privacy Protected:</span> Audio will be masked and no raw PII is sent
              to external models. Your location is only used for proximity calculations.
            </div>
          )}

          {/* Input Area */}
          <div className="space-y-3">
            <div className="flex gap-3">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === "Enter" && !isProcessing) {
                    handleSendMessage()
                  }
                }}
                placeholder="Ask anything... (e.g., 'Are you open?', 'I'm cold', 'Any deals?')"
                disabled={isProcessing}
                className="rounded-full border-2 border-slate-200 focus:border-teal-500 bg-white px-5 py-3 text-sm"
              />
              <Button
                onClick={() => setIsRecording(!isRecording)}
                size="icon"
                variant={isRecording ? "default" : "outline"}
                className={`rounded-full ${isRecording ? "bg-red-500 hover:bg-red-600" : "border-2 border-slate-200"}`}
                disabled={isProcessing}
              >
                <Mic className={`w-5 h-5 ${isRecording ? "animate-pulse" : ""}`} />
              </Button>
              <Button
                onClick={handleSendMessage}
                size="icon"
                className="rounded-full bg-teal-600 hover:bg-teal-700 text-white"
                disabled={isProcessing || !input.trim()}
              >
                <Send className="w-5 h-5" />
              </Button>
            </div>
          </div>
        </div>

        {/* Agent Activity Panel */}
        <AgentActivityPanel
          agents={activeAgents}
          currentThinkingStep={currentThinkingStep}
          isProcessing={isProcessing}
          mode={mode}
          userLocation={userLocation}
        />
      </div>
    </div>
  )
}
