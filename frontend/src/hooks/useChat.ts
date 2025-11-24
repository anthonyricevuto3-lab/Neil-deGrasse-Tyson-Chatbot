import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || '/api'

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (message: string) => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return {
        response: data.response || data.answer || 'No response from the server',
        sources: data.sources || []
      }
    } catch (error) {
      console.error('Error calling API:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  return {
    sendMessage,
    isLoading
  }
}
