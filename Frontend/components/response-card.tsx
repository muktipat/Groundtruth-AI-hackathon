"use client"

import type React from "react"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AlertCircle, MapPin, Gift, Repeat2, Phone, ExternalLink } from "lucide-react"

interface ResponseCardProps {
  content: string
  confidence: number
  provenance: string[]
  actions: Array<{ label: string; type: string }>
  mode: "tooling" | "rag"
}

export default function ResponseCard({ content, confidence, provenance, actions, mode }: ResponseCardProps) {
  const isLowConfidence = confidence < 0.6

  return (
    <Card className="p-5 bg-white border-2 border-slate-200 hover:border-teal-300 hover:shadow-lg transition space-y-4">
      {/* Response Text */}
      <div className="space-y-2">
        <p className="text-sm leading-relaxed text-slate-900">{content}</p>
      </div>

      {/* Confidence Score */}
      <div className="flex items-center justify-between py-3 px-4 bg-slate-50 rounded-lg border border-slate-200">
        <span className="text-xs font-bold text-slate-900">Confidence Score</span>
        <div className="flex items-center gap-3">
          <div className="w-24 h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${
                confidence >= 0.8 ? "bg-green-600" : confidence >= 0.6 ? "bg-amber-600" : "bg-red-600"
              }`}
              style={{ width: `${confidence * 100}%` }}
            />
          </div>
          <span className="text-xs font-bold text-slate-900 w-12 text-right">{(confidence * 100).toFixed(0)}%</span>
        </div>
      </div>

      {/* Provenance */}
      {provenance.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-bold text-slate-700">{mode === "tooling" ? "📊 Data Sources" : "📄 Evidence"}</p>
          <div className="flex flex-wrap gap-2">
            {provenance.map((source, i) => (
              <span
                key={i}
                className="text-xs bg-teal-100 text-teal-900 px-3 py-1 rounded-full border border-teal-200 font-mono font-semibold flex items-center gap-1"
              >
                {source}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Low Confidence Warning */}
      {isLowConfidence && (
        <div className="flex gap-3 items-start p-3 bg-amber-50 rounded-lg border-2 border-amber-200">
          <AlertCircle className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" />
          <div className="text-xs text-amber-900">
            <p className="font-bold">Low Confidence Response</p>
            <p className="mt-1">Would you like me to escalate to a human agent?</p>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      {actions.length > 0 && (
        <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-200">
          {actions.map((action, i) => {
            const iconMap: Record<string, React.ReactNode> = {
              map: <MapPin className="w-3 h-3" />,
              coupon: <Gift className="w-3 h-3" />,
              reserve: <Repeat2 className="w-3 h-3" />,
              escalate: <Phone className="w-3 h-3" />,
              more: <ExternalLink className="w-3 h-3" />,
            }

            return (
              <Button
                key={i}
                size="sm"
                variant="outline"
                className="text-xs gap-2 bg-white border-slate-200 text-slate-700 hover:bg-teal-50 hover:border-teal-400 hover:text-teal-700 font-semibold"
              >
                {iconMap[action.type]}
                {action.label}
              </Button>
            )
          })}
        </div>
      )}
    </Card>
  )
}
