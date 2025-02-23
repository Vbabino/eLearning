import React, {useState} from 'react'
import {
  CButton,
  CCard,
  CCardBody,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
  CFormCheck,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser } from '@coreui/icons'
import { ACCESS_TOKEN, REFRESH_TOKEN, IS_APPROVED, ID } from '../../../constants'
import { useNavigate } from 'react-router-dom' 
import api from '../../../services/api'

const Register = () => {
  // Clear any previous session tokens before storing new ones
  localStorage.removeItem(ACCESS_TOKEN)
  localStorage.removeItem(REFRESH_TOKEN)
  localStorage.removeItem(IS_APPROVED)
  localStorage.removeItem(ID)
  
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    user_type: '',
  })
  const [loading, setLoading] = useState(false)
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }
  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const res = await api.post('/api/auth/register/', formData)
      alert('Registration successful')
      navigate('/login')
    } catch (error) {
      alert(error.response?.data?.detail || 'Registration failed') 
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={9} lg={7} xl={6}>
            <CCard className="mx-4">
              <CCardBody className="p-4">
                <CForm onSubmit={handleSubmit}>
                  <h1>Register</h1>
                  <p className="text-body-secondary">Create your account</p>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilUser} />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="First Name"
                      autoComplete="first-name"
                      value={formData.first_name}
                      name="first_name"
                      onChange={handleChange}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilUser} />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="Last Name"
                      autoComplete="last-name"
                      value={formData.last_name}
                      name="last_name"
                      onChange={handleChange}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>@</CInputGroupText>
                    <CFormInput
                      placeholder="Email"
                      autoComplete="email"
                      value={formData.email}
                      name="email"
                      onChange={handleChange}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Password"
                      autoComplete="new-password"
                      value={formData.password}
                      name="password"
                      onChange={handleChange}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-4">
                    <CInputGroupText className="me-2">
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormCheck
                      inline
                      id="inlineCheckbox1"
                      name="user_type"
                      value="teacher"
                      label="Teacher"
                      onChange={handleChange}
                      checked={formData.user_type === 'teacher'}
                    />
                    <CFormCheck
                      inline
                      id="inlineCheckbox2"
                      name="user_type"
                      value="student"
                      label="Student"
                      onChange={handleChange}
                      checked={formData.user_type === 'student'}
                    />
                  </CInputGroup>
                  <div className="d-grid">
                    <CButton color="success" type="submit" disabled={loading}>
                      {loading ? 'Registering...' : 'Create Account'}
                    </CButton>
                  </div >
                </CForm>
                <div className='mt-2'>Already have an account? <CButton color="link" onClick={() => navigate('/login')}>Login here</CButton></div>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Register
