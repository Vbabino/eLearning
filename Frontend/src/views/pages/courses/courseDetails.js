import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { CCard, CCardBody, CCardHeader, CButton } from '@coreui/react'
import api from '../../../services/api'
import { USER_TYPE, ID } from '../../../constants'

const CourseDetails = () => {
  const { id } = useParams()
  const [course, setCourse] = useState(null)
  const userType = localStorage.getItem(USER_TYPE)

  useEffect(() => {
    api
      .get(`/api/courses/${id}/`)
      .then((response) => {
        setCourse(response.data)
      })
      .catch((error) => {
        console.error('There was an error fetching the course data!', error)
      })
  }, [id])

  const handleEnroll = () => {
    const enrollmentData = {
      student: localStorage.getItem(ID),
      course: id,
      is_active: true,
    }

    api
      .post(`/api/courses/${id}/enroll/`, enrollmentData)
      .then((response) => {
        alert('You have successfully enrolled in the course!')
      })
      .catch((error) => {
        console.error('There was an error enrolling in the course!', error)
      })
  }

  if (!course) {
    return <div>Loading...</div>
  }

  return (
    <CCard>
      <CCardHeader>
        <h2>{course.title}</h2>
      </CCardHeader>
      <CCardBody>
        <p>
          <strong>Description:</strong> {course.description}
        </p>
        <p>
          <strong>Created At:</strong> {new Date(course.created_at).toLocaleString()}
        </p>
        <p>
          <strong>Updated At:</strong> {new Date(course.updated_at).toLocaleString()}
        </p>
        <CButton
          color="primary"
          onClick={() => {
            handleEnroll()
          }}
          disabled={userType !== 'student'}
        >
          Enroll
        </CButton>
      </CCardBody>
    </CCard>
  )
}

export default CourseDetails
