import { useState } from 'react'
import axios from 'axios'

export default function Report({ token }) {
  const [farmerName, setFarmerName] = useState('')
  const [report, setReport] = useState(null)
  const [status, setStatus] = useState('')
  const [actualCarbon, setActualCarbon] = useState('')

  const fetchReport = async () => {
    setStatus('Loading...')
    setReport(null)
    try {
      const params = farmerName ? { farmer_name: farmerName } : {}
      const res = await axios.get(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/farm_report`, {
        params,
        headers: { 'Authorization': `Bearer ${token}` }
      })
      setReport(res.data)
      setStatus('')
    } catch (err) {
      setStatus(err.response?.data?.detail || 'No report found. Upload data first.')
    }
  }

  const verifyCarbon = async () => {
    try {
      const payload = {
        farm_id: report.id,
        actual_carbon_savings: parseFloat(actualCarbon)
      }
      const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/verify_carbon`, payload, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      setStatus(res.data.message)
      setActualCarbon('')
    } catch (err) {
      setStatus(err.response?.data?.detail || 'Failed to verify data. Only authorities/admins can do this.')
    }
  }

  return (
    <div style={{ maxWidth: 520 }}>
      <h2>Farm Carbon Report (ML Predicted)</h2>
      <div style={{ marginBottom: 8 }}>
        <label>
          Filter by Farmer Name (optional)
          <input
            type="text"
            value={farmerName}
            onChange={(e) => setFarmerName(e.target.value)}
            style={{ width: '100%' }}
          />
        </label>
      </div>
      <button onClick={fetchReport}>Get Report</button>

      {status && <p style={{ marginTop: 10 }}>{status}</p>}

      {report && (
        <div style={{ marginTop: 16, padding: 12, border: '1px solid #ddd' }}>
          <p><b>Farm ID:</b> {report.id}</p>
          <p><b>Farmer:</b> {report.farmer_name}</p>
          <p><b>Farm Size (ha):</b> {report.farm_size}</p>
          <p><b>Crop Type:</b> {report.crop_type}</p>
          <p><b>Tree Count:</b> {report.tree_count}</p>
          <p><b>Predicted Carbon Savings:</b> {report.carbon_savings}</p>
          <p><b>Timestamp:</b> {report.timestamp}</p>

          <hr style={{ margin: '16px 0' }} />
          <h4>Authority Area: Verify Actual Carbon (Trains ML)</h4>
          <label style={{ display: 'block', marginBottom: '8px' }}>
            Actual Measured Carbon Savings
            <input
              type="number"
              value={actualCarbon}
              onChange={(e) => setActualCarbon(e.target.value)}
              style={{ width: '100%', marginTop: '4px' }}
            />
          </label>
          <button onClick={verifyCarbon} style={{ backgroundColor: 'green', color: 'white' }}>
            Verify & Train ML Model
          </button>
        </div>
      )}
    </div>
  )
}
