from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from .serializers import PaymentSerializer
from .models import Payment
from .mixins import PaymentMixin


class PaymentApiView(ListAPIView):

    us_id = None
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        if kwargs.get('user_id') is not None:
            self.us_id = kwargs['user_id']
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.us_id is not None:
            return Payment.objects.filter(user=self.us_id)
        return Payment.objects.all()


class CreatePaymentApiView(PaymentMixin, CreateAPIView):

    ...


class DeletePaymentApiView(PaymentMixin, DestroyAPIView):

    ...
