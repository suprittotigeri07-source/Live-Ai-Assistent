import {
  Sparkles,
  MessageSquarePlus,
  Trash2,
  Globe,
  Calculator,
  Clock,
  FileText,
  Zap,
} from 'lucide-react';

const TOOLS = [
  { name: 'Web Search', icon: <Globe size={13} /> },
  { name: 'Calculator', icon: <Calculator size={13} /> },
  { name: 'Date & Time', icon: <Clock size={13} /> },
  { name: 'File Reader', icon: <FileText size={13} /> },
];

export default function Sidebar({ onNewChat, onClearMemory, health }) {
  const statusClass =
    health.status === 'healthy'
      ? 'online'
      : health.status === 'checking'
      ? 'checking'
      : 'offline';

  const statusText =
    health.status === 'healthy'
      ? `Connected · v${health.version}`
      : health.status === 'checking'
      ? 'Connecting…'
      : 'Offline';

  return (
    <aside className="sidebar" id="sidebar">
      {/* Brand */}
      <div className="sidebar-header">
        <div className="sidebar-brand">
          <div className="sidebar-logo">
            <Zap />
          </div>
          <div>
            <div className="sidebar-title">Live AI Assistant</div>
            <div className="sidebar-version">Powered by Ollama</div>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="sidebar-actions">
        <button
          className="sidebar-btn primary"
          onClick={onNewChat}
          id="new-chat-btn"
        >
          <MessageSquarePlus />
          New Conversation
        </button>
        <button
          className="sidebar-btn danger"
          onClick={onClearMemory}
          id="clear-memory-btn"
        >
          <Trash2 />
          Clear Memory
        </button>
      </div>

      {/* Available Tools */}
      <div className="sidebar-section">
        <div className="sidebar-section-title">
          <Sparkles
            size={11}
            style={{ display: 'inline', verticalAlign: 'middle', marginRight: 4 }}
          />
          Available Tools
        </div>
        <div className="tool-list">
          {TOOLS.map((tool) => (
            <div key={tool.name} className="tool-item">
              <span className="tool-dot" />
              {tool.name}
            </div>
          ))}
        </div>
      </div>

      {/* Footer — Connection Status */}
      <div className="sidebar-footer">
        <div className="status-indicator" id="connection-status">
          <span className={`status-dot ${statusClass}`} />
          <span>{statusText}</span>
        </div>
      </div>
    </aside>
  );
}
