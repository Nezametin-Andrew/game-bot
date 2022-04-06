from .serializers import PaymentSerializer
from .models import Payment


class PaymentMixin:

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
