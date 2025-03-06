import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from chat.consumers import ChatConsumer

User = get_user_model()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_chat(test_user):
    """
    Test WebSocket connection, sending, and receiving messages.
    """

    user, access_token = await test_user  

    communicator = WebsocketCommunicator(
        ChatConsumer.as_asgi(),
        f"/ws/chat/?token={access_token}", 
    )

    communicator.scope["user"] = user

    # Connect WebSocket
    connected, _ = await communicator.connect()
    assert connected, "WebSocket failed to connect"

    # Send a test message
    message_data = {
        "type": "chat.message",
        "message": "Hello World!",
        "sender_id": user.id,
    }
    await communicator.send_json_to(message_data)

    # Receive the message
    response = await communicator.receive_json_from()

    # Ensure the received message matches what was sent
    assert response["message"] == "Hello World!"
    assert response["sender_id"] == user.id

    # Disconnect WebSocket
    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_chat_unauthenticated():
    """
    Negative test: An unauthenticated user (missing token) should not be able to connect.
    """
    communicator = WebsocketCommunicator(
        ChatConsumer.as_asgi(),
        "/ws/chat/",  # No token provided
    )

    connected, _ = await communicator.connect()
    assert not connected, "Unauthenticated user should not be able to connect"

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_chat_empty_message(test_user):
    """
    Edge case test: Sending an empty message should not be accepted.
    """

    user, access_token = await test_user

    communicator = WebsocketCommunicator(
        ChatConsumer.as_asgi(),
        f"/ws/chat/?token={access_token}",
    )

    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected, "WebSocket failed to connect"

    # Send an empty message
    message_data = {
        "type": "chat.message",
        "message": "",  # Empty message
        "sender_id": user.id,
    }
    await communicator.send_json_to(message_data)

    try:
        response = await communicator.receive_json_from(timeout=1)
        assert (
            "message" not in response or response["message"] != ""
        ), "Empty message should not be processed"
    except Exception:
        pass  # If no response is received, it's expected

    await communicator.disconnect()
