import React, { useState } from 'react';
import { CForm, CButton, CContainer, CFormTextarea } from '@coreui/react'
import api from '../../../services/api';
import { useNavigate } from 'react-router-dom';
import { useParams } from 'react-router-dom'


const FeedbackView = () => {
    const [comment, setComment] = useState('');
    const navigate = useNavigate();
    const { id } = useParams();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const student = localStorage.getItem('id');
        const course = id;
        const feedbackData = {
            comment,
            student,
            course
        };

        try {
            await api.post('/api/feedback/feedback/', feedbackData);
            alert('Feedback submitted successfully');
        } catch (error) {
            console.error('Error submitting feedback:', error);
        }
    };

    return (
      <CContainer>
        <CForm onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="comment" className="form-label">
              Comment
            </label>
            <CFormTextarea
              id="comment"
              value={comment}
              rows={10}
              onChange={(e) => setComment(e.target.value)}
              required
            />
          </div>

          <CButton
            type="submit"
            color="primary"
            disabled={!comment}
            onClick={() => navigate('/students/enrolled-courses')}
          >
            Submit Feedback
          </CButton>
        </CForm>
      </CContainer>
    )
};

export default FeedbackView;