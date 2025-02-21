import os
from twilio.rest import Client
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def send_whatsapp_message(to: str, message: str):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    logger.info(f"TWILIO_ACCOUNT_SID: {account_sid}")
    logger.info(f"TWILIO_AUTH_TOKEN: {auth_token}")
    logger.info(f"TWILIO_PHONE_NUMBER: {from_phone_number}")
    
    if not account_sid or not auth_token or not from_phone_number:
        logger.error("Twilio credentials or phone number are not set")
        raise HTTPException(status_code=500, detail="Twilio credentials or phone number are not set")
    
    client = Client(account_sid, auth_token)
    try:
        logger.info(f"Sending message to {to}")
        message = client.messages.create(
            body=message,
            from_=from_phone_number,
            to=f'whatsapp:{to}'
        )
        logger.info(f"Message sent with SID: {message.sid}")
        return {"message_id": message.sid, "status": "sent"}
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem via Twilio: {e}")