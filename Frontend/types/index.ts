export type AgentStatus = "queued" | "running" | "verified" | "done" | "failed"

export interface Agent {
  name: string
  role: string
  status: AgentStatus
  confidence: number
  docIds?: string[]
}

export interface Message {
  id: string
  type: "user" | "assistant"
  content: string
  timestamp: Date
  confidence?: number
  provenance?: string[]
  actions?: Array<{ label: string; type: string }>
  mode?: "tooling" | "rag"
}
