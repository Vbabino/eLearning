import React, { useEffect, useState } from 'react'
import { CCard, CCardBody, CCardHeader, CSpinner, CButton } from '@coreui/react'
import { useNavigate } from 'react-router-dom'
import api from '../../../services/api'

const ViewUser = () => {
  const id = localStorage.getItem('id')
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    api
      .get(`/api/auth/user/${id}/`)

      .then((response) => {
        setUser(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error fetching user:', error)
        setLoading(false)
      })
  }, [id])

  if (loading) {
    return <CSpinner color="primary" />
  }

  if (!user) {
    return <div>User not found</div>
  }

  return (
    <CCard>
      <CCardHeader>User Details</CCardHeader>
      <CCardBody>
        <p>
          <strong>First name:</strong> {user.first_name}
        </p>
        <p>
          <strong>Last Name:</strong> {user.last_name}
        </p>
        <p>
          <strong>Email:</strong> {user.email}
        </p>
        <CButton
          onClick={() => {
            navigate(`/user/update`)
          }}
          color="primary"
        >
          Update
        </CButton>
        <CButton
          className="mx-2"
          color="secondary"
          onClick={() => {
            navigate(`/user/upload-profile-photo`)
          }}
        >
          Upload Profile Picture
        </CButton>
      </CCardBody>
    </CCard>
  )
}

export default ViewUser
