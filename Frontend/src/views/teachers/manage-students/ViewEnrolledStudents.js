import React, { useEffect, useState } from 'react'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CButton,
  CCard,
  CCardBody,
  CCardTitle,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilXCircle, cilCheck } from '@coreui/icons'
import api from '../../../services/api'

const ViewEnrolledStudents = () => {
  const [students, setStudents] = useState({})
  const [isRemoved, setIsRemoved] = useState(false)
  const [isUnblocked, setIsUnblocked] = useState(false)

  useEffect(() => {
    api
      .get('/api/courses/teacher/students/')
      .then((response) => {
        // Group students by course title
        const groupedStudents = response.data.reduce((acc, student) => {
          const courseTitle = student.course_title
          if (!acc[courseTitle]) {
            acc[courseTitle] = []
          }
          acc[courseTitle].push(student)
          return acc
        }, {})
        setStudents(groupedStudents)
      })
      .catch((error) => {
        console.error('Error fetching students:', error)
      })
  }, [])

  console.log(students)

  const handleRemoveStudent = (enrollmentId, courseId, studentID) => {
    const data = { id: enrollmentId, course_id: courseId, is_active: false, student: studentID }

    api
      .put(`/api/courses/${courseId}/remove_student/${enrollmentId}/`, data)
      .then(() => {
        setIsRemoved(true)
        setIsUnblocked(false)
        alert('Student removed successfully')
      })
      .catch((error) => {
        console.error('Error removing student:', error)
      })
  }

  const handleUnblockStudent = (enrollmentId, courseId, studentID) => {
    const data = { id: enrollmentId, course_id: courseId, is_active: false, student: studentID }

    api
      .put(`/api/courses/${courseId}/unblock_student/${enrollmentId}/`, data)
      .then(() => {
        setIsUnblocked(true)
        setIsRemoved(false)
        alert('Student unblocked successfully')
      })
      .catch((error) => {
        console.error('Error unblocking student:', error)
      })
  }

  if (Object.keys(students).length === 0) {
    return <div>No students enrolled in any course.</div>
  }

  return (
    <div>
      {Object.entries(students).map(([courseTitle, students]) => (
        <CCard key={courseTitle} className="mb-4">
          <CCardBody>
            <CCardTitle>{courseTitle}</CCardTitle>
            <CTable striped hover responsive>
              <CTableHead>
                <CTableRow>
                  <CTableHeaderCell>First Name</CTableHeaderCell>
                  <CTableHeaderCell>Last Name</CTableHeaderCell>
                  <CTableHeaderCell>Email</CTableHeaderCell>
                  <CTableHeaderCell>Actions</CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {students.map((student) => (
                  <CTableRow key={student.student}>
                    <CTableDataCell>{student.student_details.first_name}</CTableDataCell>
                    <CTableDataCell>{student.student_details.last_name}</CTableDataCell>
                    <CTableDataCell>{student.student_details.email}</CTableDataCell>
                    <CTableDataCell>
                      <CButton
                        color="danger"
                        className="me-2 rounded-pill shadow-sm"
                        onClick={() =>
                          handleRemoveStudent(student.id, student.course, student.student)
                        }
                        disabled={isRemoved}
                      >
                        <CIcon icon={cilXCircle} />
                        Remove
                      </CButton>
                      <CButton
                        color="success"
                        className="rounded-pill shadow-sm"
                        onClick={() =>
                          handleUnblockStudent(student.id, student.course, student.student)
                        }
                        disabled={isUnblocked}
                      >
                        <CIcon icon={cilCheck} />
                        Unblock
                      </CButton>
                    </CTableDataCell>
                  </CTableRow>
                ))}
              </CTableBody>
            </CTable>
          </CCardBody>
        </CCard>
      ))}
    </div>
  )
}

export default ViewEnrolledStudents
