import '../styles/Sources.css'

interface SourcesProps {
  sources: string[]
}

export default function Sources({ sources }: SourcesProps) {
  if (!sources || sources.length === 0) {
    return (
      <div className="sources-container space-glass">
        <h2>📚 Training Sources</h2>
        <p>Loading sources used to train the AI...</p>
      </div>
    )
  }

  return (
    <div className="sources-container space-glass">
      <h2>📚 Training Sources ({sources.length})</h2>
      <p>The AI was trained on these URLs containing Neil deGrasse Tyson's interviews, transcripts, articles, and talks. All responses are grounded in this knowledge base.</p>
      <ul className="sources-list">
        {sources.map(src => (
          <li key={src}>
            <a href={src} target="_blank" rel="noopener noreferrer">{src}</a>
          </li>
        ))}
      </ul>
    </div>
  )
}
