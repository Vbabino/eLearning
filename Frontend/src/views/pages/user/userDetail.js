import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../../../services/api'
import { CCard, CAvatar, CCardBody, CCardTitle, CCardText, CSpinner } from '@coreui/react'

import nopic from '../../../assets/images/avatars/nopic-50.png'


const UserDetail = () => {
  const { id } = useParams()
  const [user, setUser] = useState(null)
  const [profilePic, setProfilePic] = useState()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api
      .get(`/api/auth/user/${id}/`)
      .then((response) => {
        setUser(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error fetching user details:', error)
        setLoading(false)
      })
  }, [id])

  useEffect(() => {
    const fetchProfilePic = async () => {
      try {
        const response = await api.get(`/api/auth/user-photo/${id}/`)
        setProfilePic(response.data.photo)
      } catch (error) {
        console.error('Error fetching user photo:', error)
      }
    }

    fetchProfilePic()
  }, [id])

  if (loading) {
    return <CSpinner color="primary" />
  }

  return (
    <CCard>
      <CCardBody>
        <CCardTitle>User Details</CCardTitle>
        <CAvatar src={profilePic ? profilePic : nopic} size="md" />
        <CCardText>
          <strong>Email:</strong> {user.email}
        </CCardText>
        <CCardText>
          <strong>First Name:</strong> {user.first_name}
        </CCardText>
        <CCardText>
          <strong>Last Name:</strong> {user.last_name}
        </CCardText>
        <CCardText>
          <strong>User Type:</strong> {user.user_type}
        </CCardText>
      </CCardBody>
    </CCard>
  )
}

export default UserDetail
