import React, { useEffect, useState } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CRow,
  CButton,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilPencil, cilTrash, cilCloudUpload, cilFolderOpen } from '@coreui/icons'

import api from '../../../services/api'
import { useNavigate } from 'react-router-dom'

const ViewCourses = () => {
  const [courses, setCourses] = useState([])
  const [visible, setVisible] = useState(false)
  const [selectedCourse, setSelectedCourse] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchTeacherCourses = async () => {
      try {
        const response = await api.get(`/api/courses/list/`)
        setCourses(response.data)
      } catch (error) {
        console.error('Error fetching courses:', error)
      }
    }

    fetchTeacherCourses()
  }, [])

  const handleDeleteCourse = async () => {
    if (!selectedCourse) return
    try {
      await api.delete(`/api/courses/${selectedCourse}/delete/`)
      setCourses(courses.filter((course) => course.id !== selectedCourse))
      setVisible(false)
      setSelectedCourse(null)
    } catch (error) {
      console.error('Error deleting course:', error)
    }
  }

  const userType = localStorage.getItem('user_type')

  if (userType !== 'teacher') {
    return <div>Access Denied</div>
  }

  if (courses.message) {
    return (
      <div className="text-right">
        <CCard>
          <CCardBody>
            <h4>{courses.message}</h4>
            <CButton color="primary" onClick={() => navigate('/teachers/manage-courses/create')}>
              Create Course
            </CButton>
          </CCardBody>
        </CCard>
      </div>
    )
  }

  return (
    <div>
      <CRow className="mb-4">
        {courses.map((course) => (
          <CCol sm="6" lg="4" key={course.id} className="mb-4">
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

                <div className="d-flex flex-column mt-2">
                  <div className="d-flex justify-content-between mb-2">
                    <CButton
                      color="primary"
                      className="me-2 rounded-pill shadow-sm"
                      onClick={() => navigate(`/teachers/manage-courses/${course.id}`)}
                    >
                      <CIcon icon={cilPencil} className="me-1" />
                      Edit
                    </CButton>
                    <CButton
                      color="danger"
                      className="rounded-pill shadow-sm"
                      onClick={() => {
                        setSelectedCourse(course.id)
                        setVisible(true)
                      }}
                    >
                      <CIcon icon={cilTrash} className="me-1" />
                      Delete
                    </CButton>
                  </div>

                  <div className="d-flex justify-content-between">
                    <CButton
                      color="info"
                      className="me-2 rounded-pill shadow-sm"
                      onClick={() => navigate(`/teachers/manage-courses/${course.id}/upload`)}
                    >
                      <CIcon icon={cilCloudUpload} className="me-1" />
                      Upload Materials
                    </CButton>
                    <CButton
                      color="success"
                      className="rounded-pill shadow-sm"
                      onClick={() => navigate(`/teachers/manage-courses/${course.id}/materials`)}
                    >
                      <CIcon icon={cilFolderOpen} className="me-1" />
                      View Materials
                    </CButton>
                  </div>
                </div>
                <CModal
                  visible={visible}
                  onClose={() => setVisible(false)}
                  aria-labelledby="LiveDemoExampleLabel"
                >
                  <CModalHeader>
                    <CModalTitle id="LiveDemoExampleLabel">Delete Course</CModalTitle>
                  </CModalHeader>
                  <CModalBody>Are you sure you want to delete this course?</CModalBody>
                  <CModalFooter>
                    <CButton color="secondary" onClick={() => setVisible(false)}>
                      Close
                    </CButton>
                    <CButton color="danger" onClick={handleDeleteCourse}>
                      Confirm Delete
                    </CButton>
                  </CModalFooter>
                </CModal>
              </CCardBody>
            </CCard>
          </CCol>
        ))}
      </CRow>
    </div>
  )
}

export default ViewCourses
