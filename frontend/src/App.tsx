
import Chat from './components/Chat'
import './styles/App.css'
import { useAuth } from './hooks/useAuth'

function App() {
  const { user, loading, login, logout } = useAuth()

  return (
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
            {loading ? (
              <span>Loading...</span>
            ) : user ? (
              <>
                <span className="status-dot"></span>
                <span>Signed in as {user.userDetails}</span>
                <button onClick={logout} className="auth-button">Logout</button>
              </>
            ) : (
              <button onClick={login} className="auth-button">Sign in with Microsoft</button>
            )}
          </div>
        </div>
      </header>
      <main className="app-main">
        <Chat />
      </main>
      <footer className="app-footer space-glass">
        <p>🌌 Powered by RAG • All responses grounded in NDT's writings and interviews</p>
      </footer>
    </div>
  )
}

export default App
