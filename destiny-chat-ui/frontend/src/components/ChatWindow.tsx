/**
 * ChatWindow Component - Main chat interface
 * 
 * Author: Joanna Mazur (UX Designer)
 * Date: 2025-11-03
 */

import { useState, useEffect, useRef } from 'react'
import { Send, Loader2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import './ChatWindow.css'

interface Message {
  id: string
  content: string
  sender: string
  timestamp: string
  type: 'user' | 'agent'
}

interface ChatWindowProps {
  selectedAgent: string
}

function ChatWindow({ selectedAgent }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new message arrives
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Add welcome message when agent changes
  useEffect(() => {
    const agentName = selectedAgent.replace('@', '')
    const welcomeMessage: Message = {
      id: `welcome-${Date.now()}`,
      content: `👋 Witaj! Rozmawiam teraz z **${agentName}**. Jak mogę Ci pomóc?`,
      sender: agentName,
      timestamp: new Date().toISOString(),
      type: 'agent'
    }
    setMessages([welcomeMessage])
  }, [selectedAgent])

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isSending) return

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content: inputValue,
      sender: 'You',
      timestamp: new Date().toISOString(),
      type: 'user'
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsSending(true)

    try {
      const response = await fetch('http://localhost:8000/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: inputValue,
          to_agent: selectedAgent,
          from_user: 'User'
        })
      })

      const data = await response.json()

      const agentMessage: Message = {
        id: `agent-${Date.now()}`,
        content: data.content,
        sender: selectedAgent.replace('@', ''),
        timestamp: data.timestamp,
        type: 'agent'
      }

      setMessages(prev => [...prev, agentMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: '❌ Błąd podczas wysyłania wiadomości. Sprawdź, czy backend działa (http://localhost:8000)',
        sender: 'System',
        timestamp: new Date().toISOString(),
        type: 'agent'
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsSending(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="chat-window">
      {/* Messages Area */}
      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.type === 'user' ? 'message-user' : 'message-agent'}`}
          >
            <div className="message-header">
              <span className="message-sender">{message.sender}</span>
              <span className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString('pl-PL', {
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </span>
            </div>
            <div className="message-content">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            className="message-input"
            placeholder={`Napisz wiadomość do ${selectedAgent}...`}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            rows={1}
            disabled={isSending}
          />
          <button
            className="send-button"
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isSending}
          >
            {isSending ? (
              <Loader2 size={20} className="spinner" />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
        <div className="input-hint">
          <kbd>Enter</kbd> aby wysłać, <kbd>Shift + Enter</kbd> dla nowej linii
        </div>
      </div>
    </div>
  )
}

export default ChatWindow
