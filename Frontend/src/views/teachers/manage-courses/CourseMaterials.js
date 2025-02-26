import React, { useEffect, useState } from 'react'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CButton,
} from '@coreui/react'
import api from '../../../services/api'
import { useParams } from 'react-router-dom'

const CourseMaterials = () => {
  const { id } = useParams()

  const [materials, setMaterials] = useState([])

  useEffect(() => {
    api
      .get(`/api/courses/materials/${id}/`)
      .then((response) => setMaterials(response.data))
      .catch((error) => console.error('Error fetching materials:', error))
  }, [id])

  return (
    <div>
      <h3>Course Materials</h3>
      {materials.length === 0 ? (
        <p>No materials available.</p>
      ) : (
        <CTable striped hover>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell>#</CTableHeaderCell>
              <CTableHeaderCell>File Name</CTableHeaderCell>
              <CTableHeaderCell>Description</CTableHeaderCell>
              <CTableHeaderCell>Download</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            {materials.map((material, index) => (
              <CTableRow key={material.id}>
                <CTableDataCell>{index + 1}</CTableDataCell>
                <CTableDataCell>{material.file_name}</CTableDataCell>
                <CTableDataCell>{material.description}</CTableDataCell>
                <CTableDataCell>
                  <CButton color="primary" href={material.file} target="_blank" download>
                    Download
                  </CButton>
                </CTableDataCell>
              </CTableRow>
            ))}
          </CTableBody>
        </CTable>
      )}
    </div>
  )
}

export default CourseMaterials
