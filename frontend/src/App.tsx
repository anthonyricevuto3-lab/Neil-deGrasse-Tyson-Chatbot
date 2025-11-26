
import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Chat from './components/Chat'
import Sources from './components/Sources'
import './styles/App.css'
// Whitelisted, successfully indexed sources (103 URLs)
const ALLOWED_SOURCES = [
  'https://amatranscripts.com/ama/neil_degrasse_tyson_2011-11-13.html',
  'https://amatranscripts.com/ama/neil_degrasse_tyson_2017-04-02.html',
  'https://art19.com/shows/tim-ferriss-show',
  'https://billmoyers.com/2014/01/28/part-three-interview-highlights-neil-degrasse-tyson-on-science-literacy/',
  'https://lithub.com/neil-degrasse-tyson-writes-to-his-fans/',
  'https://neildegrassetyson.com/commentary/1998-07-22-misaligned-stars/',
  'https://neildegrassetyson.com/commentary/2001-01-01-destiny-in-space/',
  'https://neildegrassetyson.com/commentary/2002-11-25-where-even-the-sky-is-no-limit/',
  'https://neildegrassetyson.com/commentary/2007-08-05-why-america-needs-to-explore-space/',
  'https://neildegrassetyson.com/commentary/2008-06-06-vote-by-numbers/',
  'https://neildegrassetyson.com/commentary/2008-06-22-for-the-love-of-hubble/',
  'https://neildegrassetyson.com/commentary/2011-08-21-if-i-were-president/',
  'https://neildegrassetyson.com/commentary/2015-12-17-dark-matter/',
  'https://neildegrassetyson.com/commentary/2016-01-23-what-science-is/',
  'https://neildegrassetyson.com/commentary/2016-08-07-reflections-on-rationalia/',
  'https://neildegrassetyson.com/commentary/2017-04-21-science-in-america/',
  'https://neildegrassetyson.com/commentary/2019-09-25-hawaiis-conduit-to-cosmos/',
  'https://neildegrassetyson.com/commentary/2020-06-03-reflections-on-color-of-my-skin/',
  'https://neildegrassetyson.com/commentary/2021-03-18-because-of-science/',
  'https://neildegrassetyson.com/commentary/2022-05-04-few-words-on-abortion/',
  'https://neildegrassetyson.com/commentary/2022-11-17-navigate-arguments-during-holidays/',
  'https://neildegrassetyson.com/essays/1995-03-the-coriolis-force/',
  'https://neildegrassetyson.com/essays/1995-11-the-tidal-force/',
  'https://neildegrassetyson.com/essays/1996-06-ends-of-the-world/',
  'https://neildegrassetyson.com/essays/1996-07-onward-to-the-edge/',
  'https://neildegrassetyson.com/essays/1996-08-forged-in-the-stars/',
  'https://neildegrassetyson.com/essays/1996-09-the-search-for-life-in-the-universe/',
  'https://neildegrassetyson.com/essays/1996-11-outward-bound/',
  'https://neildegrassetyson.com/essays/1996-12-in-defense-of-the-big-bang/',
  'https://neildegrassetyson.com/essays/1997-03-on-being-round/',
  'https://neildegrassetyson.com/essays/1997-09-coming-attractions/',
  'https://neildegrassetyson.com/essays/1997-10-the-search-for-planets/',
  'https://neildegrassetyson.com/essays/1998-03-the-greatest-story-ever-told/',
  'https://neildegrassetyson.com/essays/1998-04-to-fly/',
  'https://neildegrassetyson.com/essays/1998-05-water-water/',
  'https://neildegrassetyson.com/essays/1998-09-space-travel-troubles/',
  'https://neildegrassetyson.com/essays/1998-10-certain-uncertainties-part-1/',
  'https://neildegrassetyson.com/essays/1998-11-certain-uncertainties-part-2/',
  'https://neildegrassetyson.com/essays/1999-02-plutos-honor/',
  'https://neildegrassetyson.com/essays/1999-05-goldilocks-and-the-three-planets/',
  'https://neildegrassetyson.com/essays/1999-10-holy-wars/',
  'https://neildegrassetyson.com/essays/2000-10-doubling-time/',
  'https://neildegrassetyson.com/essays/2000-11-on-earth-as-in-the-heavens/',
  'https://neildegrassetyson.com/essays/2000-12-the-universe-as-a-muse/',
  'https://neildegrassetyson.com/essays/2001-02-the-beginning-of-science/',
  'https://neildegrassetyson.com/essays/2001-03-coming-to-our-senses/',
  'https://neildegrassetyson.com/essays/2001-09-over-the-rainbow/',
  'https://neildegrassetyson.com/essays/2001-12-fear-of-numbers/',
  'https://neildegrassetyson.com/essays/2002-03-colors-of-the-cosmos/',
  'https://neildegrassetyson.com/essays/2002-04-the-five-points-of-lagrange/',
  'https://neildegrassetyson.com/essays/2002-05-on-being-baffled/',
  'https://neildegrassetyson.com/essays/2002-06-hollywood-nights/',
  'https://neildegrassetyson.com/essays/2002-07-the-periodic-table-of-the-cosmos/',
  'https://neildegrassetyson.com/essays/2002-10-let-there-be-dark/',
  'https://neildegrassetyson.com/essays/2002-11-going-ballistic/',
  'https://neildegrassetyson.com/essays/2003-02-footprints-in-the-sands-of-science/',
  'https://neildegrassetyson.com/essays/2003-03-stick-in-the-mud-astronomy/',
  'https://neildegrassetyson.com/essays/2003-04-30-a-perfect-world/',
  'https://neildegrassetyson.com/essays/2003-04-reaching-for-the-stars-americas-choice/',
  'https://neildegrassetyson.com/essays/2003-09-in-the-beginning/',
  'https://neildegrassetyson.com/essays/2003-10-let-there-be-light/',
  'https://neildegrassetyson.com/essays/2004-04-launching-the-right-stuff/',
  'https://neildegrassetyson.com/essays/2004-11-the-importance-of-being-constant/',
  'https://neildegrassetyson.com/essays/2005-06-fueling-up/',
  'https://neildegrassetyson.com/essays/2005-07-heading-out/',
  'https://neildegrassetyson.com/essays/2005-11-the-perimeter-of-ignorance/',
  'https://neildegrassetyson.com/essays/2006-11-delusions-of-space-enthusiasts/',
  'https://neildegrassetyson.com/essays/2007-04-the-cosmic-perspective/',
  'https://neildegrassetyson.com/essays/2007-06-plutos-requiem/',
  'https://neildegrassetyson.com/essays/2008-04-spacecraft-behaving-badly/',
  'https://neildegrassetyson.com/essays/2022-09-power-of-cosmic-perspective/',
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
