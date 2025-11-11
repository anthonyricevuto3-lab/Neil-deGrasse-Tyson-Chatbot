import { useState } from 'react'
import Chat from './components/Chat'
import './styles/App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <img 
            src="https://www.tennesseetheatre.com/assets/img/Static_SocialPhoto-Instagram_1080x1080_NeilDeGrasseTyson_2024_Regional_TennesseeTheatre_0226-402441bce2.jpg" 
            alt="Neil deGrasse Tyson" 
            className="ndt-avatar"
            onError={(e) => {
              e.currentTarget.src = 'https://ui-avatars.com/api/?name=NDT&background=e94560&color=fff&size=128&bold=true'
            }}
          />
          <div className="header-text">
            <h1>Neil deGrasse Tyson AI</h1>
            <p className="header-quote">"The universe is under no obligation to make sense to you."</p>
          </div>
          <div className="status-indicator">
            <span className="status-dot"></span>
            <span>Ready</span>
          </div>
        </div>
      </header>
      <main className="app-main">
        <Chat />
      </main>
      <footer className="app-footer">
        <p>🌌 Powered by RAG • All responses grounded in NDT's writings and interviews</p>
      </footer>
    </div>
  )
}

export default App
