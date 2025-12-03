/**
 * API Client for AuraCX Backend
 * Handles all communication with the Python FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export interface ChatRequest {
  message: string
  customer_id?: string
  location?: {
    lat: number
    lng: number
  }
  metadata?: Record<string, any>
}

export interface ChatResponse {
  response: string
  confidence: number
  mode: "tooling" | "rag"
  agent_execution?: AgentExecution[]
  sources?: string[]
  recommended_actions?: string[]
  timestamp: string
  request_id: string
  masked_input?: string
  escalation_required?: boolean
}

export interface AgentExecution {
  agent_name: string
  role: string
  status: "queued" | "running" | "completed" | "failed"
  confidence: number
  duration_ms?: number
  output?: any
}

export interface HealthCheckResponse {
  status: "ok" | "error"
  version: string
  mode: string
  timestamp: string
}

/**
 * Health check - verify backend is running
 */
export async function healthCheck(): Promise<HealthCheckResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Health check error:", error)
    throw error
  }
}

/**
 * Send chat message to backend
 */
export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(
        `Chat request failed: ${response.statusText} - ${errorData.detail || "Unknown error"}`
      )
    }

    return await response.json()
  } catch (error) {
    console.error("Chat request error:", error)
    throw error
  }
}

/**
 * Get API documentation
 */
export async function getDocumentation(): Promise<any> {
  try {
    const response = await fetch(`${API_BASE_URL}/docs`, {
      method: "GET",
    })

    if (!response.ok) {
      throw new Error(`Documentation fetch failed: ${response.statusText}`)
    }

    return await response.text()
  } catch (error) {
    console.error("Documentation fetch error:", error)
    throw error
  }
}

/**
 * Get OpenAPI schema
 */
export async function getOpenAPISchema(): Promise<any> {
  try {
    const response = await fetch(`${API_BASE_URL}/openapi.json`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`OpenAPI schema fetch failed: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error("OpenAPI schema fetch error:", error)
    throw error
  }
}
