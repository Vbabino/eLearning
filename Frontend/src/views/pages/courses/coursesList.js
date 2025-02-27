import React, { useEffect, useState } from 'react'
import { CCard, CCardBody, CCardHeader, CCol, CRow, CFormInput, CFormSelect } from '@coreui/react'
import { useNavigate } from 'react-router-dom'


import api from '../../../services/api'

const CoursesList = () => {
  const [query, setQuery] = useState('')
  const [searchField, setSearchField] = useState('title__icontains')
  const [courses, setCourses] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get(`/api/courses/course/search/?${searchField}=${query}`)
        setCourses(response.data)
      } catch (error) {
        console.error('Error fetching courses:', error)
      }
    }

    fetchCourses()
  }, [query, searchField])

  return (
    <div>
      {/* Dropdown for selecting search filter */}
      <CFormSelect
        value={searchField}
        onChange={(e) => setSearchField(e.target.value)}
        className="mb-3"
      >
        <option value="title__icontains">Search by Title</option>
        <option value="description__icontains">Search by Description</option>
      </CFormSelect>
      {/* Search input field */}
      <CFormInput
        type="text"
        placeholder="Enter search term..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="mb-3"
      />

      {/* Display results */}
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
              </CCardBody>
            </CCard>
          </CCol>
        ))}
      </CRow>
    </div>
  )
}

export default CoursesList
