/**
 * StatusBar Component - Shows current agent info
 * 
 * Author: Joanna Mazur (UX Designer)
 * Date: 2025-11-03
 */

import { Circle, Info } from 'lucide-react'
import './StatusBar.css'

interface Agent {
  name: string
  role: string
  status: string
  specialization: string
}

interface StatusBarProps {
  selectedAgent: string
  agents: Agent[]
}

function StatusBar({ selectedAgent, agents }: StatusBarProps) {
  const getAgentInfo = () => {
    if (selectedAgent === '@All') {
      return {
        name: 'Cały zespół',
        role: 'Koordynacja przez Aleksandra',
        status: 'available',
        specialization: 'Multi-agent collaboration'
      }
    }

    // Find agent by exact name match
    const agent = agents.find(a => a.name === selectedAgent)

    return agent || {
      name: selectedAgent,
      role: 'Unknown',
      status: 'offline',
      specialization: ''
    }
  }

  const agent = getAgentInfo()

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

  return (
    <div className="status-bar">
      <div className="status-bar-left">
        <div className="status-avatar">
          {agent.name.split(' ').map(n => n[0]).join('').substring(0, 2)}
        </div>
        <div className="status-info">
          <div className="status-name">{agent.name}</div>
          <div className="status-role">{agent.role}</div>
        </div>
        <div className="status-indicator">
          <Circle
            size={8}
            fill={getStatusColor(agent.status)}
            color={getStatusColor(agent.status)}
          />
        </div>
      </div>
      
      {agent.specialization && (
        <div className="status-bar-right">
          <Info size={16} />
          <span className="status-specialization">{agent.specialization}</span>
        </div>
      )}
    </div>
  )
}

export default StatusBar
