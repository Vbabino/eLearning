import React, { useState } from 'react'
import { CButton, CForm, CFormInput } from '@coreui/react'
import { useNavigate } from 'react-router-dom'
import api from '../../../services/api'

const UploadProfilePhoto = () => {
  const id = localStorage.getItem('id')
  const [formData, setFormData] = useState({ photo: '' })
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleFileChange = (event) => {
    setFormData({ ...formData, photo: event.target.files[0] })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    if (formData.photo) {
      const data = new FormData()
      data.append('photo', formData.photo)
      try {
        await api.put(`/api/auth/user/upload-profile-photo/${id}/`, data, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        alert('Profile photo uploaded successfully')
        localStorage.setItem('profileUpdated', Date.now())
        navigate('/user/view')
      } catch (error) {
        alert(error.response?.data?.detail || 'Upload failed')
      } finally {
        setLoading(false)
      }
    } else {
      console.log('No file selected')
    }
  }

  return (
    <CForm onSubmit={handleSubmit}>
      <CFormInput type="file" onChange={handleFileChange} label="Choose File" required />
      <CButton className="mt-2" type="submit" color="primary" disabled={loading}>
        {loading ? 'Uploading...' : 'Upload'}
      </CButton>
    </CForm>
  )
}

export default UploadProfilePhoto
