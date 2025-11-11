export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
  metadata?: Record<string, any>
}

export interface ChatRequest {
  message: string
  conversation_id?: string
}

export interface ChatResponse {
  response: string
  sources: string[]
  metadata?: Record<string, any>
}
