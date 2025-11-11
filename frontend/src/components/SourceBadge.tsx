import '../styles/SourceBadge.css'

interface SourceBadgeProps {
  source: string
}

export default function SourceBadge({ source }: SourceBadgeProps) {
  return (
    <span className="source-badge" title={source}>
      📚 {source}
    </span>
  )
}
