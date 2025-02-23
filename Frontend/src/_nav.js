import React from 'react'
import CIcon from '@coreui/icons-react'
import {
  cilCursor,
  cilSpeedometer,
  cilEducation,
  cilBook,
} from '@coreui/icons'
import { CNavGroup, CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavItem,
    name: 'Dashboard',
    to: '/dashboard',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
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
        to: '/base/accordion',
      },
      {
        component: CNavItem,
        name: 'View Course Materials',
        to: '/base/accordion',
      },
      {
        component: CNavItem,
        name: 'Upload Materials',
        to: '/base/accordion',
      },
      {
        component: CNavItem,
        name: 'Search Users',
        to: '/teachers/user-search',
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
        to: '/base/accordion',
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
