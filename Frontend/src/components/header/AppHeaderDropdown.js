import React from 'react'
import {  useNavigate } from 'react-router-dom'
import { REFRESH_TOKEN, ACCESS_TOKEN } from '../../constants'
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
import {
  cilUser,
  cilAccountLogout,
} from '@coreui/icons'
import CIcon from '@coreui/icons-react'

import avatar8 from '../../assets/images/avatars/8.jpg'

const AppHeaderDropdown = () => {

  const navigate = useNavigate()

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN)

    try {
      const res = await api.post('/api/auth/logout/', { refresh: refreshToken })
      if (res.status >= 200 && res.status < 300) {
        localStorage.removeItem(ACCESS_TOKEN)
        localStorage.removeItem(REFRESH_TOKEN)
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
        <CAvatar src={avatar8} size="md" />
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-body-secondary fw-semibold my-2">Settings</CDropdownHeader>
        <CDropdownItem href="#">
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
