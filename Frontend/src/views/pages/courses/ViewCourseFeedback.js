import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { CCard, CCardBody, CCardHeader, CListGroup, CListGroupItem, CSpinner } from '@coreui/react'
import api from '../../../services/api'

const ViewCourseFeedback = () => {
  const { id } = useParams()
  const [feedback, setFeedback] = useState([])
  const [loading, setLoading] = useState(true)
  const [userDetails, setUserDetails] = useState({})

  useEffect(() => {
    const fetchFeedback = async () => {
      try {
        const response = await api.get(`/api/feedback/feedback/`)
        const filteredFeedback = response.data.filter((item) => item.course === Number(id))
        setFeedback(filteredFeedback)

        filteredFeedback.forEach((item) => fetchUser(item.student))
      } catch (error) {
        console.error('Error fetching feedback:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchFeedback()
  }, [id])

  const fetchUser = async (userId) => {
    if (userDetails[userId]) return 

    try {
      const response = await api.get(`/api/auth/user/${userId}/`)
      setUserDetails((prev) => ({
        ...prev,
        [userId]: `${response.data.first_name} ${response.data.last_name}`,
      }))
    } catch (error) {
      console.error('Error fetching user:', error)
    }
  }

  if (loading) {
    return <CSpinner color="primary" />
  }

  return (
    <CCard>
      <CCardHeader>Course Feedback</CCardHeader>
      <CCardBody>
        <CListGroup>
          {feedback.map((item, index) => (
            <CListGroupItem key={index}>
              <strong>{userDetails[item.student] || 'Loading...'}</strong>: {item.comment}
            </CListGroupItem>
          ))}
        </CListGroup>
      </CCardBody>
    </CCard>
  )
}

export default ViewCourseFeedback
