
import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Chat from './components/Chat'
import Sources from './components/Sources'
import './styles/App.css'

// Successfully indexed training sources - only URLs that worked
const TRAINING_URLS = [
  'https://amatranscripts.com/ama/neil_degrasse_tyson_2011-11-13.html',
  'https://amatranscripts.com/ama/neil_degrasse_tyson_2017-04-02.html',
  'https://art19.com/shows/tim-ferriss-show',
  'https://billmoyers.com/2014/01/28/part-three-interview-highlights-neil-degrasse-tyson-on-science-literacy/',
  'https://pointofinquiry.org/2007/01/neil_degrasse_tyson_death_by_black_hole/',
  'https://pointofinquiry.org/2009/03/neil_degrasse_tyson_-_the_pluto_files/',
  'https://pointofinquiry.org/2011/02/neil_degrasse_tyson_communicating_science/',
  'https://pointofinquiry.org/2013/07/neil_degrasse_tyson_communicating_science_to_the_public2013/',
  'https://singjupost.com/transcript-astrophysicist-neil-degrasse-tyson-on-joe-rogan-podcast-1159/',
  'https://singjupost.com/transcript-the-brutal-truth-about-astrology-neil-degrasse-tyson-on-doac-podcast/',
  'https://smashnotes.com/p/the-joe-rogan-experience/e/1347-neil-degrasse-tyson/transcript',
  'https://speakola.com/ideas/neil-degrasse-tyson-science-in-america-2017',
  'https://tim.blog/2019/10/15/neil-degrasse-tyson-transcript/',
  'https://transcripts.cnn.com/show/cnr/date/2023-09-24/segment/05',
  'https://transcripts.cnn.com/show/ctmo/date/2024-10-30/segment/04',
  'https://transcripts.cnn.com/show/fzgps/date/2012-04-01/segment/01',
  'https://transcripts.cnn.com/show/fzgps/date/2013-03-24/segment/01',
  'https://transcripts.cnn.com/show/fzgps/date/2014-08-10/segment/01',
  'https://transcripts.cnn.com/show/fzgps/date/2017-05-07/segment/01',
  'https://transcripts.cnn.com/show/fzgps/date/2017-09-17/segment/01',
  'https://transcripts.cnn.com/show/fzgps/date/2021-07-11/segment/01',
  'https://transcripts.cnn.com/show/fzgps?start_fileid=fzgps_2018-01-07_01',
  'https://transcripts.cnn.com/show/se/date/2003-08-26/segment/18',
  'https://transcripts.cnn.com/show/se?start_fileid=se_2003-09-03_01',
  'https://transcripts.cnn.com/show/wtcw/date/2023-02-05/segment/01',
  'https://whatrocks.github.io/commencement-db/2015-neil-degrasse-tyson-university-of-massachusetts%2C-amherst/',
  'https://www.amnh.org/explore/science-topics/cosmic-collisions',
  'https://www.haydenplanetarium.org/tyson/',
  'https://www.haydenplanetarium.org/tyson/essays/',
  'https://www.meditationmag.com/blog/neil-degrasse-tyson/',
  'https://www.pbs.org/wgbh/nova/origins/tyson.html',
  'https://www.pbs.org/wgbh/nova/space/notes-pluto.html',
  'https://www.pbs.org/wgbh/nova/transcripts/3111_origins.html',
  'https://www.pbs.org/wgbh/nova/transcripts/3112_origins.html',
  'https://www.pbs.org/wgbh/nova/transcripts/3113_origins.html',
  'https://www.pbs.org/wgbh/nova/transcripts/3114_origins.html',
  'https://www.pbs.org/wgbh/nova/transcripts/3401_sciencen.html',
  'https://www.pbs.org/wgbh/nova/transcripts/3411_sciencen.html',
  'https://www.rev.com/transcripts/neil-degrasse-tyson-answers-artemis-i-questions-transcript',
  'https://ytscribe.com/th/v/MtQ0qxyf-Ds',
  'https://ytscribe.com/v/dXOLJOnLKDg'
]

function App() {
  const [sources, setSources] = useState<string[]>(TRAINING_URLS)

  const addSources = (incoming: string[]) => {
    setSources(prev => {
      const merged = new Set(prev)
      incoming.forEach(s => merged.add(s))
      return Array.from(merged)
    })
  }

  // Try to fetch additional sources from backend
  useEffect(() => {
    const apiBase = import.meta.env.VITE_API_URL || ''
    if (!apiBase) return
    fetch(`${apiBase}/sources`)
      .then(r => r.json())
      .then(data => {
        if (data && Array.isArray(data.sources)) {
          setSources(prev => Array.from(new Set([...prev, ...data.sources])))
        }
      })
      .catch(() => {
        // Backend not available, fallback to embedded URLs already loaded
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
