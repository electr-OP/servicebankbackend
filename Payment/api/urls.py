from Payment.api.views.history import PaymentHistoryUserView
from django.urls import include, path
from .views import *
from .views import *


urlpatterns = [
    path("wallet/fund/paystack", PaystackPaymentVerifyView.as_view(), name=""),
    path("wallet/withdraw", UserWithdrawalView.as_view(), name=""),
    # path("order/pay", OrderPaymentView.as_view(), name=""),
    # path("paystack/card/add", PaystackAddCardView.as_view(), name=""),

    #payment History
    path("user/history", PaymentHistoryUserView.as_view(), name=""),
    
]
