import React, { useState } from 'react'
import { CButton, CForm, CFormInput } from '@coreui/react'
import api from '../../../services/api'
import { useNavigate } from 'react-router-dom'
import { useParams } from 'react-router-dom'

const UploadCourseMaterials = () => {
  const { id } = useParams()
  const [file, setFile] = useState(null)
  const [description, setDescription] = useState('')
  const [fileName, setFileName] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value)
  }

  const handleFileNameChange = (e) => {
    setFileName(e.target.value)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('description', description)
    formData.append('course', id)
    formData.append('file_name', fileName)

    try {
      const response = await api.post(`/api/courses/${id}/materials/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      console.log('File uploaded successfully', response.data)
      alert('File uploaded successfully')
    } catch (error) {
      console.error('Error uploading file', error)
    } finally {
      setLoading(false)
    }
  }
  return (
    <CForm onSubmit={handleSubmit}>
      <CFormInput
        className="mb-2"
        type="file"
        onChange={handleFileChange}
        label="Choose File"
        required
      />
      <CFormInput
        className="mb-2"
        type="text"
        placeholder="File Name"
        value={fileName}
        onChange={handleFileNameChange}
      />
      <CFormInput
        type="text"
        placeholder="Description"
        value={description}
        onChange={handleDescriptionChange}
      />
      <CButton
        type="submit"
        className="mt-2"
        color="primary"
        disabled={loading}
        onClick={() => navigate('/teachers/manage-courses')}
      >
        {loading ? 'Uploading...' : 'Upload'}
      </CButton>
    </CForm>
  )
}

export default UploadCourseMaterials
