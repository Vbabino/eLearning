import React, { useState } from 'react';
import { CButton, CContainer, CForm, CFormInput, CFormTextarea } from '@coreui/react'
import api from '../../../services/api'
import { useNavigate } from 'react-router-dom'


const CreateCourse = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const navigate = useNavigate();
    const teacherId = localStorage.getItem('id') 

    const handleSubmit = async (e) => {
        e.preventDefault();
        const courseData = {
            title,
            description,
            teacher: teacherId 
        };

        try {
            await api.post('/api/courses/list/', courseData);
            alert('Course created successfully!');
            navigate('/teachers/manage-courses');
        } catch (error) {
            console.error('There was an error creating the course!', error);
            alert('Failed to create course. Please try again.');
        }
    };

    return (
      <CContainer>
        <h2>Create New Course</h2>
        <CForm onSubmit={handleSubmit}>
          <div>
            <label htmlFor="title">Title</label>
            <CFormInput
              className="mb-2"
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="description">Description</label>
            <CFormTextarea
              className="mb-2"
              id="description"
              value={description}
              rows={10}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <CButton type="submit" color="primary">
            Create Course
          </CButton>
        </CForm>
      </CContainer>
    )
};

export default CreateCourse;