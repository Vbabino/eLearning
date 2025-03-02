import React, { useEffect, useState } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CInputGroup,
  CInputGroupText,
  CFormInput,
  CButton,
  CListGroup,
  CListGroupItem,
} from '@coreui/react'

import api from '../../services/api'
 
const Chat = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [userDetails, setUserDetails] = useState({})
  const userId = localStorage.getItem('id')

  useEffect(() => {
    const token = localStorage.getItem('access')
    if (!token) return
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/?token=${token}`)

    ws.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.onmessage = async (event) => {
      console.log('📩 WebSocket message received:', event.data)
      const data = JSON.parse(event.data)
      console.log('Parsed data:', data)

      if (!data.message) {
        console.error('🚨 WebSocket message missing "message" field:', data)
        return
      }

      if (!data.sender_id) {
        console.warn('⚠️ WebSocket message missing "sender_id":', data)
        setMessages((prev) => [...prev, { sender_id: 'Unknown', message: data.message }])
        return
      }

      // Fetch sender name if not already fetched
      if (!userDetails[data.sender_id]) {
        await fetchUser(data.sender_id)
      }

      setMessages((prev) => [...prev, { sender_id: data.sender_id, message: data.message }])
    }

    ws.onclose = () => {
      console.log('WebSocket closed')
    }

    window.chatSocket = ws
    fetchUser(userId)

    return () => ws.close()
  }, [])

  const handleSend = () => {
    if (input.trim()) {
      const messageData = JSON.stringify({ message: input, sender_id: userId })
      console.log('📤 Sending message:', messageData)
      
      window.chatSocket.send(messageData)

    //   setMessages((prev) => [...prev, { sender_id: userId, message: input }])
      setInput('')
    }
  }

  const fetchUser = async (userId) => {
    if (userDetails[userId]) return

    try {
      const response = await api.get(`/api/auth/user/${userId}/`)
      setUserDetails((prev) => ({
        ...prev,
        [userId]: `${response.data.first_name} ${response.data.last_name}`,
      }))
    } catch (error) {
      console.error('Error fetching user:', error)
    }
  }

  return (
    <CCard>
      <CCardHeader>Chat with e-learners!</CCardHeader>
      <CCardBody>
        <CListGroup>
          {messages.map((msg, index) => (
            <CListGroupItem key={index}>
              <strong>{userDetails[msg.sender_id] || 'Unknown User'}:</strong> {msg.message}
            </CListGroupItem>
          ))}
        </CListGroup>
        <CInputGroup className="mt-3">
          <CFormInput
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <CInputGroupText>
            <CButton color="primary" onClick={handleSend}>
              Send
            </CButton>
          </CInputGroupText>
        </CInputGroup>
      </CCardBody>
    </CCard>
  )
}

export default Chat
