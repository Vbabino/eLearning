import React from 'react';
import { CCard, CCardBody, CCardHeader, CContainer, CRow, CCol, CNavLink, CButton } from '@coreui/react'
import { NavLink } from 'react-router-dom'


const PendingApproval = () => {
    return (
      <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
        <CContainer>
          <CRow className="justify-content-center">
            <CCol md="8">
              <CCard>
                <CCardHeader>Pending Approval</CCardHeader>
                <CCardBody>
                  <p>
                    Your account is pending approval by the admin. Please check back later for
                    updates.
                  </p>
                  <CButton to="/login" as={NavLink} color="primary">
                    Login
                  </CButton>
                </CCardBody>
              </CCard>
            </CCol>
          </CRow>
        </CContainer>
      </div>
    )
};

export default PendingApproval;