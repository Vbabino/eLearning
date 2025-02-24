import React, { useState, useEffect } from 'react'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CFormInput,
  CFormSelect,
} from '@coreui/react'

import api from '../../../../services/api'
import { useNavigate } from 'react-router-dom'

const UserSearch = () => {
  const [query, setQuery] = useState('')
  const [searchField, setSearchField] = useState('last_name__icontains')
  const [users, setUsers] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    if (query.length > 2) {
      api
        .get(`/api/auth/user/search/?${searchField}=${query}`)
        .then((response) => setUsers(response.data))
        .catch((error) => {
          console.error('Error fetching users:', error)
          setUsers([])
        })
    } else {
      setUsers([])
    }
  }, [query, searchField])

  return (
    <div>
      {/* Dropdown for selecting search filter */}
      <CFormSelect
        value={searchField}
        onChange={(e) => setSearchField(e.target.value)}
        className="mb-3"
      >
        <option value="last_name__icontains">Search by Last Name</option>
        <option value="first_name__icontains">Search by First Name</option>
        <option value="email__icontains">Search by Email</option>
      </CFormSelect>

      {/* Search input field */}
      <CFormInput
        type="text"
        placeholder="Enter search term..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {/* Display results */}
      <CTable striped hover className="mt-3">
        <CTableHead>
          <CTableRow>
            <CTableHeaderCell>#</CTableHeaderCell>
            <CTableHeaderCell>Email</CTableHeaderCell>
            <CTableHeaderCell>First Name</CTableHeaderCell>
            <CTableHeaderCell>Last Name</CTableHeaderCell>
            <CTableHeaderCell>User Type</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {users.map((user, index) => (
            <CTableRow
              key={user.id}
              onClick={() => navigate(`/user/${user.id}`)}
              style={{ cursor: 'pointer' }}
            >
              <CTableDataCell>{index + 1}</CTableDataCell>
              <CTableDataCell>{user.email}</CTableDataCell>
              <CTableDataCell>{user.first_name}</CTableDataCell>
              <CTableDataCell>{user.last_name}</CTableDataCell>
              <CTableDataCell>{user.user_type}</CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
    </div>
  )
}

export default UserSearch
