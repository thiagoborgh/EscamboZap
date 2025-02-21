from app.models import PaymentRequest

def process_payment(request: PaymentRequest):
    # Simulação de processamento de pagamento
    return {"message": f"Pagamento de R${request.amount:.2f} recebido de {request.user}. Transação aprovada!"}