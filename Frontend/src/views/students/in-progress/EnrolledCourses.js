import React, { useEffect, useState } from 'react'
import { CCard, CCardBody, CCardHeader, CCol, CRow, CButton } from '@coreui/react'
import { useNavigate } from 'react-router-dom'

import api from '../../../services/api'
import CIcon from '@coreui/icons-react'
import {  cilFolderOpen } from '@coreui/icons'

const EnrolledCourses = () => {
  const [courses, setCourses] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get(`/api/courses/list/students/`)
        setCourses(response.data)
      } catch (error) {
        console.error('Error fetching courses:', error)
      }
    }

    fetchCourses()
  }, [])
  
  const userType = localStorage.getItem('user_type')
  if (userType !== 'student') {
    return <div>Access Denied</div>
  }
  
  if (courses.message){
    return (
      <div className="text-center">
        <h4>{courses.message}</h4>
      </div>
    )
  }

  return (
    <CRow className="mb-4">
      {courses.map((course) => (
        <CCol xs="12" sm="6" md="4" key={course.id} className="mb-4" style={{ cursor: 'pointer' }}>
          <CCard>
            <CCardHeader>{course.title}</CCardHeader>
            <CCardBody>
              <p
                style={{
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                }}
              >
                {course.description}
              </p>
              <small>Created at: {new Date(course.created_at).toLocaleDateString()}</small>
              <br />
              <small>Updated at: {new Date(course.updated_at).toLocaleDateString()}</small>
              <br />
              <CButton
                color="success"
                className="rounded-pill shadow-sm mt-2"
                onClick={() => navigate(`/students/enrolled-courses-materials/${course.id}/`)}
              >
                <CIcon icon={cilFolderOpen} className="me-1" />
                View Materials
              </CButton>
              <br />
              <CButton
                color="warning"
                className="rounded-pill shadow-sm mt-2"
                onClick={() => navigate(`/students/enrolled-courses-feedback/${course.id}/`)}
              >
                <CIcon icon={cilFolderOpen} className="me-1" />
                Leave feedback
              </CButton>
            </CCardBody>
          </CCard>
        </CCol>
      ))}
    </CRow>
  )
}

export default EnrolledCourses
