import React from 'react'
import { CContainer, CRow, CCol, CCard, CCardBody, CCardHeader, CButton } from '@coreui/react'
import { useNavigate } from 'react-router-dom'


const WelcomePage = () => {
  const navigate = useNavigate();

  const handleExploreCourses = () => {
    navigate('/courses/list');
  }

  return (
    <CContainer>
      <CRow className="justify-content-center">
        <CCol md="8">
          <CCard>
            <CCardHeader>
              <h1>Welcome to eLearning</h1>
            </CCardHeader>
            <CCardBody>
              <p>
                Welcome to our eLearning platform. Here you can find various courses to enhance your
                skills.
              </p>
              <CButton color="primary" onClick={handleExploreCourses}>
                Explore Courses
              </CButton>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </CContainer>
  )
}

export default WelcomePage
