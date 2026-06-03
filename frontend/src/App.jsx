import { useState } from 'react'
import './App.css'
import UploadData from './UploadData.jsx'
import Report from './Report.jsx'
import Auth from './Auth.jsx'

function App() {
  const [page, setPage] = useState('upload')
  const [token, setToken] = useState(null)

  if (!token) {
    return (
      <div className="bp5-ui-text" style={{ padding: '24px', minHeight: '100vh' }}>
        <div className="bp5-card" style={{ maxWidth: 900, margin: '0 auto', textAlign: 'center' }}>
          <h1 className="bp5-heading">🌍 Carbon MRV Platform</h1>
          <Auth setToken={setToken} />
        </div>
      </div>
    )
  }

  return (
    <div className="bp5-ui-text" style={{ padding: '24px', minHeight: '100vh' }}>
      <div className="bp5-card" style={{ maxWidth: 900, margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 className="bp5-heading">🌍 Carbon MRV Platform</h1>
          <button className="bp5-button" onClick={() => setToken(null)}>Logout</button>
        </div>
        <div style={{ marginBottom: 12 }}>
          <button className="bp5-button bp5-intent-primary" onClick={() => setPage('upload')}>
            Upload Data
          </button>
          <button
            className="bp5-button"
            style={{ marginLeft: 8 }}
            onClick={() => setPage('report')}
          >
            View Report & Predictions
          </button>
        </div>
        <div>{page === 'upload' ? <UploadData token={token} /> : <Report token={token} />}</div>
      </div>
    </div>
  )
}

export default App
