from enum import Enum


class EOrder(Enum):
    CREATED = "criado"
    EXPIRED = "expirado"
    ANALYSIS = "em analise"
    COMPLETE = "concluido"
    CARHEBACK = "chargeback"
    PAID = "pago"
    REFUNDED = "reembolsado"
    FAILED = "falha no pagamento"
    