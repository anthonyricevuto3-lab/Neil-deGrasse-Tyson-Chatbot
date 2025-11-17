import { useState } from 'react'


export function useChat() {
  const [isLoading, setIsLoading] = useState(false)


  // Placeholder sendMessage function (removes dependency on missing api.ts)
  const sendMessage = async (message: string) => {
    setIsLoading(true)
    try {
      // Simulate a response
      return {
        response: `Echo: ${message}`,
        sources: []
      }
    } finally {
      setIsLoading(false)
    }
  }

  return {
    sendMessage,
    isLoading
  }
}
