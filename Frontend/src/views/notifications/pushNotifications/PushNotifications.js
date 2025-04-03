import { useEffect, useState } from 'react'
import { CAlert, CContainer } from '@coreui/react'
import api from '../../../services/api'

const Notifications = () => {
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    // Fetch stored notifications from the API
    const fetchNotifications = async () => {
      try {
        const response = await api.get('/api/notifications/notifications/')
        setNotifications(response.data)
      } catch (error) {
        console.error('Error fetching notifications:', error)
      }
    }

    fetchNotifications()

    // WebSocket connection
    const token = localStorage.getItem('access')
    if (!token) return
    const ws = new WebSocket(`ws://144.126.234.87:8002/ws/notifications/?token=${token}`)

    ws.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      console.log('WebSocket message received:', event.data)
      const data = JSON.parse(event.data)
      if (data.message) {
        setNotifications((prev) => [...prev, { id: data.id, content: data.message }])
      } else {
        console.error('Unexpected WebSocket message format:', data)
      }
    }

    ws.onclose = () => {
      console.log('WebSocket closed')
    }

    return () => ws.close()
  }, [])

  const handleDismiss = async (id) => {
    try {
      await api.delete(`/api/notifications/notifications/${id}/`)
      setNotifications((prev) => prev.filter((notification) => notification.id !== id))
    } catch (error) {
      console.error('Error deleting notification:', error)
    }
  }

  return (
    <CContainer>
      <h3>Notifications</h3>
      {notifications.length === 0 ? (
        <CAlert color="info">No notifications available</CAlert>
      ) : (
        notifications.map((notification, index) => (
          <CAlert
            key={index}
            color="primary"
            dismissible
            onClose={() => handleDismiss(notification.id)}
          >
            {notification.content}
          </CAlert>
        ))
      )}
    </CContainer>
  )
}

export default Notifications
