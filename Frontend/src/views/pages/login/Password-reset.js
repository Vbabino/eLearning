import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CFormInput,   
  CInputGroup,
  CInputGroupText,
  CRow,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {  cilUser } from '@coreui/icons'
import api from '../../../services/api'
import { ACCESS_TOKEN, REFRESH_TOKEN, IS_APPROVED, ID } from '../../../constants'

const Login = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({ email: '' })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Clear any previous session tokens before storing new ones
      localStorage.removeItem(ACCESS_TOKEN)
      localStorage.removeItem(REFRESH_TOKEN)
      localStorage.removeItem(IS_APPROVED)
      localStorage.removeItem(ID)
      
      // Make password reset request
      const res = await api.post('/api/auth/request-password-reset/', formData)

      // Notify user for further actions
      alert('OTP code sent to your email')

      
    } catch (error) {
      alert(error.response?.data?.detail || 'OTP request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={8}>
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm onSubmit={handleSubmit}>
                    <h1>Get a One Time Password code</h1>
                    <p className="text-body-secondary">Enter your email to receive your OTP</p>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilUser} />
                      </CInputGroupText>
                      <CFormInput
                        placeholder="email"
                        autoComplete="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                      />
                    </CInputGroup>

                    <CRow>
                      <CCol xs={6}>
                        <CButton color="primary" className="px-4" type="submit" disabled={loading}>
                          {loading ? 'Sending...' : 'Send OTP code'}
                        </CButton>
                      </CCol>
                      <CCol xs={6} className="text-right">
                        <Link to="/verify-otp">
                          <CButton color="link" className="px-0">
                            Verify OTP
                          </CButton>
                        </Link>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Login
