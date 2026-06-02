import { useState } from 'react'
import axios from 'axios'
import { Box, TextField, Button, Typography, Paper, Stack } from '@mui/material'

export default function UploadData({ token }) {
  const [form, setForm] = useState({
    farmer_name: '',
    farm_size: '',
    crop_type: '',
    tree_count: '',
  })
  const [status, setStatus] = useState('')

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setStatus('Submitting...')
    try {
      const payload = {
        farmer_name: form.farmer_name,
        farm_size: parseFloat(form.farm_size || 0),
        crop_type: form.crop_type,
        tree_count: parseInt(form.tree_count || 0, 10),
      }
      const res = await axios.post(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/upload_data`, payload, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      setStatus(`Success! Saved with id ${res.data.id}`)
    } catch (err) {
      setStatus(err.response?.data?.detail || 'Failed to upload data')
    }
  }

  return (
    <Paper elevation={1} sx={{ p: 2, maxWidth: 520 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Upload Farm Data
      </Typography>
      <Box component="form" onSubmit={handleSubmit} noValidate>
        <Stack spacing={2}>
          <TextField
            label="Farmer Name"
            name="farmer_name"
            value={form.farmer_name}
            onChange={handleChange}
            required
            fullWidth
            size="small"
          />
          <TextField
            label="Farm Size (ha)"
            type="number"
            inputProps={{ step: '0.01' }}
            name="farm_size"
            value={form.farm_size}
            onChange={handleChange}
            required
            fullWidth
            size="small"
          />
          <TextField
            label="Crop Type"
            name="crop_type"
            value={form.crop_type}
            onChange={handleChange}
            required
            fullWidth
            size="small"
          />
          <TextField
            label="Tree Count"
            type="number"
            name="tree_count"
            value={form.tree_count}
            onChange={handleChange}
            required
            fullWidth
            size="small"
          />
          <Box>
            <Button type="submit" variant="contained">
              Submit
            </Button>
          </Box>
        </Stack>
      </Box>
      {status && (
        <Typography variant="body2" sx={{ mt: 2 }}>
          {status}
        </Typography>
      )}
    </Paper>
  )
}
