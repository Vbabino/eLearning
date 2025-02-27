import React from 'react'
import CIcon from '@coreui/icons-react'
import { cilCursor, cilEducation, cilBook, cilSearch } from '@coreui/icons'
import { CNavGroup, CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavItem,
    name: 'Search Courses',
    to: '/courses/list',
    icon: <CIcon icon={cilSearch} customClassName="nav-icon" />,
    badge: {
      color: 'info',
    },
  },
  {
    component: CNavItem,
    name: 'Search Users',
    to: '/user/user-search/',
    icon: <CIcon icon={cilSearch} customClassName="nav-icon" />,
    badge: {
      color: 'info',
    },
  },

  {
    component: CNavTitle,
    name: 'Teachers',
  },
  {
    component: CNavGroup,
    name: 'My Courses',
    to: '/theme/colors',
    icon: <CIcon icon={cilEducation} customClassName="nav-icon" />,
    items: [
      {
        component: CNavItem,
        name: 'Manage Courses',
        to: '/teachers/manage-courses',
      },

      {
        component: CNavItem,
        name: 'Manage Students',
        to: '/base/accordion',
      },
    ],
  },
  {
    component: CNavTitle,
    name: 'Students',
  },
  {
    component: CNavGroup,
    name: 'Courses',
    to: '/base',
    icon: <CIcon icon={cilBook} customClassName="nav-icon" />,
    items: [
      {
        component: CNavItem,
        name: 'In Progress',
        to: '/students/enrolled-courses',
      },
      {
        component: CNavItem,
        name: 'Your Updates',
        to: '/base/accordion',
      },
      {
        component: CNavItem,
        name: 'Your Feedback',
        to: '/base/accordion',
      },
    ],
  },
  {
    component: CNavTitle,
    name: 'Collaboration',
  },
  {
    component: CNavGroup,
    name: 'Interactive Tools',
    icon: <CIcon icon={cilCursor} customClassName="nav-icon" />,
    items: [
      {
        component: CNavItem,
        name: 'Whiteboard',
        to: '/whiteboard',
      },
    ],
  },
]

export default _nav
