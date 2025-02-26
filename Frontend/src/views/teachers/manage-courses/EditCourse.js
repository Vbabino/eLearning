import React, { useState } from 'react'
import { useParams } from 'react-router-dom'
import { CButton, CContainer, CForm, CFormInput } from '@coreui/react'
import api from '../../../services/api'
import { useNavigate } from 'react-router-dom'

const EditCourseDetails = () => {
  const { id } = useParams()
  const userID = localStorage.getItem('id')

  const [formData, setFormData] = useState({ title: '', description: '' })
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.put(`/api/courses/${id}/update/`, {...formData, teacher: userID})
      alert('Course updated successfully')
      navigate('/teachers/manage-courses')
    } catch (error) {
      alert(error.response?.data?.detail || 'Update failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <CContainer>
        <p className="text-body-secondary">Update course details:</p>

        <CForm onSubmit={handleSubmit}>
          <CFormInput
            className="mb-2"
            placeholder="Title"
            autoComplete="title"
            value={formData.title}
            name="title"
            onChange={handleChange}
          />
          <CFormInput
            className="mb-2"
            placeholder="Description"
            autoComplete="description"
            value={formData.description}
            name="description"
            onChange={handleChange}
          />
          <CButton type="submit" color="primary" disabled={loading}>
            {loading ? 'Updating...' : 'Update'}
          </CButton>
        </CForm>
      </CContainer>
    </div>
  )
}

export default EditCourseDetails
