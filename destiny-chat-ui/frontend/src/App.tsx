/**
 * Destiny Chat UI - Main App Component
 * 
 * Author: Joanna Mazur (UX Designer)
 * Orchestrated by: Aleksander Nowak
 * Date: 2025-11-03
 */

import { useState, useEffect } from 'react'
import { MessageSquare, Users, Settings } from 'lucide-react'
import ChatWindow from './components/ChatWindow'
import AgentSelector from './components/AgentSelector'
import StatusBar from './components/StatusBar'
import './App.css'

interface Agent {
  name: string
  role: string
  status: string
  specialization: string
}

function App() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [selectedAgent, setSelectedAgent] = useState<string>('@All')
  const [loading, setLoading] = useState(true)

  // Fetch agents on mount
  useEffect(() => {
    fetchAgents()
  }, [])

  const fetchAgents = async () => {
    try {
      const response = await fetch('http://localhost:8000/agents')
      const data = await response.json()
      setAgents(data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching agents:', error)
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <MessageSquare className="logo-icon" size={28} />
          <h1 className="app-title">Destiny Chat UI</h1>
          <span className="app-subtitle">Chat with AI Agents</span>
        </div>
        <div className="header-right">
          <button className="icon-button" title="Settings">
            <Settings size={20} />
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="app-main">
        {/* Sidebar - Agent List */}
        <aside className="app-sidebar">
          <div className="sidebar-header">
            <Users size={20} />
            <h2>Agents</h2>
            <span className="agent-count">{agents.length}</span>
          </div>
          
          {loading ? (
            <div className="loading">Loading agents...</div>
          ) : (
            <AgentSelector
              agents={agents}
              selectedAgent={selectedAgent}
              onSelectAgent={setSelectedAgent}
            />
          )}
        </aside>

        {/* Chat Area */}
        <main className="app-content">
          <StatusBar selectedAgent={selectedAgent} agents={agents} />
          <ChatWindow selectedAgent={selectedAgent} />
        </main>
      </div>
    </div>
  )
}

export default App
