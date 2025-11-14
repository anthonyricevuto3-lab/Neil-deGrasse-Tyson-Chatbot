import { useState } from 'react'
import { chatAPI } from '../lib/api.js'

export function useChat() {
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (message: string) => {
    setIsLoading(true)
    try {
      const response = await chatAPI.sendMessage(message)
      return response
    } finally {
      setIsLoading(false)
    }
  }

  return {
    sendMessage,
    isLoading
  }
}
