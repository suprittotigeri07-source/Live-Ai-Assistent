import { useState, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import {
  Bot,
  User,
  Globe,
  Calculator,
  Copy,
  Check,
  Wrench,
} from 'lucide-react';

/**
 * Renders a single chat message (user or assistant).
 * Supports markdown, syntax-highlighted code blocks, and tool results.
 */
export default function ChatMessage({ message }) {
  const { role, content, type, tool, result } = message;
  const isUser = role === 'user';

  // If this is a tool result message, render the special card
  if (type === 'tool' && result) {
    return (
      <div className="message assistant">
        <div className="message-avatar">
          <Bot />
        </div>
        <div className="message-content">
          <ToolResultCard tool={tool} result={result} />
        </div>
      </div>
    );
  }

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-avatar">
        {isUser ? <User /> : <Bot />}
      </div>
      <div className="message-content">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code: CodeBlock,
          }}
        >
          {content || ''}
        </ReactMarkdown>
      </div>
    </div>
  );
}

/**
 * Code block renderer with syntax highlighting and copy button.
 */
function CodeBlock({ children, className, node, ...rest }) {
  const [copied, setCopied] = useState(false);

  const match = /language-(\w+)/.exec(className || '');
  const language = match ? match[1] : '';
  const codeString = String(children).replace(/\n$/, '');

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(codeString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, [codeString]);

  // Inline code (no language class, no newlines)
  if (!match && !codeString.includes('\n')) {
    return (
      <code className={className} {...rest}>
        {children}
      </code>
    );
  }

  return (
    <div className="code-block-wrapper">
      <div className="code-block-header">
        <span>{language || 'code'}</span>
        <button
          className={`code-copy-btn ${copied ? 'copied' : ''}`}
          onClick={handleCopy}
        >
          {copied ? (
            <>
              <Check size={12} /> Copied
            </>
          ) : (
            <>
              <Copy size={12} /> Copy
            </>
          )}
        </button>
      </div>
      <SyntaxHighlighter
        style={oneDark}
        language={language || 'text'}
        PreTag="div"
        customStyle={{
          margin: 0,
          borderRadius: 0,
          background: 'rgba(0, 0, 0, 0.25)',
          padding: '14px',
          fontSize: '12.5px',
        }}
      >
        {codeString}
      </SyntaxHighlighter>
    </div>
  );
}

/**
 * Renders tool execution results as a special card.
 */
function ToolResultCard({ tool, result }) {
  const toolIcons = {
    web_search: <Globe size={14} />,
    calculator: <Calculator size={14} />,
  };

  const toolLabels = {
    web_search: 'Web Search',
    calculator: 'Calculator',
  };

  const icon = toolIcons[tool] || <Wrench size={14} />;
  const label = toolLabels[tool] || tool;

  return (
    <div className="tool-result-card">
      <div className="tool-result-header">
        {icon}
        <span>{label} Result</span>
      </div>
      <div className="tool-result-body">
        {tool === 'web_search' ? (
          <WebSearchResult data={result} />
        ) : tool === 'calculator' ? (
          <CalculatorResult data={result} />
        ) : (
          <pre style={{ whiteSpace: 'pre-wrap', fontSize: '12px' }}>
            {typeof result === 'string' ? result : JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

function WebSearchResult({ data }) {
  // Tavily returns { answer, results: [...] }
  if (!data) return <p>No results found.</p>;

  const answer = data.answer;
  const results = data.results || [];

  return (
    <>
      {answer && (
        <p style={{ marginBottom: '12px', color: 'var(--text-primary)', fontWeight: 500 }}>
          {answer}
        </p>
      )}
      {results.map((item, i) => (
        <div key={i} className="search-result-item">
          <div className="search-result-title">{item.title}</div>
          <div className="search-result-url">{item.url}</div>
          <div className="search-result-content">
            {item.content?.substring(0, 200)}
            {item.content?.length > 200 ? '…' : ''}
          </div>
        </div>
      ))}
      {results.length === 0 && !answer && <p>No results found.</p>}
    </>
  );
}

function CalculatorResult({ data }) {
  return (
    <p style={{ fontSize: '18px', fontWeight: 700, color: 'var(--accent-tertiary)' }}>
      = {typeof data === 'object' ? JSON.stringify(data) : String(data)}
    </p>
  );
}
