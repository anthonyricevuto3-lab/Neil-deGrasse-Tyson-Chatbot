import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import '../styles/Message.css'

interface MessageProps {
  message: {
    role: 'user' | 'assistant'
    content: string
    sources?: string[]
  }
}

const NDT_AVATAR = 'https://www.tennesseetheatre.com/assets/img/Static_SocialPhoto-Instagram_1080x1080_NeilDeGrasseTyson_2024_Regional_TennesseeTheatre_0226-402441bce2.jpg'
// Neutral user avatar (remove explicit "You" labeling)
const USER_AVATAR = 'https://ui-avatars.com/api/?name=User&background=e94560&color=fff&size=128'

export default function Message({ message }: MessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <img 
        src={isUser ? USER_AVATAR : NDT_AVATAR}
        alt={isUser ? 'User' : 'Neil deGrasse Tyson'}
        className="message-avatar"
        onError={(e) => {
          e.currentTarget.src = 'https://ui-avatars.com/api/?name=NDT&background=e94560&color=fff&size=128&bold=true'
        }}
      />
      <div className="message-content">
        {isUser ? (
          <p>{message.content}</p>
        ) : (
          <>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
            
            {/* Sources intentionally omitted from inline chat display */}
          </>
        )}
      </div>
    </div>
  )
}
