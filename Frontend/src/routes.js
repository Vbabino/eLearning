import React from 'react'

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

// User
const ViewUser = React.lazy(() => import('./views/pages/user/view-user'))
const UpdateUser = React.lazy(() => import('./views/pages/user/update-user'))
const UploadProfilePhoto = React.lazy(() => import('./views/pages/user/upload-profile-photo'))

// Teacher
// const ManageCourses = React.lazy(() => import('./views/teachers/manage-courses/ManageCourses'))
// const ViewCourseMaterials = React.lazy(() => import('./views/teachers/view-course-materials/ViewCourseMaterials'))
// const UploadMaterials = React.lazy(() => import('./views/teachers/upload-materials/UploadMaterials'))
const UserSearch = React.lazy(() => import('./views/teachers/user-search/UserSearch'))
// const ManageStudents = React.lazy(() => import('./views/teachers/manage-students/ManageStudents'))


const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },

  // User routes
  { path: '/user/view', name: 'View User', element: ViewUser },
  { path: '/user/update', name: 'Update User', element: UpdateUser },
  { path: '/user/upload-profile-photo', name: 'Upload Profile Photo', element: UploadProfilePhoto },

  // Teacher routes
  
  // { path: '/teachers/manage-courses', name: 'Manage Courses', element: ManageCourses },
  // { path: '/teachers/view-course-materials', name: 'View Course Materials', element: ViewCourseMaterials },
  // { path: '/teachers/upload-materials', name: 'Upload Materials', element: UploadMaterials },
  { path: '/teachers/user-search', name: 'User Search', element: UserSearch },
  // { path: '/teachers/manage-students', name: 'Manage Students', element: ManageStudents },
]

export default routes
