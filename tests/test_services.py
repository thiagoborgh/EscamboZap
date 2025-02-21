import pytest
from unittest.mock import patch
from app.services.messaging import send_whatsapp_message

@patch('app.services.messaging.Client')
def test_send_whatsapp_message(mock_client):
    mock_client.return_value.messages.create.return_value.sid = "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    response = send_whatsapp_message("+14155552671", "Test message")
    assert response["status"] == "sent"
    assert response["message_id"] == "SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"