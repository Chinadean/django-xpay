from djangoxpay.models import BaseModel, Money


class Payment(BaseModel):
    def __init__(self,
                 source_id: str,
                 amount_money=None,
                 app_fee_money=None,
                 autocomplete: bool = True,
                 customer_id=None,
                 location_id=None,
                 reference_id=None,
                 note=None, ):
        self.source_id = source_id
        self.amount_money = amount_money.json if isinstance(amount_money, Money) else amount_money
        self.app_fee_money = app_fee_money.json if isinstance(app_fee_money, Money) else app_fee_money
        self.autocomplete = autocomplete
        self.customer_id = customer_id
        self.location_id = location_id
        self.reference_id = reference_id
        self.note = note
