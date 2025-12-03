"use client"

import { useState } from "react"
import LandingPage from "@/components/landing-page"
import ChatInterface from "@/components/chat-interface"

export default function Home() {
  const [mode, setMode] = useState<"tooling" | "rag">("tooling")
  const [showChat, setShowChat] = useState(false)

  if (showChat) {
    return <ChatInterface initialMode={mode} onModeChange={setMode} onBack={() => setShowChat(false)} />
  }

  return <LandingPage mode={mode} setMode={setMode} onStartChat={() => setShowChat(true)} />
}
