import '../styles/Sources.css'

interface SourcesProps {
  sources: string[]
}

export default function Sources({ sources }: SourcesProps) {
  if (!sources || sources.length === 0) {
    return (
      <div className="sources-container space-glass">
        <h2>📚 Sources</h2>
        <p>No sources collected yet. Ask questions to build the knowledge reference list.</p>
      </div>
    )
  }

  return (
    <div className="sources-container space-glass">
      <h2>📚 Referenced Sources</h2>
      <p>The chatbot draws from these URLs (interviews, transcripts, articles). They are aggregated from responses but omitted inline for conversational flow.</p>
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
