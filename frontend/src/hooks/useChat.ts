import { useState } from 'react'

// Primary backend base URL (deployed Container App)
const DEFAULT_BACKEND = 'https://ndt-backend.politeforest-c8151342.westus.azurecontainerapps.io/api'
// Attempt to read build-time env; fall back to container app URL.
const ENV_BACKEND = (import.meta.env?.VITE_API_URL as string | undefined)?.replace(/\/$/, '')
const API_BASE = (ENV_BACKEND && ENV_BACKEND.length > 0 ? ENV_BACKEND : DEFAULT_BACKEND)

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (message: string) => {
    setIsLoading(true)
    const payload = JSON.stringify({ message })

    // Helper to perform a fetch attempt
    const attempt = async (base: string) => {
      const resp = await fetch(`${base}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: payload
      })
      if (!resp.ok) {
        let detail = `HTTP ${resp.status}`
        try {
          const body = await resp.json()
          if (body?.detail) detail = body.detail
        } catch {/* ignore parse errors */}
        throw new Error(detail)
      }
      return resp.json()
    }

    try {
      let data: any
      try {
        // First attempt with resolved base
        data = await attempt(API_BASE)
      } catch (firstErr) {
        // If initial attempt failed AND env var was missing, no alternate needed
        // If env var existed but failed, try hard-coded default as fallback
        if (API_BASE !== DEFAULT_BACKEND) {
          try {
            data = await attempt(DEFAULT_BACKEND)
          } catch (secondErr) {
            console.error('Fallback attempt failed:', secondErr)
            throw firstErr
          }
        } else {
          throw firstErr
        }
      }

      return {
        response: data.response || data.answer || 'No response from the server',
        sources: data.sources || []
      }
    } catch (error: any) {
      console.error('Error calling API:', error)
      throw new Error(error?.message || 'Request failed')
    } finally {
      setIsLoading(false)
    }
  }

  return { sendMessage, isLoading }
}
