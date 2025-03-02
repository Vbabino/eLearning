import React from 'react'

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))

// User
const ViewUser = React.lazy(() => import('./views/pages/user/view-user'))
const UserDetail = React.lazy(() => import('./views/pages/user/userDetail'))
const UpdateUser = React.lazy(() => import('./views/pages/user/update-user'))
const UserSearch = React.lazy(() => import('./views/pages/user/user-search/UserSearch'))
const UploadProfilePhoto = React.lazy(() => import('./views/pages/user/upload-profile-photo'))

// Teacher
const ViewCourses = React.lazy(() => import('./views/teachers/manage-courses/ViewCourses'))
const EditCourseDetails = React.lazy(() => import('./views/teachers/manage-courses/EditCourse'))
const CreateCourse = React.lazy(() => import('./views/teachers/manage-courses/CreateCourse'))
const UploadCourseMaterials = React.lazy(() => import('./views/teachers/manage-courses/UploadCourseMaterials'))
const CourseMaterials = React.lazy(() => import('./views/teachers/manage-courses/CourseMaterials'))
const ViewEnrolledStudents = React.lazy(() => import('./views/teachers/manage-students/ViewEnrolledStudents'))

//Students
const EnrolledCourses = React.lazy(() => import('./views/students/in-progress/EnrolledCourses'))
const ViewCourseMaterials = React.lazy(() => import('./views/students/in-progress/ViewCourseMaterials'))
const FeedbackView = React.lazy(() => import('./views/students/in-progress/FeedbackView'))

// Courses
const CoursesList = React.lazy(() => import('./views/pages/courses/coursesList'))
const CourseDetails = React.lazy(() => import('./views/pages/courses/courseDetails'))
const ViewCourseFeedback = React.lazy(() => import('./views/pages/courses/ViewCourseFeedback'))

// Notifications
const PushNotifications = React.lazy(() => import('./views/notifications/pushNotifications/PushNotifications'))

// Chat
const Chat = React.lazy(() => import('./views/chat/Chat'))

const routes = [
  // Default route
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Search Course', element: Dashboard },
  
  // User routes
  { path: '/user/view', name: 'View User', element: ViewUser },
  { path: '/user/:id', name: 'User Detail', element: UserDetail },
  { path: '/user/update', name: 'Update User', element: UpdateUser },
  { path: '/user/user-search/', name: 'Search User', element: UserSearch },
  { path: '/user/upload-profile-photo', name: 'Upload Profile Photo', element: UploadProfilePhoto },

  // Courses routes
  { path: '/courses/list', name: 'Courses List', element: CoursesList },
  {path: '/courses/:id', name: 'Course Details', element: CourseDetails},
  {path: '/courses/:id/feedback', name: 'Course Feedback', element: ViewCourseFeedback},
  
  // Student routes
  {path: '/students/enrolled-courses', name: 'Enrolled Courses', element: EnrolledCourses},
  {path: '/students/enrolled-courses-materials/:id', name: 'Course Materials', element: ViewCourseMaterials},
  {path: '/students/enrolled-courses-feedback/:id/', name: 'Feedback', element: FeedbackView},

  // Teacher routes
  { path: '/teachers/manage-courses', name: 'Manage Courses', element: ViewCourses },
  {path: '/teachers/manage-courses/:id', name: 'Edit Course', element: EditCourseDetails},
  {path: '/teachers/manage-courses/create', name: 'Create Course', element: CreateCourse},
  {path: '/teachers/manage-courses/:id/upload', name: 'Upload Course Materials', element: UploadCourseMaterials},
  {path: '/teachers/manage-courses/:id/materials', name: 'Course Materials', element: CourseMaterials},
  {path: '/teachers/manage-students/', name: 'Enrolled Students', element: ViewEnrolledStudents},

  // Notifications
  {path: '/notifications/push', name: 'Push Notifications', element: PushNotifications},

  // Chat
  {path: '/chat', name: 'Chat', element: Chat},
  
]

export default routes
