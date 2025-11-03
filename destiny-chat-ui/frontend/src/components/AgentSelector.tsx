/**
 * AgentSelector Component - Agent list with selection
 * 
 * Author: Joanna Mazur (UX Designer)
 * Date: 2025-11-03
 */

import { Users, Circle } from 'lucide-react'
import './AgentSelector.css'

interface Agent {
  name: string
  role: string
  status: string
  specialization: string
}

interface AgentSelectorProps {
  agents: Agent[]
  selectedAgent: string
  onSelectAgent: (agent: string) => void
}

function AgentSelector({ agents, selectedAgent, onSelectAgent }: AgentSelectorProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return '#10b981'
      case 'busy':
        return '#f59e0b'
      case 'offline':
        return '#6b7280'
      default:
        return '#94a3b8'
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'available':
        return 'Dostępny'
      case 'busy':
        return 'Zajęty'
      case 'offline':
        return 'Offline'
      default:
        return 'Nieznany'
    }
  }

  const getAvatarColor = (agentName: string) => {
    // Pastelowe kolory dla różnych agentów
    const colorMap: { [key: string]: string } = {
      'Aleksander Nowak': '#b5a8d6',      // Pastelowy fiolet
      'Tomasz Kamiński': '#a8d5ba',       // Pastelowa zieleń
      'Anna Lewandowska': '#f7b7a3',      // Pastelowy pomarańcz
      'Joanna Mazur': '#f9d5a7',          // Pastelowy żółty
      'Magdalena Wiśniewska': '#d4a5c4',  // Pastelowy różowy
      'Katarzyna Zielińska': '#a3d4e8',   // Pastelowy niebieski
      'Piotr Nowicki': '#c8d4a7',         // Pastelowa oliwka
      'Michał Kowalczyk': '#e8b4a3',      // Pastelowy łosoś
      'Dr. Joanna Kowalska': '#d6b8c5'    // Pastelowa lawenda
    }
    return colorMap[agentName] || '#b5a8d6'
  }

  return (
    <div className="agent-selector">
      {/* @All option */}
      <button
        className={`agent-item ${selectedAgent === '@All' ? 'agent-item-selected' : ''}`}
        onClick={() => onSelectAgent('@All')}
      >
        <div className="agent-avatar" style={{ background: '#a8c5d4' }}>
          <Users size={20} />
        </div>
        <div className="agent-info">
          <div className="agent-name">@All</div>
          <div className="agent-role">Cały zespół</div>
        </div>
      </button>

      <div className="agent-divider">Agenci</div>

      {/* Individual agents */}
      {agents.map((agent) => {
        const agentTag = agent.name  // Use full name instead of just first name
        const isSelected = selectedAgent === agentTag
        
        return (
          <button
            key={agent.name}
            className={`agent-item ${isSelected ? 'agent-item-selected' : ''}`}
            onClick={() => onSelectAgent(agentTag)}
          >
            <div className="agent-avatar" style={{ background: getAvatarColor(agent.name) }}>
              {agent.name.split(' ').map(n => n[0]).join('')}
            </div>
            <div className="agent-info">
              <div className="agent-name">{agent.name}</div>
              <div className="agent-role">{agent.role}</div>
            </div>
            <div className="agent-status">
              <Circle
                size={10}
                fill={getStatusColor(agent.status)}
                color={getStatusColor(agent.status)}
              />
              <span className="agent-status-text">
                {getStatusText(agent.status)}
              </span>
            </div>
          </button>
        )
      })}
    </div>
  )
}

export default AgentSelector
