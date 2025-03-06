import React, { useState } from 'react'
import {
  CButton,
  CContainer,
  CForm,
  CFormInput,
  
} from '@coreui/react'
import { useNavigate } from 'react-router-dom'
import api from '../../../services/api'

const UpdateUser = () => {
  const id = localStorage.getItem('id')
  const [formData, setFormData] = useState({ first_name: '', last_name: '' })
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.put(`/api/auth/user/${id}/`, formData)
      alert('User updated successfully')
      navigate('/user/view')
    } catch (error) {
      alert(error.response?.data?.detail || 'Update failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <CContainer>
        <p className="text-body-secondary">Update your personal details:</p>

        <CForm onSubmit={handleSubmit}>
          <CFormInput
          className='mb-2'
            placeholder="First Name"
            autoComplete="first-name"
            value={formData.first_name}
            name="first_name"
            onChange={handleChange}
          />
          <CFormInput
            className='mb-2'
            placeholder="Last Name"
            autoComplete="last-name"
            value={formData.last_name}
            name="last_name"
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

export default UpdateUser
