
import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Chat from './components/Chat'
import Sources from './components/Sources'
import { TRAINING_URLS } from './data/trainingUrls.ts'
import './styles/App.css'
// Single source of truth: use training URLs list
const ALLOWED_SOURCES = TRAINING_URLS
const ALLOWED_SET = new Set(ALLOWED_SOURCES)

function App() {
  const [sources, setSources] = useState<string[]>(ALLOWED_SOURCES)

  // Lock the sources list to the allowed whitelist
  const addSources = (_incoming: string[]) => {
    setSources(Array.from(ALLOWED_SET))
  }

  // Fetch indexed-only sources from backend and intersect with whitelist
  useEffect(() => {
    const apiBase = import.meta.env.VITE_API_URL || ''
    if (!apiBase) return
    fetch(`${apiBase}/sources?indexed_only=1`)
      .then(r => r.json())
      .then(data => {
        if (data && Array.isArray(data.sources)) {
          const filtered = data.sources.filter((s: string) => ALLOWED_SET.has(s))
          setSources(filtered.length ? filtered : Array.from(ALLOWED_SET))
        }
      })
      .catch(() => {
        // fallback to embedded whitelist
      })
  }, [])

  return (
    <BrowserRouter>
      <div className="app space-bg">
        <div className="starfield"></div>
        <header className="app-header space-glass">
          <div className="header-content">
            <img 
              src="https://www.tennesseetheatre.com/assets/img/Static_SocialPhoto-Instagram_1080x1080_NeilDeGrasseTyson_2024_Regional_TennesseeTheatre_0226-402441bce2.jpg" 
              alt="Neil deGrasse Tyson" 
              className="ndt-avatar hologram"
              onError={(e) => {
                e.currentTarget.src = 'https://ui-avatars.com/api/?name=NDT&background=2d2dff&color=fff&size=128&bold=true'
              }}
            />
            <div className="header-text">
              <h1 className="futuristic-title">Neil deGrasse Tyson AI</h1>
              <p className="header-quote">"The universe is under no obligation to make sense to you."</p>
            </div>
            <div className="status-indicator">
              <span className="status-dot"></span>
              <span>Ready</span>
            </div>
          </div>
          <nav className="app-nav">
            <Link to="/" className="nav-link">💬 Chat</Link>
            <Link to="/sources" className="nav-link">📚 Sources ({sources.length})</Link>
          </nav>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Chat onNewSources={addSources} />} />
            <Route path="/sources" element={<Sources sources={sources} />} />
          </Routes>
        </main>
        <footer className="app-footer space-glass">
          <p>🌌 Powered by RAG • All responses grounded in NDT's writings and interviews</p>
        </footer>
      </div>
    </BrowserRouter>
  )
}

export default App
