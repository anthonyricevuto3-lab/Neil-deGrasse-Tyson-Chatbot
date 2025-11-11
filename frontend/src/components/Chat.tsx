import { useState } from 'react'
import { useChat } from '../hooks/useChat'
import Message from './Message.tsx'
import '../styles/Chat.css'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
}

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const { sendMessage, isLoading } = useChat()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!input.trim() || isLoading) return

    const userMessage: ChatMessage = {
      role: 'user',
      content: input
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')

    try {
      const response = await sendMessage(input)
      
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        sources: response.sources
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, something went wrong. Please try again.'
      }
      
      setMessages(prev => [...prev, errorMessage])
    }
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>👋 Welcome to the Cosmos!</h2>
            <p>Ask me anything about astronomy, physics, space exploration, or the universe. I'm here to share the wonder of science with you!</p>
            <div className="example-questions">
              <button onClick={() => setInput("Why are we made of stardust?")}>
                ⭐ Why are we made of stardust?
              </button>
              <button onClick={() => setInput("What happens inside a black hole?")}>
                🕳️ What happens inside a black hole?
              </button>
              <button onClick={() => setInput("Should humans colonize Mars?")}>
                🚀 Should humans colonize Mars?
              </button>
              <button onClick={() => setInput("What is the cosmic perspective?")}>
                🌌 What is the cosmic perspective?
              </button>
            </div>
          </div>
        )}
        
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
        
        {isLoading && (
          <div className="loading-indicator">
            <span>Thinking...</span>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={isLoading}
          className="chat-input"
        />
        <button 
          type="submit" 
          disabled={isLoading || !input.trim()}
          className="chat-submit"
        >
          Send
        </button>
      </form>
    </div>
  )
}
