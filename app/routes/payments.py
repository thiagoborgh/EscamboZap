from fastapi import APIRouter, HTTPException, Depends
from app.models import PaymentRequest
from app.services.payments import process_payment

router = APIRouter()

@router.post("/")
def make_payment(request: PaymentRequest):
    return process_payment(request)