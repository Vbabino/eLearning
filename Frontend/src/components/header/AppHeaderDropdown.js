import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { REFRESH_TOKEN, ACCESS_TOKEN, IS_APPROVED, ID } from '../../constants'
import api from '../../services/api'
import {
  CAvatar,
  CDropdown,
  CDropdownDivider,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react'
import { cilUser, cilAccountLogout } from '@coreui/icons'
import CIcon from '@coreui/icons-react'

import nopic from '../../assets/images/avatars/nopic-50.png'

const AppHeaderDropdown = () => {
  const id = localStorage.getItem(ID)
  const profileUpdated = localStorage.getItem('profileUpdated')
  const [profilePic, setProfilePic] = useState()
  const navigate = useNavigate()

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

  
  }, [profileUpdated])

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN)

    try {
      const res = await api.post('/api/auth/logout/', { refresh: refreshToken })
      if (res.status >= 200 && res.status < 300) {
        localStorage.removeItem(ACCESS_TOKEN)
        localStorage.removeItem(REFRESH_TOKEN)
        localStorage.removeItem(IS_APPROVED)
        localStorage.removeItem(ID)

        localStorage.clear()
        navigate('/login', { replace: true })
      }
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0 pe-0" caret={false}>
        <CAvatar src={profilePic ? profilePic : nopic} size="md" />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-body-secondary fw-semibold my-2">Settings</CDropdownHeader>
        <CDropdownItem onClick={() => navigate('/user/view')}>
          <CIcon icon={cilUser} className="me-2" />
          Profile
        </CDropdownItem>
        <CDropdownDivider />
        <CDropdownItem onClick={handleLogout}>
          <CIcon icon={cilAccountLogout} className="me-2" />
          Log Out
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

export default AppHeaderDropdown
