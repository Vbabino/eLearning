import React, { useEffect, useState } from 'react'
import { CCard, CCardBody, CCardHeader, CCol, CRow } from '@coreui/react'
import { useNavigate } from 'react-router-dom'


import api from '../../../services/api'

const CoursesList = () => {
  const [courses, setCourses] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get('/api/courses/list/')
        setCourses(response.data)
      } catch (error) {
        console.error('Error fetching courses:', error)
      }
    }

    fetchCourses()
  }, [])

  return (
    <CRow className="mb-4">
      {courses.map((course) => (
        <CCol
          xs="12"
          sm="6"
          md="4"
          key={course.id}
          className="mb-4"
          onClick={() => {
            navigate(`/courses/${course.id}`) 
          }}
          style={{ cursor: 'pointer' }}
        >
          <CCard>
            <CCardHeader>{course.title}</CCardHeader>
            <CCardBody>
              <p>{course.description}</p>
              <small>Created at: {new Date(course.created_at).toLocaleDateString()}</small>
              <br />
              <small>Updated at: {new Date(course.updated_at).toLocaleDateString()}</small>
            </CCardBody>
          </CCard>
        </CCol>
      ))}
    </CRow>
  )
}

export default CoursesList
