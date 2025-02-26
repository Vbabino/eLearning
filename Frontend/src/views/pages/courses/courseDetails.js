import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { CCard, CCardBody, CCardHeader, CButton } from '@coreui/react'
import api from '../../../services/api'

const CourseDetails = () => {
  const { id } = useParams()
  const [course, setCourse] = useState(null)
  const [isEnrolled, setIsEnrolled] = useState(false)
  const userType = localStorage.getItem('user_type')

  useEffect(() => {
    api
      .get(`/api/courses/${id}/`)
      .then((response) => {
        setCourse(response.data)
        setIsEnrolled(response.data.is_enrolled)
      })
      .catch((error) => {
        console.error('There was an error fetching the course data!', error)
      })
  }, [id])

  const handleEnroll = () => {
    if (isEnrolled) {
      alert('You are already enrolled in this course.')
      return
    }
    const enrollmentData = {
      student: localStorage.getItem("id"),
      course: id,
      is_active: true,
    }
    api
      .post(`/api/courses/${id}/enroll/`, enrollmentData)
      .then((response) => {
        alert('You have successfully enrolled in the course!')
        setIsEnrolled(true)
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
          onClick={handleEnroll}
          disabled={isEnrolled || userType !== 'student'}
        >
          {isEnrolled ? 'Already Enrolled' : 'Enroll'}
        </CButton>
      </CCardBody>
    </CCard>
  )
}

export default CourseDetails
